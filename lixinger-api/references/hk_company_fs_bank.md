# API文档/香港/公司接口/财务报表/银行

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/hk/company/fs/bank
> API Key: `hk/company/fs/bank`

---

## 财报数据API

**简要描述:** 获取财务数据，如营业收入、ROE等。

**请求URL:** `https://open.lixinger.com/api/hk/company/fs/bank`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/hk/company/fs/bank](https://www.lixinger.com/api/open-api/html-doc/hk/company/fs/bank)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 股票代码数组。 stockCodes长度>=1且<=100，格式如下：["01398"]。 请参考 股票信息API 获取合法的stockCode。 需要注意的是，当传入startDate时只能传入一个股票代码。 |
| date | No | String: latest \| YYYY-MM-DD (北京时间) | 信息日期。 用于获取指定日期数据。 由于每个季度的最后一天为财报日，请确保传入正确的日期，例如：2017-03-31、2017-06-30、2017-09-30、2017-12-31 或 latest。 其中，传入 **latest** 会得到最近1.1年内的最新财报数据。 需要注意的是，startDate和date至少要传一个。 |
| startDate | No | String: YYYY-MM-DD (北京时间) | 信息起始时间。 用于获取一定时间范围内的数据。 **开始和结束的时间间隔不超过10年** 需要注意的是，startDate和date至少要传一个。 |
| endDate | No | String: YYYY-MM-DD (北京时间) | 信息结束时间。 用于获取一定时间范围内的数据。 默认值是上周一。 需要注意的是，请与startDate一起使用。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[tableName].[fieldName].[expressionCalculateType]。 比如，你想获取营业总收入累计原始值以及应收账款当期同比值，对应的metricsList设置为：["q.ps.toi.t", "q.bs.ar.c_y2y"]。 需要注意的是，当stockCodes长度大于1时最多只能选取48个指标；当stockCodes长度等于1时最多只能获取128 个指标。 **当前支持:** granularity 年 : `y`; 半年 : `hy`; 季度 : `q` expressionCalculateType 资产负债表: 年(y): 当期 :t当期同比 :t_y2y当期环比 :t_c2c半年(hy): 当期 :t当期原始值 :t_o当期同比 :t_y2y当期环比 :t_c2c半年 :c半年原始值 :c_o半年同比 :c_y2y半年环比 :c_c2c季度(q): 当期 :t当期原始值 :t_o当期同比 :t_y2y当期环比 :t_c2c单季 :c单季原始值 :c_o单季同比 :c_y2y单季环比 :c_c2c; 利润表: 年(y): 累积 :t累积原始值 :t_o累积同比 :t_y2y半年(hy): 累积 :t累积原始值 :t_o累积同比 :t_y2y累积环比 :t_c2c半年 :c半年原始值 :c_o半年同比 :c_y2y半年环比 :c_c2c半年年比 :c_2yTTM :ttmTTM原始值 :ttm_oTTM同比 :ttm_y2yTTM环比 :ttm_c2c季度(q): 累积 :t累积原始值 :t_o累积同比 :t_y2y累积环比 :t_c2c单季 :c单季原始值 :c_o单季同比 :c_y2y单季环比 :c_c2c单季年比 :c_2yTTM :ttmTTM原始值 :ttm_oTTM同比 :ttm_y2yTTM环比 :ttm_c2c; 现金流量表: 年(y): 累积 :t累积原始值 :t_o累积同比 :t_y2y半年(hy): 累积 :t累积原始值 :t_o累积同比 :t_y2y累积环比 :t_c2c半年 :c半年原始值 :c_o半年同比 :c_y2y半年环比 :c_c2c半年年比 :c_2yTTM :ttmTTM原始值 :ttm_oTTM同比 :ttm_y2yTTM环比 :ttm_c2c季度(q): 累积 :t累积原始值 :t_o累积同比 :t_y2y累积环比 :t_c2c单季 :c单季原始值 :c_o单季同比 :c_y2y单季环比 :c_c2c单季年比 :c_2yTTM :ttmTTM原始值 :ttm_oTTM同比 :ttm_y2yTTM环比 :ttm_c2c tableName.fieldName 资产负债表 一、资产总计 : bs.ta现金及存放中央银行款项 : bs.cabwcb存放同业及其他金融机构款项 : bs.bwbaofi贵金属 : bs.pm拆出资金 : bs.pwbaofi买入返售金融资产 : bs.fahursa发放贷款及垫款 : bs.laatc香港政府负债证明书 : bs.hkgcoi衍生金融资产 : bs.dfa金融投资： : bs.financial_investing#指定以公允价值计量且其变动计入损益的金融投资(HK) : bs.dfiafvtpol#以公允价值计量且其变动计入当期损益的金融投资 : bs.fiafvtpol#以摊余成本计量的金融投资 : bs.fiaac#以公允价值计量且其变动计入其他综合收益的债务工具投资 : bs.diafvtoci#指定为以公允价值计量且其变动计入其他综合收益的权益工具投资 : bs.deiafvtoci物业、厂房及设备 : bs.ppe不动产、厂房及设备占总资产比率 : bs.ppe_ta_r使用权资产 : bs.roua于联营及合资公司之权益 : bs.iiaajv(其中)联营公司投资 : bs.iia(其中)合营公司投资 : bs.iijv商誉及无形资产 : bs.gwaia(其中)商誉 : bs.gw(其中)无形资产 : bs.ia可收回之税项 : bs.tr递延所得税资产 : bs.dita其他资产 : bs.oa二、负债合计 : bs.tl资产负债率 : bs.tl_ta_r向中央银行借款 : bs.bfcb同业及其他金融机构存放款项 : bs.dfbaofi拆入资金 : bs.pfbaofi客户存款 : bs.cd香港纸币流通额 : bs.hkcnic卖出回购金融资产 : bs.fasurpa衍生金融负债 : bs.dfl以公允价值计量且其变动计入当期损益的金融负债 : bs.flafvtpol指定以公允价值计量且其变动计入损益的金融负债(HK) : bs.dflafvtpol已发行债务证券 : bs.dsi应交税费 : bs.tp递延所得税负债 : bs.ditl其他负债 : bs.ol三、所有者权益合计 : bs.toe股东权益占比 : bs.toe_ta_r股本 : bs.sc股本溢价 : bs.spa其他权益工具 : bs.oei(其中)优先股 : bs.psioei(其中)永续债 : bs.pcsioei资本公积 : bs.capr减：库存股 : bs.is储备 : bs.r专项储备 : bs.rr其他储备 : bs.ors盈余公积 : bs.surr未分配利润 : bs.rtp股份奖励计划所持股份 : bs.shfsas可换股债券权益部分 : bs.ecocb归属于母公司股东及其他权益持有者的权益合计 : bs.tetshaoehopc归属于母公司普通股股东权益合计 : bs.tetoshopc少数股东权益 : bs.etmsh可赎回少数股东权益 : bs.rnci四、员工情况员工人数 : bs.ep_stn五、股本、股东以及估值市值 : bs.mc总股本 : bs.tscPE-TTM : bs.pe_ttmPB : bs.pbPS-TTM : bs.ps_ttmPCF-TTM : bs.pcf_ttm股息率 : bs.dyr 利润表 一、营业收入 : ps.oi净利息收入 : ps.nii(其中)利息收入 : ps.ii(其中)利息支出 : ps.ie手续费及佣金净收入 : ps.nfaci(其中)手续费及佣金收入 : ps.faci(其中)手续费及佣金支出 : ps.face已赚保费 : ps.ep对联营企业及合营企业的投资收益 : ps.iifaajv(其中)对联营公司的投资收益 : ps.iifa(其中)对合营企业的投资收益 : ps.iifjv投资收益 : ps.ivi其他业务收入 : ps.ooi二、营业支出 : ps.oe税金及附加 : ps.tas业务及管理费用 : ps.baae资产减值损失 : ps.ailor信用减值损失 : ps.cilor其他资产减值损失 : ps.oail其他业务成本 : ps.ooe三、利润总额 : ps.tp减：所得税费用 : ps.ite有效税率 : ps.ite_tp_r四、净利润 : ps.np净利润率 : ps.np_s_r归属于母公司股东及其他权益持有者的净利润 : ps.npatshaoehopc归属于母公司普通股股东的净利润 : ps.npatoshopc少数股东损益 : ps.npatmsh可赎回少数股东权益利息及回购视同股利分配 : ps.adddicwrornci非国际公认会计准则净利润 : ps.nonifrs_op非国际公认会计准则归属于母公司股东净利润 : ps.nonifrs_opatoehopc五、基本每股收益 : ps.beps稀释每股收益 : ps.deps六、综合收益总额 : ps.tci归属于母公司股东及其他权益持有者的综合收益总额 : ps.tciatshaoehopc归属于母公司普通股股东的综合收益总额 : ps.tciatoshopc归属于少数股东的综合收益总额 : ps.tciatmsh可赎回少数股东权益的综合收益 : ps.tciatrnci其他综合收益的税后净额 : ps.natooci七、分红、回购及涨跌幅分红金额 : ps.daH股分红金额 : ps.da_om分红率 : ps.d_np_r回购金额 : ps.ra年度涨跌幅 : ps.spc_a 现金流量表 经营活动产生的现金流量净额 : cfs.ncffoa投资活动产生的现金流量净额 : cfs.ncffia筹资活动产生的现金流量净额 : cfs.ncfffa现金及现金等价物的净增加额 : cfs.niicace期初现金及现金等价物的余额 : cfs.bocaceatpb汇率变动对现金及现金等价物的影响 : cfs.iocacedtfier期末现金及现金等价物净余额 : cfs.bocaceatpe 财务指标 一、人均指标员工人数 : m.ep_stn (expressionCalculateType参考资产负债表) 人均营业收入 : m.oi_pc (expressionCalculateType参考利润表) 人均净利润 : m.np_pc (expressionCalculateType参考利润表) 二、每股指标总股本 : m.tsc (expressionCalculateType参考资产负债表) 归属于母公司普通股股东的每股收益 : m.npatoshopc_ps (expressionCalculateType参考利润表) 归属于母公司普通股股东的每股股东权益 : m.tetoshopc_ps (expressionCalculateType参考资产负债表) 每股经营活动产生的现金流量净额 : m.ncffoa_ps (expressionCalculateType参考现金流量表) 每股资本公积 : m.cr_ps (expressionCalculateType参考资产负债表) 每股未分配利润 : m.rp_ps (expressionCalculateType参考资产负债表) 每股分红 : m.da_ps (expressionCalculateType参考利润表) 三、盈利能力归属于少数股股东的ROE : m.roe_atomsh (expressionCalculateType参考利润表) 归属于母公司普通股股东的ROE : m.roe_atoshaopc (expressionCalculateType参考利润表) 净资产收益率(ROE) : m.roe (expressionCalculateType参考利润表) 杠杆倍数 : m.l (expressionCalculateType参考资产负债表) 总资产收益率(ROA) : m.roa (expressionCalculateType参考利润表) 总资产周转率 : m.ta_to (expressionCalculateType参考利润表) 净利润率 : m.np_s_r (expressionCalculateType参考利润表) 四、营运能力(周转率)不动产、厂房及设备周转率 : m.ppe_tor (expressionCalculateType参考利润表) 五、营运能力(周转天数)不动产、厂房及设备周转天数 : m.ppe_ds (expressionCalculateType参考利润表) 股东权益周转天数 : m.toe_ds (expressionCalculateType参考利润表) 总资产周转天数 : m.ta_ds (expressionCalculateType参考利润表) 六、偿债及资本结构资产负债率 : m.tl_ta_r (expressionCalculateType参考资产负债表) 七、现金流量经投融产生的现金流量净额 : m.ncffoaiafa (expressionCalculateType参考现金流量表) |

**返回数据说明::**

| 参数名称 | 数据类型 | 说明 |
| --- | --- | --- |
| date | Date | 财报日期 |
| reportDate | Date | 公告时间 |
| standardDate | Date | 标准财年时间（不同公司的财年不一样，有的年报12月结束，有的却是3月结束，还有的7月结束。例如2017-01-01到2017-06-30结束的年报，调整到2016-Q4，其余的季报和中报都相应的做类似调整。调整后具有通用性。） |
| stockCode | String | 股票代码 |
| reportType | String | 财报类型 |
| currency | String | 货币类型 |
| auditOpinionType | String | 审计意见 无保留意见 : `unqualified_opinion`; 保留意见 : `qualified_opinion`; 保留意见与解释性说明 : `qualified_opinion_with_explanatory_notes`; 否定意见 : `adverse_opinion`; 拒绝表示意见 : `disclaimer_of_opinion`; 解释性说明 : `explanatory_statement`; 无法表示意见 : `unable_to_express_an_opinion`; 带强调事项段的无保留意见 : `unqualified_opinion_with_highlighted_matter_paragraph` |

### 示例

```json
{
    "date": "2023-12-31",
    "stockCodes": [
        "01398"
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
            "currency": "CNY",
            "q": {
                "ps": {
                    "oi": {
                        "t": 928051456000
                    }
                }
            },
            "reportDate": "2024-03-28T00:00:00+08:00",
            "reportType": "annual_report",
            "standardDate": "2023-12-31T00:00:00+08:00",
            "stockCode": "01398"
        }
    ]
}
```
