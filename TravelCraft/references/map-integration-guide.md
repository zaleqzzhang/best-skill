# Phase 3.5 + 4.5 Map Integration Guide

> 适用于 TravelCraft v2.2+
> 本文档仅在 Phase 3.5（路线校准）或 Phase 4.5（地图嵌入）触发时读取。

## Why Tencent Location Service?

| 候选 | 优势 | 劣势 |
|------|------|------|
| 🏆 **腾讯位置服务** | 国内 CDN 快、免费额度足（10k/日）、支持境内外、与小红书同生态 | 仅中文地名优化 |
| 高德 Web API | 国内路况好 | 免费额度更严格（100/日） |
| 百度地图 | POI 数据全 | Key 审批慢 |
| Google Maps | 全球好 | 国内不可用 |

默认选腾讯位置服务。

## Key Setup (First-Time)

1. **Create Key**: https://lbs.qq.com/dev/console/key/add
   - Name: `TravelCraft`
   - Enable: ✅ WebServiceAPI（选"域名白名单"，白名单留空）
   - Don't enable: SDK / 微信小程序
2. **Allocate Quota**（⚠️ 容易漏的步骤）:
   - https://lbs.qq.com/dev/console/quota/manage
   - 把默认 10k/日 分配给 Key 的 geocoder + direction/driving
   - 新 Key 默认未分配，不分配会报 `status: 121`
3. **Save Key**:
   ```bash
   echo "TMAP_KEY=WA6BZ-XXXXX-XXXXX-XXXXX-XXXXX-XXXXX" >> ~/.codebuddy/skills/TravelCraft/data/.env
   ```

## Quota Budget（how many calls per trip）

| 阶段 | 消耗 | 典型 6 天行程 |
|------|------|--------------|
| 3.5.2 地理编码 | 1 次/地点 | 15-25 次 |
| 3.5.4 路线校准 | 1 次/段 | 5-8 次 |
| 4.5 地图嵌入 | 0（前端加载不计入 WebService）| — |
| 用户浏览行程 | 1 次 JS API 加载（另计额度） | 每次打开 1 次 |

→ **一次完整规划约 30 次调用，远低于 10k/日 上限**。

## API Endpoints Used

### Geocoder (地理编码)
```
GET https://apis.map.qq.com/ws/geocoder/v1/?address=<NAME>&key=<KEY>
```

Returns: `{lng, lat, reliability 0-10, level 0-11}`. We filter `reliability >= 7`.

### Driving Direction (驾车路线)
```
GET https://apis.map.qq.com/ws/direction/v1/driving/
    ?from=<lat,lng>&to=<lat,lng>[&waypoints=<lat,lng;lat,lng>]&key=<KEY>
```

Returns: `{distance_m, duration_min, polyline[lat0,lng0,Δlat,Δlng,...]}`.

Polyline 使用差分编码，见 `scripts/calibrate_route.py::decode_compressed_polyline`。

### JavaScript API GL (地图渲染)
```html
<script src="https://map.qq.com/api/gljs?v=1.exp&key=<KEY>"></script>
```

核心对象：`TMap.Map` / `TMap.MultiMarker` / `TMap.MultiPolyline` / `TMap.InfoWindow`。

### URI API (一键导航)
```
https://apis.map.qq.com/uri/v1/marker?marker=coord:<lat>,<lng>;title:<NAME>&referer=TravelCraft
https://apis.map.qq.com/uri/v1/routeplan?type=drive&from=<NAME>&fromcoord=<lat>,<lng>&to=<NAME>&tocoord=<lat>,<lng>&referer=TravelCraft
```

手机点击 → 自动唤起腾讯地图 APP 或落地页（未装 APP 时网页版）。

## Deviation Threshold Policy

| 偏差 | 处理 |
|------|------|
| ≤ ±10% | ✓ 绿色标识，无需调整 |
| ±10% ~ ±20% | • 灰色标识，告知用户但不打断 |
| > ±20% | ⚠️ 红色标识，**必须询问用户是否调整行程** |

偏差 > +30% 的段落，推荐在当天减少 1 个景点；偏差 > -30% 的段落，可以考虑加一个路过景点。

## Common Issues

### status: 121 "此 key 每日调用量已达到上限"
**原因**：新 Key 未在"配额管理"分配额度。
**解决**：访问 https://lbs.qq.com/dev/console/quota/manage 手动分配。

### status: 199 "此 key 未开启 webservice 功能"
**原因**：创建 Key 时未勾选 WebServiceAPI。
**解决**：编辑 Key，勾选 WebServiceAPI，保存。

### status: 311 "key 格式错误"
**原因**：Key 复制粘贴时带了空格/换行，或用了测试 Key。
**解决**：重新从控制台复制。

### JavaScript API 地图显示空白
**原因**：域名未在白名单（如果启用了白名单）。
**解决**：Key 白名单留空 OR 加入部署域名（`.edgeone.cool` / `.vercel.app` / 自定义域名）。

### 标注 marker 没显示
**原因**：`TMap.MultiMarker` 需要 `styles.default` 或匹配的 styleId。
**检查**：inject_tmap.py 模板已默认处理。

## Recipe: Manual Calibration

如果 Skill 自动流程失败，可手动完成：

```bash
cd /path/to/trip/
cat > places.txt <<EOF
A 地 | 北京
B 地 | 上海
EOF
python3 scripts/geocode_places.py --key $TMAP_KEY -i places.txt -o places.json

# 基于 places.json 手写 route.json 定义每段 from/to
python3 scripts/calibrate_route.py --key $TMAP_KEY -i route.json -o calibrated.json
python3 scripts/inject_tmap.py --html trip.html --route calibrated.json --key $TMAP_KEY -o trip.html
```

## Future Extensions (v2.3+ 规划)

- **实时路况**：调 `realtime` 参数，避开拥堵时段
- **天气融合**：叠加墨迹天气 API，行程前 3 天自动推送天气提醒
- **打卡记录**：用户扫码查看行程时记录位置，事后生成"实际走过的轨迹图"
- **高德+腾讯双地图**：让用户选择自己习惯的导航应用
