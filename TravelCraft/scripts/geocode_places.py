#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TravelCraft v2.2 — 批量地理编码工具

用腾讯位置服务 WebService Geocoder API 把一组地点名称
转换为经纬度坐标，保存为 places.json。

Usage:
    python3 geocode_places.py \\
        --key WA6BZ-... \\
        --input places.txt \\
        --output places.json

places.txt 每行一个地点，可选加上"城市"提示：
    邯郸博物馆 | 邯郸
    响堂山石窟 | 邯郸
    龙门石窟 | 洛阳
"""
import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

GEOCODER_URL = "https://apis.map.qq.com/ws/geocoder/v1/"


def geocode(name, region, key):
    """地理编码：地名 → {lng, lat, formatted_address}"""
    # region 会被拼进 address，提高精度
    address = f"{region}{name}" if region else name
    params = {"address": address, "key": key}
    url = GEOCODER_URL + "?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read())
        if data.get("status") != 0:
            sys.stderr.write(f"[geocode] ✗ {name}: {data.get('message')}\n")
            return None
        r = data["result"]
        return {
            "name": name,
            "region": region,
            "lng": r["location"]["lng"],
            "lat": r["location"]["lat"],
            "address_title": r.get("title", ""),
            "province": r["address_components"].get("province", ""),
            "city": r["address_components"].get("city", ""),
            "district": r["address_components"].get("district", ""),
            "reliability": r.get("reliability", 0),
            "level": r.get("level", 0),
        }
    except Exception as e:
        sys.stderr.write(f"[geocode] ✗ {name}: {e}\n")
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", required=True, help="腾讯位置服务 Key")
    ap.add_argument("--input", "-i", required=True, help="输入文件：每行 '地名 | 城市'")
    ap.add_argument("--output", "-o", required=True, help="输出 JSON 文件")
    ap.add_argument("--qps", type=float, default=5,
                    help="每秒最多调用次数（默认 5，WebService 免费额度上限）")
    args = ap.parse_args()

    entries = []
    for line in Path(args.input).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "|" in line:
            name, region = [x.strip() for x in line.split("|", 1)]
        else:
            name, region = line, ""
        entries.append((name, region))

    results = []
    interval = 1.0 / args.qps
    for i, (name, region) in enumerate(entries):
        if i > 0:
            time.sleep(interval)
        r = geocode(name, region, args.key)
        if r:
            results.append(r)
            print(f"[geocode] ✓ {name} → ({r['lng']:.4f}, {r['lat']:.4f}) [{r['address_title'][:20]}]")
        else:
            results.append({"name": name, "region": region, "error": True})

    Path(args.output).write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    ok = sum(1 for r in results if "lng" in r)
    print(f"\n[geocode] Saved {ok}/{len(results)} successful → {args.output}")


if __name__ == "__main__":
    main()
