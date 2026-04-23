#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TravelCraft v2.2 — 腾讯地图嵌入工具（就地替换版）

把 calibrated.json 中的路线数据注入到现有 HTML：
  - 就地替换 <div class="route-map"><img .../></div>（Phase 4 模板产生的路线示意图）
    变成可交互的腾讯地图
  - 保留外层 .card 和 <h4>路线</h4> 标题的视觉一致性
  - 下方追加每日路线摘要卡片（里程 / 时长 / 偏差 / 一键导航）
  - 景点标注点击 → 弹出 infoWindow 带「导航到此」按钮（唤起腾讯地图 APP / H5）

如果 HTML 里没有 .route-map，则回退到在 <body> 顶部追加模式。

Usage:
    python3 inject_tmap.py \\
        --html index.html \\
        --route calibrated.json \\
        --key WA6BZ-... \\
        --output index-with-map.html \\
        [--mode replace|prepend]   # 默认 replace
"""
import argparse
import json
import re
from pathlib import Path


# -------- 地图容器 + 摘要卡片 HTML + CSS（就地替换模式）--------
MAP_BLOCK_TEMPLATE = r"""<style>
  .tc-tmap-wrap { width: 100%; margin: 8px 0 0; }
  #tc-tmap-container {
    width: 100%;
    height: 460px;
    background: #F5EFE6;
    border: 1px solid #E8DCC9;
    border-radius: var(--radius, 8px);
    overflow: hidden;
  }
  .tc-route-summary {
    margin-top: 14px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 10px;
    font-size: 13px;
  }
  .tc-route-card {
    padding: 10px 12px;
    background: #F5EFE6;
    border-left: 3px solid #B07B5F;
    border-radius: 4px;
  }
  .tc-route-card .day { font-weight: bold; color: #2C4A6E; font-size: 13px; }
  .tc-route-card .route { color: #333; margin: 3px 0; font-size: 12.5px; }
  .tc-route-card .stats { color: #666; font-size: 12px; }
  .tc-route-card .deviation {
    font-size: 11px;
    font-family: "Times New Roman", serif;
    margin-top: 2px;
  }
  .tc-route-card .deviation.ok { color: #5B7A5A; }
  .tc-route-card .deviation.high { color: #C0392B; }
  .tc-nav-btn {
    display: inline-block;
    padding: 4px 10px;
    background: #B07B5F;
    color: #FFF !important;
    font-size: 11px;
    text-decoration: none !important;
    letter-spacing: 2px;
    margin-top: 6px;
    border-radius: 3px;
  }
  .tc-nav-btn:hover { background: #9A6A50; }
  .tc-totals {
    text-align: center;
    margin-top: 12px;
    font-size: 12px;
    color: #999;
    font-family: "Times New Roman", "Songti SC", serif;
  }
  .tc-totals strong { color: #B07B5F; font-weight: bold; }
  @media (max-width: 640px) {
    #tc-tmap-container { height: 340px; }
  }
</style>
<div class="tc-tmap-wrap">
  <div id="tc-tmap-container"></div>
  <div class="tc-route-summary" id="tc-route-summary"></div>
  <div class="tc-totals">
    🚗 实测总里程 <strong>__TOTAL_DIST__</strong> km &nbsp;·&nbsp; ⏱ 总驾驶 <strong>__TOTAL_HOURS__</strong> h &nbsp;·&nbsp; 📍 <strong>__PLACE_COUNT__</strong> 个景点
  </div>
</div>
<script>
(function(){
  var ROUTE_DATA = __ROUTE_JSON__;
  var TMAP_KEY = "__TMAP_KEY__";
  var DAY_COLORS = ['#B07B5F', '#2C4A6E', '#5B7A5A', '#8E6C88', '#C99C5C', '#3D6A6A'];

  // ① 动态加载 TMap SDK（兼容密码门 document.write 后的环境）
  function loadTMap(cb){
    if (window.TMap && window.TMap.Map) { cb(); return; }
    var existing = document.querySelector('script[data-tc-tmap]');
    if (existing) {
      var poll = setInterval(function(){
        if (window.TMap && window.TMap.Map){ clearInterval(poll); cb(); }
      }, 100);
      return;
    }
    var s = document.createElement('script');
    s.src = 'https://map.qq.com/api/gljs?v=1.exp&key=' + TMAP_KEY;
    s.setAttribute('data-tc-tmap', '1');
    s.async = true;
    s.onload = function(){
      var poll = setInterval(function(){
        if (window.TMap && window.TMap.Map){ clearInterval(poll); cb(); }
      }, 100);
    };
    s.onerror = function(){
      var box = document.getElementById('tc-tmap-container');
      if (box) box.innerHTML = '<div style="padding:40px;text-align:center;color:#C0392B;">地图 SDK 加载失败<br>请检查网络或稍后刷新</div>';
    };
    document.head.appendChild(s);
  }

  // ② 等容器在 DOM 中出现再初始化
  function whenReady(cb, tries){
    tries = tries || 0;
    var el = document.getElementById('tc-tmap-container');
    if (el && el.offsetWidth > 0){ cb(); return; }
    if (tries > 40){ return; }
    setTimeout(function(){ whenReady(cb, tries+1); }, 100);
  }

  function initMap(){
    var container = document.getElementById('tc-tmap-container');
    if (!container) return;
    if (!ROUTE_DATA.segments || ROUTE_DATA.segments.length === 0){
      container.innerHTML = '<div style="padding:40px;text-align:center;color:#999;">暂无驾车路线</div>';
      return;
    }

    // 计算中心点
    var allLats = [], allLngs = [];
    ROUTE_DATA.segments.forEach(function(seg){
      if (seg.polyline && seg.polyline.length){
        seg.polyline.forEach(function(p){ allLats.push(p[0]); allLngs.push(p[1]); });
      } else {
        if (seg.from){ allLats.push(seg.from.lat); allLngs.push(seg.from.lng); }
        if (seg.to){ allLats.push(seg.to.lat); allLngs.push(seg.to.lng); }
      }
    });
    var centerLat = allLats.reduce(function(a,b){return a+b;},0) / allLats.length;
    var centerLng = allLngs.reduce(function(a,b){return a+b;},0) / allLngs.length;

    var map = new TMap.Map(container, {
      center: new TMap.LatLng(centerLat, centerLng),
      zoom: 8,
      viewMode: '2D',
      showControl: true,
      baseMap: { type: 'vector', features: ['base', 'building2d', 'point', 'label'] }
    });

    var bounds = new TMap.LatLngBounds();

    // 绘制每段路线
    ROUTE_DATA.segments.forEach(function(seg, idx){
      var color = DAY_COLORS[idx % DAY_COLORS.length];
      if (seg.polyline && seg.polyline.length > 1){
        var path = seg.polyline.map(function(p){ return new TMap.LatLng(p[0], p[1]); });
        new TMap.MultiPolyline({
          map: map,
          styles: {
            ds: new TMap.PolylineStyle({
              color: color, width: 5,
              borderWidth: 1, borderColor: '#FFFFFF',
              lineCap: 'round'
            })
          },
          geometries: [{ id: 'seg_'+idx, styleId: 'ds', paths: path }]
        });
        path.forEach(function(ll){ bounds.extend(ll); });
      }
    });

    // 去重收集所有景点
    var placeMap = {};
    ROUTE_DATA.segments.forEach(function(seg){
      [seg.from, seg.to].concat(seg.waypoints || []).forEach(function(p){
        if (!p || p.lng == null) return;
        var k = p.lng.toFixed(4) + ',' + p.lat.toFixed(4);
        if (!placeMap[k]){
          placeMap[k] = { name: p.name, lng: p.lng, lat: p.lat, day: seg.day };
        }
      });
    });

    var markerGeoms = [];
    Object.keys(placeMap).forEach(function(k, i){
      var p = placeMap[k];
      markerGeoms.push({
        id: 'm'+i,
        position: new TMap.LatLng(p.lat, p.lng),
        properties: { title: p.name, day: p.day, lng: p.lng, lat: p.lat }
      });
      bounds.extend(new TMap.LatLng(p.lat, p.lng));
    });

    var marker = new TMap.MultiMarker({
      map: map,
      styles: {
        default: new TMap.MarkerStyle({
          width: 28, height: 36,
          anchor: { x: 14, y: 36 }
        })
      },
      geometries: markerGeoms
    });

    var infoWin = new TMap.InfoWindow({
      map: map,
      position: new TMap.LatLng(centerLat, centerLng),
      content: '',
      offset: { x: 0, y: -32 }
    });
    infoWin.close();

    marker.on('click', function(evt){
      var p = evt.geometry.properties;
      var navUrl = 'https://apis.map.qq.com/uri/v1/marker?marker=coord:' + p.lat + ',' + p.lng + ';title:' + encodeURIComponent(p.title) + ';addr:&referer=TravelCraft';
      infoWin.setPosition(evt.geometry.position);
      infoWin.setContent(
        '<div style="font-family:Songti SC,serif;padding:6px 10px;min-width:140px;">' +
          '<div style="font-size:14px;font-weight:bold;color:#333;margin-bottom:2px;">' + p.title + '</div>' +
          '<div style="font-size:11px;color:#999;margin-bottom:8px;">Day ' + p.day + '</div>' +
          '<a class="tc-nav-btn" href="' + navUrl + '" target="_blank" style="display:inline-block;padding:4px 10px;background:#B07B5F;color:#FFF;font-size:11px;text-decoration:none;border-radius:3px;">🚗 导航到此</a>' +
        '</div>'
      );
      infoWin.open();
    });

    setTimeout(function(){
      if (!bounds.isEmpty()){
        map.fitBounds(bounds, { padding: { top: 40, bottom: 40, left: 40, right: 40 }});
      }
    }, 300);

    // 渲染每日摘要卡片
    var summaryEl = document.getElementById('tc-route-summary');
    if (!summaryEl) return;
    summaryEl.innerHTML = ROUTE_DATA.segments.map(function(seg, idx){
      var color = DAY_COLORS[idx % DAY_COLORS.length];
      var dist = seg.real_distance_km != null ? seg.real_distance_km : '—';
      var dur = seg.real_duration_hours != null ? seg.real_duration_hours.toFixed(1) + 'h' : '—';
      var devHtml = '';
      if (seg.deviation_percent != null){
        var absDev = Math.abs(seg.deviation_percent);
        var klass = absDev > 20 ? 'high' : 'ok';
        var icon = absDev > 20 ? '⚠️' : '✓';
        var sign = seg.deviation_percent >= 0 ? '+' : '';
        devHtml = '<div class="deviation ' + klass + '">' + icon + ' 估算偏差 ' + sign + seg.deviation_percent + '%</div>';
      }
      var navFrom = 'https://apis.map.qq.com/uri/v1/routeplan?type=drive&from=' + encodeURIComponent(seg.from.name) + '&fromcoord=' + seg.from.lat + ',' + seg.from.lng + '&to=' + encodeURIComponent(seg.to.name) + '&tocoord=' + seg.to.lat + ',' + seg.to.lng + '&referer=TravelCraft';
      return (
        '<div class="tc-route-card" style="border-left-color:' + color + ';">' +
          '<div class="day">Day ' + seg.day + ' · ' + (seg.name || '') + '</div>' +
          '<div class="route">' + seg.from.name + ' → ' + seg.to.name + '</div>' +
          '<div class="stats">🚗 ' + dist + ' km · ⏱ ' + dur + '</div>' +
          devHtml +
          '<a class="tc-nav-btn" href="' + navFrom + '" target="_blank">一键导航</a>' +
        '</div>'
      );
    }).join('');
  }

  function boot(){
    whenReady(function(){
      loadTMap(initMap);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
</script>"""


def inject(html, route, key, mode="replace"):
    total_dist = sum(s.get("real_distance_km", 0) for s in route["segments"])
    total_hours = sum(s.get("real_duration_hours", 0) for s in route["segments"])

    # 收集唯一景点数量
    unique = set()
    for s in route["segments"]:
        for p in [s["from"], s["to"]] + s.get("waypoints", []):
            if p and p.get("lng") is not None:
                unique.add((round(p["lng"], 4), round(p["lat"], 4)))

    compact = {"segments": []}
    for s in route["segments"]:
        compact["segments"].append({
            "day": s.get("day"),
            "name": s.get("name"),
            "from": s["from"],
            "to": s["to"],
            "waypoints": s.get("waypoints", []),
            "polyline": s.get("polyline", []),
            "real_distance_km": s.get("real_distance_km"),
            "real_duration_hours": s.get("real_duration_hours"),
            "deviation_percent": s.get("deviation_percent"),
        })

    block = (MAP_BLOCK_TEMPLATE
             .replace("__TMAP_KEY__", key)
             .replace("__ROUTE_JSON__", json.dumps(compact, ensure_ascii=False))
             .replace("__TOTAL_DIST__", f"{total_dist:.0f}")
             .replace("__TOTAL_HOURS__", f"{total_hours:.1f}")
             .replace("__PLACE_COUNT__", str(len(unique))))

    if mode == "replace":
        # 就地替换 <div class="route-map">...</div>
        pattern = re.compile(r'<div class="route-map">.*?</div>', re.DOTALL)
        m = pattern.search(html)
        if m:
            new_html = html[:m.start()] + block + html[m.end():]
            print(f"[inject_tmap] 就地替换 .route-map ({m.end()-m.start()} bytes → {len(block)} bytes)")
            return new_html
        print("[inject_tmap] ⚠️  未找到 .route-map 元素，回退到 prepend 模式")
        mode = "prepend"

    if mode == "prepend":
        m = re.search(r"<body[^>]*>", html, re.IGNORECASE)
        if m:
            idx = m.end()
            return html[:idx] + block + html[idx:]
        return html + block

    return html


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True)
    ap.add_argument("--route", required=True)
    ap.add_argument("--key", required=True)
    ap.add_argument("--output", "-o", required=True)
    ap.add_argument("--mode", choices=["replace", "prepend"], default="replace")
    args = ap.parse_args()

    html = Path(args.html).read_text(encoding="utf-8")
    route = json.loads(Path(args.route).read_text(encoding="utf-8"))

    new_html = inject(html, route, args.key, args.mode)
    Path(args.output).write_text(new_html, encoding="utf-8")
    print(f"[inject_tmap] saved → {args.output}")


if __name__ == "__main__":
    main()
