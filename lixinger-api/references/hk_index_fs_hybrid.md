# API文档/香港/指数接口/财务报表/混合

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/hk/index/fs/hybrid
> API Key: `hk/index/fs/hybrid`

---

## 财报数据API

**简要描述:** 获取财务数据，如营业收入、ROE等。

**说明:**

- 指标计算请参考指数财务数据计算

**请求URL:** `https://open.lixinger.com/api/hk/index/fs/hybrid`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/hk/index/fs/hybrid](https://www.lixinger.com/api/open-api/html-doc/hk/index/fs/hybrid)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 指数代码数组。 stockCodes长度>=1且<=100，格式如下：["HSI"]。 请参考 指数信息API 获取合法的stockCode。 需要注意的是，当传入startDate时只能传入一个股票代码。 |
| date | No | String: latest \| YYYY-MM-DD (北京时间) | 信息日期。 用于获取指定日期数据。 由于每个季度的最后一天为财报日，请确保传入正确的日期，例如：2017-03-31、2017-06-30、2017-09-30、2017-12-31 或 latest。 其中，传入 **latest** 会得到最近1.1年内的最新财报数据。 需要注意的是，startDate和date至少要传一个。 |
| startDate | No | String: YYYY-MM-DD (北京时间) | 信息起始时间。 用于获取一定时间范围内的数据。 **开始和结束的时间间隔不超过10年** 需要注意的是，startDate和date至少要传一个。 |
| endDate | No | String: YYYY-MM-DD (北京时间) | 信息结束时间。 用于获取一定时间范围内的数据。 默认值是上周一。 需要注意的是，请与startDate一起使用。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[tableName].[fieldName].[expressionCalculateType]。 比如，你想获取营业总收入累计原始值以及应收账款当期同比值，对应的metricsList设置为：["q.ps.toi.t", "q.bs.ar.c_y2y"]。 需要注意的是，当stockCodes长度大于1时最多只能选取48个指标；当stockCodes长度等于1时最多只能获取128 个指标。 **当前支持:** granularity 年 : `y`; 半年 : `hy`; 季度 : `q` expressionCalculateType 资产负债表: 年(y): 当期 :t当期同比 :t_y2y当期环比 :t_c2c半年(hy): 当期 :t当期原始值 :t_o当期同比 :t_y2y当期环比 :t_c2c半年 :c半年原始值 :c_o半年同比 :c_y2y半年环比 :c_c2c季度(q): 当期 :t当期原始值 :t_o当期同比 :t_y2y当期环比 :t_c2c单季 :c单季原始值 :c_o单季同比 :c_y2y单季环比 :c_c2c; 利润表: 年(y): 累积 :t累积原始值 :t_o累积同比 :t_y2y半年(hy): 累积 :t累积原始值 :t_o累积同比 :t_y2y累积环比 :t_c2c半年 :c半年原始值 :c_o半年同比 :c_y2y半年环比 :c_c2c半年年比 :c_2yTTM :ttmTTM原始值 :ttm_oTTM同比 :ttm_y2yTTM环比 :ttm_c2c季度(q): 累积 :t累积原始值 :t_o累积同比 :t_y2y累积环比 :t_c2c单季 :c单季原始值 :c_o单季同比 :c_y2y单季环比 :c_c2c单季年比 :c_2yTTM :ttmTTM原始值 :ttm_oTTM同比 :ttm_y2yTTM环比 :ttm_c2c; 现金流量表: 年(y): 累积 :t累积原始值 :t_o累积同比 :t_y2y半年(hy): 累积 :t累积原始值 :t_o累积同比 :t_y2y累积环比 :t_c2c半年 :c半年原始值 :c_o半年同比 :c_y2y半年环比 :c_c2c半年年比 :c_2yTTM :ttmTTM原始值 :ttm_oTTM同比 :ttm_y2yTTM环比 :ttm_c2c季度(q): 累积 :t累积原始值 :t_o累积同比 :t_y2y累积环比 :t_c2c单季 :c单季原始值 :c_o单季同比 :c_y2y单季环比 :c_c2c单季年比 :c_2yTTM :ttmTTM原始值 :ttm_oTTM同比 :ttm_y2yTTM环比 :ttm_c2c tableName.fieldName 资产负债表 一、资产总计 : bs.ta物业、厂房及设备 : bs.ppe商誉及无形资产 : bs.gwaia(其中)商誉 : bs.gw(其中)无形资产 : bs.ia二、负债合计 : bs.tl资产负债率 : bs.tl_ta_r应交税费 : bs.tp递延所得税负债 : bs.ditl三、所有者权益合计 : bs.toe股东权益占比 : bs.toe_ta_r股本 : bs.sc股本溢价 : bs.spa其他权益工具 : bs.oei(其中)优先股 : bs.psioei(其中)永续债 : bs.pcsioei资本公积 : bs.capr减：库存股 : bs.is储备 : bs.r专项储备 : bs.rr其他储备 : bs.ors盈余公积 : bs.surr未分配利润 : bs.rtp股份奖励计划所持股份 : bs.shfsas可换股债券权益部分 : bs.ecocb归属于母公司股东及其他权益持有者的权益合计 : bs.tetshaoehopc归属于母公司普通股股东权益合计 : bs.tetoshopc少数股东权益 : bs.etmsh可赎回少数股东权益 : bs.rnci四、员工情况员工人数 : bs.ep_stn市值 : bs.mc总股本 : bs.tsc 利润表 一、营业收入 : ps.oi对联营企业及合营企业的投资收益 : ps.iifaajv(其中)对联营公司的投资收益 : ps.iifa(其中)对合营企业的投资收益 : ps.iifjv投资收益 : ps.ivi三、利润总额 : ps.tp减：所得税费用 : ps.ite有效税率 : ps.ite_tp_r四、净利润 : ps.np净利润率 : ps.np_s_r归属于母公司股东及其他权益持有者的净利润 : ps.npatshaoehopc归属于母公司普通股股东的净利润 : ps.npatoshopc少数股东损益 : ps.npatmsh可赎回少数股东权益利息及回购视同股利分配 : ps.adddicwrornci非国际公认会计准则净利润 : ps.nonifrs_op非国际公认会计准则归属于母公司股东净利润 : ps.nonifrs_opatoehopc七、分红、回购及涨跌幅分红金额 : ps.daH股分红金额 : ps.da_om回购金额 : ps.ra 现金流量表 经营活动产生的现金流量净额 : cfs.ncffoa投资活动产生的现金流量净额 : cfs.ncffia筹资活动产生的现金流量净额 : cfs.ncfffa现金及现金等价物的净增加额 : cfs.niicace期初现金及现金等价物的余额 : cfs.bocaceatpb汇率变动对现金及现金等价物的影响 : cfs.iocacedtfier期末现金及现金等价物净余额 : cfs.bocaceatpe 财务指标 一、人均指标员工人数 : m.ep_stn (expressionCalculateType参考资产负债表) 人均净利润 : m.np_pc (expressionCalculateType参考利润表) 二、每股指标总股本 : m.tsc (expressionCalculateType参考资产负债表) 归属于母公司普通股股东的每股收益 : m.npatoshopc_ps (expressionCalculateType参考利润表) 归属于母公司普通股股东的每股股东权益 : m.tetoshopc_ps (expressionCalculateType参考资产负债表) 每股经营活动产生的现金流量净额 : m.ncffoa_ps (expressionCalculateType参考现金流量表) 每股资本公积 : m.cr_ps (expressionCalculateType参考资产负债表) 每股未分配利润 : m.rp_ps (expressionCalculateType参考资产负债表) 每股分红 : m.da_ps (expressionCalculateType参考利润表) 三、盈利能力归属于少数股股东的ROE : m.roe_atomsh (expressionCalculateType参考利润表) 归属于母公司普通股股东的ROE : m.roe_atoshaopc (expressionCalculateType参考利润表) 净资产收益率(ROE) : m.roe (expressionCalculateType参考利润表) 杠杆倍数 : m.l (expressionCalculateType参考资产负债表) 总资产收益率(ROA) : m.roa (expressionCalculateType参考利润表) 总资产周转率 : m.ta_to (expressionCalculateType参考利润表) 净利润率 : m.np_s_r (expressionCalculateType参考利润表) 四、营运能力(周转率)不动产、厂房及设备周转率 : m.ppe_tor (expressionCalculateType参考利润表) 五、营运能力(周转天数)不动产、厂房及设备周转天数 : m.ppe_ds (expressionCalculateType参考利润表) 股东权益周转天数 : m.toe_ds (expressionCalculateType参考利润表) 总资产周转天数 : m.ta_ds (expressionCalculateType参考利润表) 六、偿债及资本结构资产负债率 : m.tl_ta_r (expressionCalculateType参考资产负债表) 七、现金流量经投融产生的现金流量净额 : m.ncffoaiafa (expressionCalculateType参考现金流量表) |

### 示例

```json
{
    "date": "2023-12-31",
    "stockCodes": [
        "HSI"
    ],
    "metricsList": [
        "q.ps.oi.t"
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
            "date": "2023-12-31T00:00:00+08:00",
            "currency": "HKD",
            "reportDate": "2025-03-31T00:00:00+08:00",
            "reportType": "annual_report",
            "standardDate": "2023-12-31T00:00:00+08:00",
            "q": {
                "ps": {
                    "oi": {
                        "t": 24045651758940
                    }
                }
            },
            "stockCode": "HSI"
        }
    ]
}
```
