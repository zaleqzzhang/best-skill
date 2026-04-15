# API文档/大陆/基金接口/基金经理接口/热度数据/基金经理收益率

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/fund-manager/hot/fmp
> API Key: `cn/fund-manager/hot/fmp`

---

## 基金经理收益率API

**简要描述:** 获取基金经理收益率数据。

**请求URL:** `https://open.lixinger.com/api/cn/fund-manager/hot/fmp`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/fund-manager/hot/fmp](https://www.lixinger.com/api/open-api/html-doc/cn/fund-manager/hot/fmp)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 基金经理代码数组。 stockCodes长度>=1且<=100，格式如下：["8801388323","8801372475"]。 请参考 基金信息API 获取合法的stockCode。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| stockCode | String | 股票代码 |
| fm_p_r_d | Date | 最新收益率时间 |
| fm_p_r_fys | Number | 今年以来收益率 |
| fm_p_r_m1 | Number | 一个月收益率 |
| fm_p_r_m3 | Number | 三个月收益率 |
| fm_p_r_m6 | Number | 六个月收益率 |
| fm_p_r_y1 | Number | 一年收益率 |
| fm_p_r_y3 | Number | 三年收益率 |
| fm_p_r_y5 | Number | 五年收益率 |
| fm_p_r_y10 | Number | 十年收益率 |
| fm_cagr_p_r_fs | Number | 管理基金以来年化收益率 |
| fm_p_r_fys_rp | Number | 相同基金经理类型今年以来收益率排名 |
| fm_p_r_m1_rp | Number | 相同基金经理类型一个月收益率排名 |
| fm_p_r_m3_rp | Number | 相同基金经理类型三个月收益率排名 |
| fm_p_r_m6_rp | Number | 相同基金经理类型六个月收益率排名 |
| fm_p_r_y1_rp | Number | 相同基金经理类型一年收益率排名 |
| fm_p_r_y3_rp | Number | 相同基金经理类型三年收益率排名 |
| fm_p_r_y5_rp | Number | 相同基金经理类型五年收益率排名 |
| fm_p_r_y10_rp | Number | 相同基金经理类型十年收益率排名 |
| fm_cagr_p_r_fs_rp | Number | 相同基金经理类型管理基金以来年化收益率排名 |

### 示例

```json
{
    "stockCodes": [
        "8801388323",
        "8801372475"
    ],
    "token": "***********"
}
```

### 返回结果

```json
{
    "code": 1,
    "message": "success",
    "data": [
        {
            "type": "fmp",
            "fm_p_r_d": "2024-07-23T00:00:00+08:00",
            "fm_p_r_fys": -0.07814271919787852,
            "fm_p_r_m1": -0.070751205601289,
            "fm_p_r_m3": -0.00647597683396306,
            "fm_p_r_m6": 0.08178737716082862,
            "fm_p_r_y1": -0.11375853036459838,
            "fm_p_r_y3": -0.005146128019615448,
            "fm_p_r_y5": 0.89304113195063,
            "fm_cagr_p_r_fs": 0.19601427446086217,
            "fm_cagr_p_r_fs_m": 0.007129851533267173,
            "fm_cagr_p_r_fs_r_c": 1662,
            "fm_cagr_p_r_fs_rp": 0.001806140878988561,
            "fm_p_r_fys_m": -0.05512574202364218,
            "fm_p_r_fys_r_c": 1567,
            "fm_p_r_fys_rp": 0.5893997445721584,
            "fm_p_r_m1_m": -0.039971526343316355,
            "fm_p_r_m1_r_c": 1650,
            "fm_p_r_m1_rp": 0.881746513038205,
            "fm_p_r_m3_m": -0.0256994556272937,
            "fm_p_r_m3_r_c": 1625,
            "fm_p_r_m3_rp": 0.3232758620689655,
            "fm_p_r_m6_m": 0.02223334774589003,
            "fm_p_r_m6_r_c": 1586,
            "fm_p_r_m6_rp": 0.19873817034700317,
            "fm_p_r_y1_m": -0.13759946867221168,
            "fm_p_r_y1_r_c": 1466,
            "fm_p_r_y1_rp": 0.4225255972696246,
            "fm_p_r_y3_m": -0.323024914817268,
            "fm_p_r_y3_r_c": 1055,
            "fm_p_r_y3_rp": 0.10341555977229601,
            "fm_p_r_y5_m": 0.20509730442587748,
            "fm_p_r_y5_r_c": 754,
            "fm_p_r_y5_rp": 0.05444887118193891,
            "stockCode": "8801388323"
        },
        {
            "type": "fmp",
            "fm_p_r_d": "2026-03-19T00:00:00+08:00",
            "fm_p_r_m1": -0.03564082383442879,
            "fm_p_r_m3": -0.03626846356594238,
            "fm_p_r_m6": -0.09234219718217729,
            "fm_p_r_y1": -0.035554842800971986,
            "fm_p_r_y3": -0.08069346076959016,
            "fm_p_r_y5": -0.3246524389370188,
            "fm_p_r_y10": 1.0554424071948723,
            "fm_cagr_p_r_fs": 0.08431169058638854,
            "fm_cagr_p_r_fs_m": 0.07285370674764913,
            "fm_cagr_p_r_fs_r_c": 1751,
            "fm_cagr_p_r_fs_rp": 0.4308571428571429,
            "fm_p_r_fys_m": 0.014029037126290334,
            "fm_p_r_fys_r_c": 1665,
            "fm_p_r_fys_rp": 0.7620192307692307,
            "fm_p_r_m1_m": -0.03189919049529877,
            "fm_p_r_m1_r_c": 1707,
            "fm_p_r_m1_rp": 0.5439624853458382,
            "fm_p_r_m3_m": 0.03025685691625113,
            "fm_p_r_m3_r_c": 1656,
            "fm_p_r_m3_rp": 0.8918429003021148,
            "fm_p_r_m6_m": 0.033077741446893905,
            "fm_p_r_m6_r_c": 1601,
            "fm_p_r_m6_rp": 0.9,
            "fm_p_r_y10_m": 1.1002543137616247,
            "fm_p_r_y10_r_c": 271,
            "fm_p_r_y10_rp": 0.5185185185185185,
            "fm_p_r_y1_m": 0.19748484263221966,
            "fm_p_r_y1_r_c": 1504,
            "fm_p_r_y1_rp": 0.9640718562874252,
            "fm_p_r_y3_m": 0.18025096157214848,
            "fm_p_r_y3_r_c": 1110,
            "fm_p_r_y3_rp": 0.890892696122633,
            "fm_p_r_y5_m": 0.09759329400782923,
            "fm_p_r_y5_r_c": 757,
            "fm_p_r_y5_rp": 0.9444444444444444,
            "fm_p_r_fys": -0.014863372956966714,
            "stockCode": "8801372475"
        }
    ]
}
```
