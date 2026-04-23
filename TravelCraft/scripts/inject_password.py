#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TravelCraft v2.0 — AES-256 encrypt an HTML file and wrap with a password gate.

The output is a fully static HTML page that:
  1. Shows a password input form (宋式美学: 月白底 + 赭石按钮)
  2. On submit: derives key via PBKDF2(password, salt, 10000 iterations)
  3. Decrypts ciphertext locally via crypto-js (AES-CBC)
  4. Replaces document content with decrypted HTML
  5. Wrong password: shows "密码错误" with shake animation

Security level: suitable for family / friends privacy (casual).
NOT for regulatory-grade secrets.

Usage:
    python3 inject_password.py --input trip.html --password hn2026 --output trip.html
"""
import argparse
import base64
import hashlib
import json
import os
import sys
from pathlib import Path

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives import padding
    from cryptography.hazmat.backends import default_backend
except ImportError:
    sys.stderr.write(
        "[inject_password] missing deps. run: pip3 install cryptography\n"
    )
    sys.exit(1)


GATE_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · 行迹 · TravelCraft</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.2.0/crypto-js.min.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: "Songti SC", "STSong", "SimSun", serif;
    background: #F5EFE6;
    min-height: 100vh;
    display: flex; align-items: center; justify-content: center;
    padding: 20px;
    color: #333;
  }}
  .gate {{
    background: #FFF;
    padding: 40px 32px;
    max-width: 380px; width: 100%;
    border: 1px solid #E8DCC9;
    box-shadow: 0 8px 32px rgba(176, 123, 95, 0.12);
    text-align: center;
  }}
  .brand {{
    font-size: 32px; color: #B07B5F; font-weight: bold;
    letter-spacing: 8px; margin-bottom: 4px;
  }}
  .subtitle {{
    font-size: 12px; color: #999; letter-spacing: 2px;
    margin-bottom: 32px; font-family: "Times New Roman", serif;
    font-style: italic;
  }}
  .ornament {{
    width: 60px; height: 2px; background: #B07B5F;
    margin: 0 auto 32px; position: relative;
  }}
  .ornament::before, .ornament::after {{
    content: ""; position: absolute; top: -2px;
    width: 6px; height: 6px; background: #B07B5F;
    border-radius: 50%;
  }}
  .ornament::before {{ left: -10px; }}
  .ornament::after {{ right: -10px; }}
  h1 {{
    font-size: 20px; color: #2C4A6E; margin-bottom: 12px;
  }}
  .hint {{
    font-size: 13px; color: #999; margin-bottom: 28px;
    line-height: 1.6;
  }}
  input[type="password"] {{
    width: 100%; padding: 12px 16px;
    border: 1px solid #DDD; background: #FAFAF5;
    font-size: 16px; font-family: inherit;
    margin-bottom: 20px; text-align: center;
    letter-spacing: 4px;
    transition: border-color 0.2s;
  }}
  input[type="password"]:focus {{
    outline: none; border-color: #B07B5F;
  }}
  button {{
    width: 100%; padding: 12px;
    background: #B07B5F; color: #FFF;
    border: none; font-size: 15px; font-family: inherit;
    letter-spacing: 8px; cursor: pointer;
    transition: background 0.2s;
  }}
  button:hover {{ background: #9A6A50; }}
  .error {{
    color: #C0392B; font-size: 13px;
    margin-top: 12px; min-height: 18px;
  }}
  .shake {{ animation: shake 0.4s; }}
  @keyframes shake {{
    0%, 100% {{ transform: translateX(0); }}
    25% {{ transform: translateX(-8px); }}
    75% {{ transform: translateX(8px); }}
  }}
  .footer {{
    margin-top: 32px; font-size: 11px; color: #BBB;
  }}
</style>
</head>
<body>
<div class="gate" id="gate">
  <div class="brand">行 迹</div>
  <div class="subtitle">TravelCraft</div>
  <div class="ornament"></div>
  <h1>🔒  受保护的行程</h1>
  <div class="hint">请输入密码查看完整行程<br>（向行程分享者索取）</div>
  <form id="unlock">
    <input type="password" id="pwd" placeholder="••••" autocomplete="off" autofocus>
    <button type="submit">解 锁</button>
    <div class="error" id="err"></div>
  </form>
  <div class="footer">v2.0 · 行迹 TravelCraft</div>
</div>

<script>
(function () {{
  const PAYLOAD = {payload_json};

  document.getElementById('unlock').addEventListener('submit', function (e) {{
    e.preventDefault();
    const pwd = document.getElementById('pwd').value;
    const errEl = document.getElementById('err');
    const gate = document.getElementById('gate');
    errEl.textContent = '';

    try {{
      const salt = CryptoJS.enc.Base64.parse(PAYLOAD.salt);
      const iv = CryptoJS.enc.Base64.parse(PAYLOAD.iv);
      const ct = CryptoJS.enc.Base64.parse(PAYLOAD.ct);
      const key = CryptoJS.PBKDF2(pwd, salt, {{
        keySize: 256 / 32, iterations: 10000, hasher: CryptoJS.algo.SHA256
      }});
      const decrypted = CryptoJS.AES.decrypt(
        {{ ciphertext: ct }}, key,
        {{ iv: iv, mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.Pkcs7 }}
      );
      const html = decrypted.toString(CryptoJS.enc.Utf8);
      if (!html || html.indexOf('<') === -1) throw new Error('invalid');

      // Replace page content with decrypted HTML
      document.open();
      document.write(html);
      document.close();
    }} catch (ex) {{
      errEl.textContent = '密码错误，请重试';
      gate.classList.remove('shake');
      void gate.offsetWidth;
      gate.classList.add('shake');
      document.getElementById('pwd').value = '';
    }}
  }});
}})();
</script>
</body>
</html>
"""


def encrypt_html(plain_html: str, password: str) -> dict:
    """AES-256-CBC + PBKDF2-SHA256. Returns base64 fields."""
    salt = os.urandom(16)
    iv = os.urandom(16)
    # PBKDF2(password, salt, 10000 iter, sha256) -> 32 bytes
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"),
                              salt, 10000, dklen=32)

    padder = padding.PKCS7(128).padder()
    padded = padder.update(plain_html.encode("utf-8")) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded) + encryptor.finalize()

    return {
        "salt": base64.b64encode(salt).decode("ascii"),
        "iv": base64.b64encode(iv).decode("ascii"),
        "ct": base64.b64encode(ct).decode("ascii"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", "-i", required=True, help="HTML file to protect")
    ap.add_argument("--password", "-p", required=True, help="Password (≥4 chars)")
    ap.add_argument("--output", "-o", required=True, help="Output file path")
    ap.add_argument("--title", default="行程", help="Page title shown on gate")
    args = ap.parse_args()

    if len(args.password) < 4:
        ap.error("password must be at least 4 characters")

    src = Path(args.input)
    if not src.exists():
        ap.error(f"input not found: {src}")

    plain = src.read_text(encoding="utf-8")
    payload = encrypt_html(plain, args.password)

    html = GATE_TEMPLATE.format(
        title=args.title,
        payload_json=json.dumps(payload),
    )

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"[inject_password] protected → {out}  ({len(html)} bytes)")
    print(f"[inject_password] original size: {len(plain)}, encrypted size: {len(payload['ct'])}")


if __name__ == "__main__":
    main()
