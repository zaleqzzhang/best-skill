#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TravelCraft v2.2 — 驾车路线校准工具

调用腾讯位置服务 WebService 驾车路线规划 API，
获取每段的真实距离、时长、折线坐标，并生成对比报告。

路线段定义（route.json 格式示例）：
{
  "key": "WA6BZ-...",   # 可不填，命令行 --key 覆盖
  "segments": [
    {
      "name": "北京→邯郸",
      "day": 1,
      "from": {"name": "北京西站", "lng": 116.32, "lat": 39.89},
      "to":   {"name": "邯郸博物馆", "lng": 114.54, "lat": 36.63},
      "waypoints": [],
      "estimated_hours": 5.0   # 行程草案中的估算
    },
    ...
  ]
}

输出：calibrated.json
每段新增：real_distance_km, real_duration_hours, polyline, deviation_percent
"""
import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROUTE_URL = "https://apis.map.qq.com/ws/direction/v1/driving/"


def call_driving_api(from_pt, to_pt, waypoints, key):
    """调用驾车路线规划 API"""
    params = {
        "from": f"{from_pt['lat']},{from_pt['lng']}",
        "to":   f"{to_pt['lat']},{to_pt['lng']}",
        "key":  key,
        "output": "json",
    }
    if waypoints:
        params["waypoints"] = ";".join(
            f"{w['lat']},{w['lng']}" for w in waypoints
        )
    url = ROUTE_URL + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=15) as resp:
        return json.loads(resp.read())


def decode_compressed_polyline(coords):
    """腾讯 API 返回的 polyline 是 [lat0, lng0, Δlat1, Δlng1, Δlat2, Δlng2, ...]
       用差分编码（除第一对），需要还原。"""
    if not coords or len(coords) < 2:
        return []
    pts = [(coords[0], coords[1])]
    for i in range(2, len(coords), 2):
        # 差值 * 1e6 后为整数，还原除以 1e6 并累加
        dlat = coords[i] / 1000000
        dlng = coords[i + 1] / 1000000
        last_lat, last_lng = pts[-1]
        pts.append((last_lat + dlat, last_lng + dlng))
    return pts


def calibrate_segment(seg, key, verbose=True):
    try:
        data = call_driving_api(seg["from"], seg["to"],
                                 seg.get("waypoints", []), key)
    except Exception as e:
        seg["error"] = f"API call failed: {e}"
        return seg

    if data.get("status") != 0:
        seg["error"] = data.get("message", "unknown error")
        if verbose:
            print(f"  ✗ {seg['name']}: {seg['error']}")
        return seg

    route = data["result"]["routes"][0]
    dist_km = route["distance"] / 1000
    dur_hours = route["duration"] / 60

    seg["real_distance_km"] = round(dist_km, 1)
    seg["real_duration_hours"] = round(dur_hours, 2)
    seg["polyline"] = decode_compressed_polyline(route.get("polyline", []))

    # 与估算对比
    est = seg.get("estimated_hours", 0)
    if est > 0:
        dev = (dur_hours - est) / est * 100
        seg["deviation_percent"] = round(dev, 1)
        flag = "⚠️ " if abs(dev) > 20 else "✓ "
    else:
        flag = "• "

    if verbose:
        est_str = f"原估 {est:.1f}h" if est > 0 else "无估算"
        print(f"  {flag}{seg['name']}: 实测 {dist_km:.1f}km / {dur_hours:.2f}h ({est_str})")
    return seg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", help="腾讯位置服务 Key（覆盖 route.json 中的 key）")
    ap.add_argument("--input", "-i", required=True, help="route.json")
    ap.add_argument("--output", "-o", required=True, help="calibrated.json")
    args = ap.parse_args()

    route = json.loads(Path(args.input).read_text(encoding="utf-8"))
    key = args.key or route.get("key")
    if not key:
        sys.exit("ERROR: no Key provided")

    print(f"[calibrate] {len(route['segments'])} 段路线校准中...")
    for i, seg in enumerate(route["segments"]):
        if i > 0:
            time.sleep(0.25)  # QPS 限流
        calibrate_segment(seg, key)

    Path(args.output).write_text(
        json.dumps(route, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # 打印汇总
    total_dist = sum(s.get("real_distance_km", 0) for s in route["segments"])
    total_hours = sum(s.get("real_duration_hours", 0) for s in route["segments"])
    print(f"\n[calibrate] 总里程 {total_dist:.1f} km / 总驾驶时间 {total_hours:.2f} h")
    print(f"[calibrate] Saved → {args.output}")


if __name__ == "__main__":
    main()
