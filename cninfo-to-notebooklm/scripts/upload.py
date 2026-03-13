#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upload PDF files to NotebookLM using notebooklm-py CLI

Prerequisites:
pip install notebooklm-py playwright
playwright install chromium
notebooklm login  # Authenticate first
"""

import sys
import os
import subprocess
import json
import shutil
import time
import re

# Cache file for notebook mappings
NOTEBOOK_CACHE_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "notebook_cache.json"
)

def check_notebooklm_installed() -> bool:
    """Check if notebooklm CLI is installed"""
    return shutil.which("notebooklm") is not None

def _load_notebook_cache() -> dict:
    """Load notebook cache from file"""
    if os.path.exists(NOTEBOOK_CACHE_FILE):
        try:
            with open(NOTEBOOK_CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def _save_notebook_cache(cache: dict):
    """Save notebook cache to file"""
    try:
        with open(NOTEBOOK_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️ Failed to save notebook cache: {e}")

def _get_cached_notebook(stock_code: str) -> str:
    """Get cached notebook ID for a stock"""
    cache = _load_notebook_cache()
    return cache.get("stocks", {}).get(stock_code, {}).get("notebook_id")

def _cache_notebook(stock_code: str, stock_name: str, notebook_id: str, notebook_title: str):
    """Cache notebook ID for a stock"""
    cache = _load_notebook_cache()
    if "stocks" not in cache:
        cache["stocks"] = {}
    cache["stocks"][stock_code] = {
        "stock_name": stock_name,
        "notebook_id": notebook_id,
        "notebook_title": notebook_title,
        "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    _save_notebook_cache(cache)
    print(f"📝 Cached notebook for {stock_code}: {notebook_id}")

def run_notebooklm_command(args: list) -> tuple:
    """Run notebooklm command and return (success, output)"""
    try:
        result = subprocess.run(
            ["notebooklm"] + args,
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def create_notebook(title: str) -> str:
    """Create a new NotebookLM notebook, returns notebook ID or None"""
    print(f"📚 Creating notebook: {title}")
    success, output = run_notebooklm_command(["create", title])
    if not success:
        print(f"❌ Failed to create notebook: {output}", file=sys.stderr)
        return None

    # Parse output to find notebook ID
    # Output format: "Created notebook: (ID: <id>)" or similar
    for line in output.split("\n"):
        if "ID:" in line or "id:" in line:
            # Extract ID from line
            match = re.search(r"[a-f0-9-]{36}", line)
            if match:
                notebook_id = match.group(0)
                print(f"✅ Created notebook: {notebook_id}")
                return notebook_id

    # Also check for UUID-like patterns
    match = re.search(r"[a-f0-9-]{36}", output)
    if match:
        notebook_id = match.group(0)
        print(f"✅ Created notebook: {notebook_id}")
        return notebook_id

    # Fallback: return trimmed output
    print(f"⚠️ Output: {output}")
    return output.strip().split()[-1] if output.strip() else None

def get_or_create_notebook(stock_code: str, stock_name: str, force_new: bool = False) -> str:
    """Get existing notebook or create new one for a stock"""
    # Check cache first
    if not force_new:
        cached_id = _get_cached_notebook(stock_code)
        if cached_id:
            print(f"📋 Found cached notebook for {stock_code}: {cached_id}")
            # Try to use the notebook - assume it exists even if verification fails
            # (NotebookLM API can be flaky)
            print(f"✅ Using cached notebook: {cached_id}")
            return cached_id
    
    # Create new notebook
    notebook_title = f"{stock_name} 财务报告"
    notebook_id = create_notebook(notebook_title)
    
    if notebook_id:
        _cache_notebook(stock_code, stock_name, notebook_id, notebook_title)
    
    return notebook_id

def get_existing_sources(notebook_id: str) -> set:
    """Get set of existing source names in a notebook"""
    existing = set()
    
    # Set notebook context
    success, output = run_notebooklm_command(["use", notebook_id])
    if not success:
        return existing
    
    # Get source list
    success, output = run_notebooklm_command(["source", "list"])
    if not success:
        return existing
    
    # Parse output to extract source titles
    # Output format is a table with columns: ID, Title, Type, Created, Status
    # Example line: │ 4f32efa0-98cb-… │ 000708_2019_a… │ 📄 PDF │ 2026-03-13 │ ready │
    for line in output.split("\n"):
        line = line.strip()
        if not line:
            continue
        
        # Skip header and separator lines
        if "━━" in line or "─" in line:
            continue
        if "ID" in line and "Title" in line:
            continue
        
        # Look for lines containing PDF source patterns
        # Pattern: │ <id> │ <title> │ 📄 PDF │ ...
        if "│" in line and ("PDF" in line or "Unknown" in line):
            # Split by │ and get the title column (2nd data column)
            parts = [p.strip() for p in line.split("│")]
            # parts[0] is empty (before first │)
            # parts[1] is ID
            # parts[2] is Title
            if len(parts) >= 3:
                title = parts[2].strip()
                if title and not title.startswith("ID"):
                    existing.add(title)
                    # Also add without truncation marker
                    if title.endswith("…"):
                        base = title[:-1]
                        existing.add(base)
    
    return existing

def upload_source(notebook_id: str, file_path: str, skip_existing: bool = True) -> bool:
    """Upload a file as source to a notebook"""
    filename = os.path.basename(file_path)
    print(f"📤 Uploading: {filename}")

    # Set notebook context first
    success, output = run_notebooklm_command(["use", notebook_id])
    if not success:
        print(f"❌ Failed to set notebook: {output}", file=sys.stderr)
        return False
    
    # Check if source already exists (optional)
    if skip_existing:
        success, list_output = run_notebooklm_command(["source", "list"])
        if success and filename.replace(".pdf", "") in list_output:
            print(f"  ⏭️ Source already exists, skipping")
            return True

    # Add source
    success, output = run_notebooklm_command(["source", "add", file_path])
    if success:
        print(f"  ✅ Uploaded successfully")
        return True
    else:
        # Check if error is about duplicate
        if "already exists" in output.lower() or "duplicate" in output.lower():
            print(f"  ⏭️ Source already exists, skipping")
            return True
        print(f"  ❌ Failed: {output}", file=sys.stderr)
        return False

def upload_all_sources(notebook_id: str, files: list) -> dict:
    """Upload multiple files to a notebook with rate limiting and duplicate check"""
    results = {"success": [], "failed": [], "skipped": []}
    
    # Get existing sources once at the beginning
    print(f"📋 Checking existing sources in notebook...")
    existing_sources = get_existing_sources(notebook_id)
    print(f"   Found {len(existing_sources)} existing sources: {list(existing_sources)[:5]}...")
    
    for i, file_path in enumerate(files):
        filename = os.path.basename(file_path)
        filename_no_ext = filename.replace(".pdf", "")
        
        # Check if file already exists (exact match or prefix match for truncated names)
        should_skip = False
        for existing in existing_sources:
            # Check if existing source matches this file
            # Handle truncated names like "000708_2019_a…" matching "000708_2019_annual"
            if existing == filename or existing == filename_no_ext:
                should_skip = True
                break
            # Prefix match for truncated names
            if existing.endswith("…"):
                prefix = existing[:-1]
                if filename_no_ext.startswith(prefix):
                    should_skip = True
                    break
            # Also check if filename starts with existing (non-truncated)
            if filename_no_ext.startswith(existing.rstrip("…")):
                should_skip = True
                break
        
        if should_skip:
            print(f"📤 Skipping (already exists): {filename}")
            results["skipped"].append(file_path)
            continue
        
        # Add delay between uploads to avoid rate limiting
        if i > 0 and len(results["success"]) > 0:
            print(f"  ⏳ Waiting 3 seconds before next upload...")
            time.sleep(3)
        
        if upload_source(notebook_id, file_path, skip_existing=False):
            results["success"].append(file_path)
        else:
            results["failed"].append(file_path)
            # Longer delay after failure
            print(f"  ⏳ Waiting 5 seconds before retry...")
            time.sleep(5)
    
    return results

def cleanup_temp_files(files: list, temp_dir: str = None):
    """Remove temporary files after upload"""
    for f in files:
        try:
            os.remove(f)
        except Exception:
            pass

    if temp_dir and (temp_dir.startswith("/var/folders") or "/tmp/" in temp_dir):
        try:
            shutil.rmtree(temp_dir)
            print(f"🧹 Cleaned up temp directory: {temp_dir}")
        except Exception:
            pass

def configure_notebook(notebook_id: str, prompt_file: str) -> bool:
    """Configure notebook with custom prompt"""
    if not os.path.exists(prompt_file):
        print(f"⚠️ Prompt file not found: {prompt_file}")
        return False

    try:
        with open(prompt_file, "r", encoding="utf-8") as f:
            prompt = f.read()
    except Exception as e:
        print(f"❌ Error reading prompt file: {e}")
        return False

    print(f"⚙️ Configuring notebook with custom prompt...")

    # --persona takes TEXT, so we pass the content directly
    # We also set mode to 'detailed' and response-length to 'longer' for depth
    success, output = run_notebooklm_command(
        [
            "configure",
            "--notebook",
            notebook_id,
            "--persona",
            prompt,
            "--response-length",
            "longer",
        ]
    )

    if success:
        print(f"  ✅ Configuration successful")
        return True
    else:
        print(f"  ❌ Configuration failed: {output}", file=sys.stderr)
        return False

def main():
    """Main entry point"""
    if len(sys.argv) < 3:
        print("Usage: python upload.py <notebook_title> <pdf_file1> [pdf_file2] ...")
        print("       python upload.py <notebook_title> --json <json_file>")
        print("")
        print("The JSON file should contain output from download.py")
        sys.exit(1)

    # Check notebooklm is installed
    if not check_notebooklm_installed():
        print("❌ NotebookLM CLI not found!", file=sys.stderr)
        print("Install with: pip install notebooklm-py playwright")
        print("Then: playwright install chromium")
        print("Then authenticate with: notebooklm login")
        sys.exit(1)

    notebook_title = sys.argv[1]

    # Handle JSON input from download.py
    if sys.argv[2] == "--json":
        json_file = sys.argv[3]
        with open(json_file, "r") as f:
            data = json.load(f)
        files = data.get("files", [])
        temp_dir = data.get("output_dir")
        notebook_title = f"{data.get('stock_name', notebook_title)} 财务报告"
    else:
        files = sys.argv[2:]
        temp_dir = None

    if not files:
        print("❌ No files to upload", file=sys.stderr)
        sys.exit(1)

    print(f"📁 Files to upload: {len(files)}")

    # Create notebook
    notebook_id = create_notebook(notebook_title)
    if not notebook_id:
        sys.exit(1)

    # Upload all files
    results = upload_all_sources(notebook_id, files)

    # Summary
    print(f"\n{'=' * 50}")
    print(f"✅ Uploaded: {len(results['success'])} files")
    if results["failed"]:
        print(f"❌ Failed: {len(results['failed'])} files")
    print(f"📚 Notebook: {notebook_title}")
    print(f"🆔 ID: {notebook_id}")

    # Cleanup temp files
    if temp_dir:
        cleanup_temp_files(files, temp_dir)

    # Output JSON result
    result = {
        "notebook_id": notebook_id,
        "notebook_title": notebook_title,
        "uploaded": len(results["success"]),
        "failed": len(results["failed"]),
    }
    print("\n---JSON_OUTPUT---")
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
