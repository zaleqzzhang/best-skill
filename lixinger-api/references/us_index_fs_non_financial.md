# API文档/美国/指数接口/财务报表/非金融

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/us/index/fs/non_financial
> API Key: `us/index/fs/non_financial`

---

## 财报数据API

**简要描述:** 获取财务数据，如营业收入、ROE等。

**说明:**

- 指标计算请参考指数财务数据计算

**请求URL:** `https://open.lixinger.com/api/us/index/fs/non_financial`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/us/index/fs/non_financial](https://www.lixinger.com/api/open-api/html-doc/us/index/fs/non_financial)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 指数代码数组。 stockCodes长度>=1且<=100，格式如下：[".INX"]。 请参考 指数信息API 获取合法的stockCode。 需要注意的是，当传入startDate时只能传入一个股票代码。 |
| date | No | String: latest \| YYYY-MM-DD (北京时间) | 信息日期。 用于获取指定日期数据。 由于每个季度的最后一天为财报日，请确保传入正确的日期，例如：2017-03-31、2017-06-30、2017-09-30、2017-12-31 或 latest。 其中，传入 **latest** 会得到最近1.1年内的最新财报数据。 需要注意的是，startDate和date至少要传一个。 |
| startDate | No | String: YYYY-MM-DD (北京时间) | 信息起始时间。 用于获取一定时间范围内的数据。 **开始和结束的时间间隔不超过10年** 需要注意的是，startDate和date至少要传一个。 |
| endDate | No | String: YYYY-MM-DD (北京时间) | 信息结束时间。 用于获取一定时间范围内的数据。 默认值是上周一。 需要注意的是，请与startDate一起使用。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[tableName].[fieldName].[expressionCalculateType]。 比如，你想获取营业总收入累计原始值以及应收账款当期同比值，对应的metricsList设置为：["q.ps.toi.t", "q.bs.ar.c_y2y"]。 需要注意的是，当stockCodes长度大于1时最多只能选取48个指标；当stockCodes长度等于1时最多只能获取128 个指标。 **当前支持:** granularity 年 : `y`; 半年 : `hy`; 季度 : `q` expressionCalculateType 资产负债表: 年(y): 当期 :t当期同比 :t_y2yTTM环比 :ttm_c2c半年(hy): 当期 :t当期原始值 :t_o当期同比 :t_y2y当期环比 :t_c2c半年 :c半年原始值 :c_o半年同比 :c_y2y半年环比 :c_c2c季度(q): 当期 :t当期原始值 :t_o当期同比 :t_y2y当期环比 :t_c2c单季 :c单季原始值 :c_o单季同比 :c_y2y单季环比 :c_c2c; 利润表: 年(y): 累积 :t累积原始值 :t_o累积同比 :t_y2y半年(hy): 累积 :t累积原始值 :t_o累积同比 :t_y2y累积环比 :t_c2c半年 :c半年原始值 :c_o半年同比 :c_y2y半年环比 :c_c2c半年年比 :c_2yTTM :ttmTTM原始值 :ttm_oTTM同比 :ttm_y2yTTM环比 :ttm_c2c季度(q): 累积 :t累积原始值 :t_o累积同比 :t_y2y累积环比 :t_c2c单季 :c单季原始值 :c_o单季同比 :c_y2y单季环比 :c_c2c单季年比 :c_2yTTM :ttmTTM原始值 :ttm_oTTM同比 :ttm_y2yTTM环比 :ttm_c2c; 现金流量表: 年(y): 累积 :t累积原始值 :t_o累积同比 :t_y2y半年(hy): 累积 :t累积原始值 :t_o累积同比 :t_y2y累积环比 :t_c2c半年 :c半年原始值 :c_o半年同比 :c_y2y半年环比 :c_c2c半年年比 :c_2yTTM :ttmTTM原始值 :ttm_oTTM同比 :ttm_y2yTTM环比 :ttm_c2c季度(q): 累积 :t累积原始值 :t_o累积同比 :t_y2y累积环比 :t_c2c单季 :c单季原始值 :c_o单季同比 :c_y2y单季环比 :c_c2c单季年比 :c_2yTTM :ttmTTM原始值 :ttm_oTTM同比 :ttm_y2yTTM环比 :ttm_c2c tableName.fieldName 资产负债表 一、资产总计 : bs.ta流动资产合计 : bs.tca流动资产占比 : bs.tca_ta_r货币资金 : bs.cabb货币资金占比 : bs.cabb_ta_r可供出售金融资产(流动) : bs.cafsfa应收账款 : bs.ar存货 : bs.i非流动资产合计 : bs.tnca非流动资产占比 : bs.tnca_ta_r可供出售金融资产(非流动) : bs.ncafsfa物业、厂房及设备 : bs.ppe商誉及无形资产 : bs.gwaia二、负债合计 : bs.tl资产负债率 : bs.tl_ta_r流动负债合计 : bs.tcl流动负债占比 : bs.tcl_tl_r应付账款 : bs.ap递延收益 : bs.drev非流动负债合计 : bs.tncl非流动负债占比 : bs.tncl_tl_r递延所得税负债 : bs.ditl三、所有者权益合计 : bs.toe股东权益占比 : bs.toe_ta_r未分配利润 : bs.rtp其他综合收益 : bs.oci归属于母公司普通股股东权益合计 : bs.tetoshopc四、股本、股东以及估值市值 : bs.mc总股本 : bs.tsc 利润表 一、营业总收入 : ps.toi营业收入 : ps.oi营业成本 : ps.oc毛利率(GM) : ps.gp_m销售及行政开支 : ps.sgnae研发费用 : ps.rade研发费用率 : ps.rade_r利息费用 : ps.ieife二、利润总额 : ps.tp所得税费用 : ps.ite有效税率 : ps.ite_tp_r研发费占利润总额比值 : ps.rade_tp_r三、净利润 : ps.np净利润率 : ps.np_s_r归属于母公司股东及其他权益持有者的净利润 : ps.npatshaoehopc归属于母公司普通股股东的净利润 : ps.npatoshopc少数股东损益 : ps.npatmsh五、分红及涨跌幅分红金额 : ps.da 现金流量表 一、经营活动产生的现金流量净额 : cfs.ncffoa业务收购支付的相关现金 : cfs.ncpicwba二、投资活动产生的现金流量净额 : cfs.ncffia三、筹资活动产生的现金流量净额 : cfs.ncfffa支付股息支付的现金 : cfs.cpfd四、现金及现金等价物的净增加额 : cfs.niicace汇率变动对现金及现金等价物的影响 : cfs.iocacedtfier五、附注股份酬金支出 : cfs.sbce折旧及摊销 : cfs.daa 财务指标 一、每股指标总股本 : m.tsc (expressionCalculateType参考资产负债表) 归属于母公司普通股股东的每股收益 : m.npatoshopc_ps (expressionCalculateType参考利润表) 归属于母公司普通股股东的每股股东权益 : m.tetoshopc_ps (expressionCalculateType参考资产负债表) 每股未分配利润 : m.rp_ps (expressionCalculateType参考资产负债表) 每股分红 : m.da_ps (expressionCalculateType参考利润表) 每股经营活动产生的现金流量净额 : m.ncffoa_ps (expressionCalculateType参考现金流量表) 二、盈利能力归属于母公司普通股股东的ROE : m.roe_atoshaopc (expressionCalculateType参考利润表) 净资产收益率(ROE) : m.roe (expressionCalculateType参考利润表) 杠杆倍数 : m.l (expressionCalculateType参考资产负债表) 总资产收益率(ROA) : m.roa (expressionCalculateType参考利润表) 总资产周转率 : m.ta_to (expressionCalculateType参考利润表) 净利润率 : m.np_s_r (expressionCalculateType参考利润表) 毛利率(GM) : m.gp_m (expressionCalculateType参考利润表) 三、营运能力(周转率)存货周转率 : m.i_tor (expressionCalculateType参考利润表) 应收账款周转率 : m.ar_tor (expressionCalculateType参考利润表) 应付账款周转率 : m.ap_tor (expressionCalculateType参考利润表) 不动产、厂房及设备周转率 : m.ppe_tor (expressionCalculateType参考利润表) 四、营运能力(周转天数)存货周转天数 : m.i_ds (expressionCalculateType参考利润表) 应收账款周转天数 : m.ar_ds (expressionCalculateType参考利润表) 应付账款周转天数 : m.ap_ds (expressionCalculateType参考利润表) 不动产、厂房及设备周转天数 : m.ppe_ds (expressionCalculateType参考利润表) 流动资产周转天数 : m.tca_ds (expressionCalculateType参考利润表) 股东权益周转天数 : m.toe_ds (expressionCalculateType参考利润表) 五、偿债及资本结构资产负债率 : m.tl_ta_r (expressionCalculateType参考资产负债表) 货币资金占流动负债比率 : m.cabb_tcl_r (expressionCalculateType参考资产负债表) 流动比率 : m.c_r (expressionCalculateType参考资产负债表) 不动产、厂房及设备占总资产比率 : m.ppe_ta_r (expressionCalculateType参考资产负债表) 六、现金流量经投融产生的现金流量净额 : m.ncffoaiafa (expressionCalculateType参考现金流量表) 经营活动产生的现金流量净额对净利润的比率 : m.ncffoa_np_r (expressionCalculateType参考利润表) |

### 示例

```json
{
    "date": "2023-12-31",
    "stockCodes": [
        ".INX"
    ],
    "metricsList": [
        "q.ps.toi.t"
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
            "date": "2023-12-31T00:00:00-05:00",
            "currency": "USD",
            "reportDate": "2024-09-06T00:00:00-04:00",
            "reportType": "annual_report",
            "standardDate": "2023-12-31T00:00:00-05:00",
            "q": {
                "ps": {
                    "toi": {
                        "t": 16332464326000
                    }
                }
            },
            "stockCode": ".INX"
        }
    ]
}
```
