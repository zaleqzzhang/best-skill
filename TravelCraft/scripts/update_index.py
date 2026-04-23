#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TravelCraft v2.0 — Update the travel bookshelf index.

1. Appends a trip entry to data/trips.json (or updates existing by id)
2. Renders data/trips.json -> assets/index-template/index.html via Jinja2
3. Writes final index to OUTPUT_DIR (ready for deployment)

Usage:
    python3 update_index.py \\
        --slug henan-culture-2026-05 \\
        --title "河南文化自驾" \\
        --date-range "2026-05-01 ~ 2026-05-06" \\
        --days 6 \\
        --people 3 \\
        --theme "文化" \\
        --cover photos/longshan.jpg \\
        --url-eop https://... \\
        --url-vercel https://... \\
        --password-protected \\
        --output-dir ./bookshelf-build
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
except ImportError:
    sys.stderr.write("[update_index] missing deps. run: pip3 install jinja2\n")
    sys.exit(1)

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR / "data"
TEMPLATE_DIR = SKILL_DIR / "assets" / "index-template"
TRIPS_JSON = DATA_DIR / "trips.json"


def load_trips():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if TRIPS_JSON.exists():
        try:
            return json.loads(TRIPS_JSON.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"trips": []}


def save_trips(data):
    TRIPS_JSON.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def upsert_trip(data, entry):
    trips = data.setdefault("trips", [])
    for i, t in enumerate(trips):
        if t.get("id") == entry["id"]:
            trips[i] = entry
            return data
    trips.append(entry)
    return data


def render_index(data, output_dir: Path):
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=select_autoescape(["html"]),
    )
    tpl = env.get_template("index.html")

    # Sort by created_at desc
    trips = sorted(
        data.get("trips", []),
        key=lambda t: t.get("created_at", ""),
        reverse=True,
    )

    # Group by year
    grouped = {}
    for t in trips:
        year = t.get("created_at", "")[:4] or "未分组"
        grouped.setdefault(year, []).append(t)

    rendered = tpl.render(
        trips=trips,
        grouped=grouped,
        total=len(trips),
        latest_date=trips[0]["created_at"][:10] if trips else "",
        generated_at=dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "index.html").write_text(rendered, encoding="utf-8")
    print(f"[update_index] rendered → {output_dir / 'index.html'}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True, help="Unique trip id (URL-safe)")
    ap.add_argument("--title", required=True)
    ap.add_argument("--date-range", dest="date_range", default="")
    ap.add_argument("--days", type=int, default=0)
    ap.add_argument("--people", type=int, default=0)
    ap.add_argument("--theme", default="")
    ap.add_argument("--cover", default="", help="Cover image path or URL")
    ap.add_argument("--url-eop", dest="url_eop", default="")
    ap.add_argument("--url-vercel", dest="url_vercel", default="")
    ap.add_argument("--url-github", dest="url_github", default="",
                    help="GitHub + jsDelivr URL (国内推荐)")
    ap.add_argument("--password-protected", dest="has_password",
                    action="store_true")
    ap.add_argument("--output-dir", dest="output_dir",
                    default="./bookshelf-build")
    args = ap.parse_args()

    entry = {
        "id": args.slug,
        "title": args.title,
        "date_range": args.date_range,
        "days": args.days,
        "people": args.people,
        "theme": args.theme,
        "has_password": args.has_password,
        "cover_image": args.cover,
        "urls": {
            "github": args.url_github,
            "eop": args.url_eop,
            "vercel": args.url_vercel,
        },
        "primary_url": args.url_github or args.url_eop or args.url_vercel,
        "created_at": dt.datetime.now().isoformat(timespec="seconds"),
    }

    data = load_trips()
    upsert_trip(data, entry)
    save_trips(data)
    print(f"[update_index] trips.json now has {len(data['trips'])} entries")

    render_index(data, Path(args.output_dir))
    print("[update_index] done. deploy the output dir to your 'my-travelcraft' project.")


if __name__ == "__main__":
    main()
