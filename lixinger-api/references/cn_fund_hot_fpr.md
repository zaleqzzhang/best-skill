# 分红再投入收益率排名API

## 分红再投入收益率排名API

**简要描述:** 获取分红再投入收益率排名数据。

**请求URL:** `https://open.lixinger.com/api/cn/fund/hot/fpr`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/fund/hot/fpr](https://www.lixinger.com/api/open-api/html-doc/cn/fund/hot/fpr)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 基金代码数组。 stockCodes长度>=1且<=100，格式如下：["161725","005827"]。 请参考 基金信息API 获取合法的stockCode。 |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| stockCode | String | 股票代码 |
| last_data_date | Date | 数据时间 |
| f_p_r_fys_ssrp | Number | 同类型基金分红再投入收益率排名%(今年以来) |
| f_p_r_m1_ssrp | Number | 同类型基金分红再投入收益率排名%(1个月) |
| f_p_r_m3_ssrp | Number | 同类型基金分红再投入收益率排名%(3个月) |
| f_p_r_m6_ssrp | Number | 同类型基金分红再投入收益率排名%(6个月) |
| f_p_r_y1_ssrp | Number | 同类型基金分红再投入收益率排名%(1年) |
| f_p_r_y2_ssrp | Number | 同类型基金分红再投入收益率排名%(2年) |
| f_p_r_y3_ssrp | Number | 同类型基金分红再投入收益率排名%(3年) |
| f_p_r_y5_ssrp | Number | 同类型基金分红再投入收益率排名%(5年) |
| f_p_r_y10_ssrp | Number | 同类型基金分红再投入收益率排名%(10年) |
| f_cagr_p_r_fs_ssrp | Number | 同类型基金成立以来分红再投入年化收益率排名 |
| f_p_r_fys_ssc | Number | 同类型基金个数分红再投入收益率(今年以来) |
| f_p_r_m1_ssc | Number | 同类型基金个数分红再投入收益率(1个月) |
| f_p_r_m3_ssc | Number | 同类型基金个数分红再投入收益率(3个月) |
| f_p_r_m6_ssc | Number | 同类型基金个数分红再投入收益率(6个月) |
| f_p_r_y2_ssc | Number | 同类型基金个数分红再投入收益率(2年) |
| f_p_r_y3_ssc | Number | 同类型基金个数分红再投入收益率(3年) |
| f_p_r_y5_ssc | Number | 同类型基金个数分红再投入收益率(5年) |
| f_p_r_y10_ssc | Number | 同类型基金个数分红再投入收益率(10年) |
| f_cagr_p_r_fs_ssc | Number | 同类型基金个数分红再投入收益率(10年) |

### 示例

```json
{
    "stockCodes": [
        "161725",
        "005827"
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
            "type": "fpr",
            "f_p_r_fys_ssc": 5570,
            "f_p_r_fys_ssrp": 0.9504399353564374,
            "f_p_r_m1_ssc": 5708,
            "f_p_r_m1_ssrp": 0.7949886104783599,
            "f_p_r_m3_ssc": 5517,
            "f_p_r_m3_ssrp": 0.9873096446700508,
            "f_p_r_m6_ssc": 5215,
            "f_p_r_m6_ssrp": 0.9668200997314922,
            "f_p_r_y1_ssc": 4404,
            "f_p_r_y1_ssrp": 0.9995457642516467,
            "f_p_r_y2_ssc": 3385,
            "f_p_r_y2_ssrp": 0.999113475177305,
            "f_p_r_y3_ssc": 2811,
            "f_p_r_y3_ssrp": 0.9971530249110321,
            "f_p_r_y5_ssc": 1697,
            "f_p_r_y5_ssrp": 0.9716981132075472,
            "f_cagr_p_r_fs_ssc": 5717,
            "f_cagr_p_r_fs_ssrp": 0.4279216235129461,
            "f_p_r_y10_ssc": 516,
            "f_p_r_y10_ssrp": 0.06990291262135923,
            "stockCode": "161725"
        },
        {
            "type": "fpr",
            "f_p_r_fys_ssc": 9004,
            "f_p_r_fys_ssrp": 0.7467510829723426,
            "f_p_r_m1_ssc": 9164,
            "f_p_r_m1_ssrp": 0.5499290625341046,
            "f_p_r_m3_ssc": 8982,
            "f_p_r_m3_ssrp": 0.8775192072152321,
            "f_p_r_m6_ssc": 8747,
            "f_p_r_m6_ssrp": 0.909215641436085,
            "f_p_r_y1_ssc": 8329,
            "f_p_r_y1_ssrp": 0.9699807877041307,
            "f_p_r_y2_ssc": 7700,
            "f_p_r_y2_ssrp": 0.8750487076243668,
            "f_p_r_y3_ssc": 6833,
            "f_p_r_y3_ssrp": 0.9167154566744731,
            "f_p_r_y5_ssc": 4123,
            "f_p_r_y5_ssrp": 0.9454148471615721,
            "f_cagr_p_r_fs_ssc": 9051,
            "f_cagr_p_r_fs_ssrp": 0.3064088397790055,
            "stockCode": "005827"
        }
    ]
}
```
