# API文档/大陆/行业接口/申万2021版/财务报表/混合

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/industry/fs/sw_2021/hybrid
> API Key: `cn/industry/fs/sw_2021/hybrid`

---

## 财报数据API

**简要描述:** 获取财务数据，如营业收入、ROE等。

**说明:**

- 指标计算请参考行业财务数据计算

**请求URL:** `https://open.lixinger.com/api/cn/industry/fs/sw_2021/hybrid`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/industry/fs/sw_2021/hybrid](https://www.lixinger.com/api/open-api/html-doc/cn/industry/fs/sw_2021/hybrid)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 行业代码数组。 stockCodes长度>=1且<=100，格式如下：["490000"]。 请参考 行业信息API 获取合法的stockCode。 需要注意的是，当传入startDate时只能传入一个股票代码。 |
| date | No | String: latest \| YYYY-MM-DD (北京时间) | 信息日期。 用于获取指定日期数据。 由于每个季度的最后一天为财报日，请确保传入正确的日期，例如：2017-03-31、2017-06-30、2017-09-30、2017-12-31 或 latest。 其中，传入 **latest** 会得到最近1.1年内的最新财报数据。 需要注意的是，startDate和date至少要传一个。 |
| startDate | No | String: YYYY-MM-DD (北京时间) | 信息起始时间。 用于获取一定时间范围内的数据。 **开始和结束的时间间隔不超过10年** 需要注意的是，startDate和date至少要传一个。 |
| endDate | No | String: YYYY-MM-DD (北京时间) | 信息结束时间。 用于获取一定时间范围内的数据。 默认值是上周一。 需要注意的是，请与startDate一起使用。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[tableName].[fieldName].[expressionCalculateType]。 比如，你想获取营业总收入累计原始值以及应收账款当期同比值，对应的metricsList设置为：["q.ps.toi.t", "q.bs.ar.c_y2y"]。 需要注意的是，当stockCodes长度大于1时最多只能选取48个指标；当stockCodes长度等于1时最多只能获取128 个指标。 **当前支持:** granularity 年 : `y`; 半年 : `hy`; 季度 : `q` expressionCalculateType 资产负债表: 年(y): 当期 :t当期回溯值 :t_r当期同比 :t_y2y当期环比 :t_c2c半年(hy): 当期 :t当期回溯值 :t_r当期同比 :t_y2y当期环比 :t_c2c半年 :c半年回溯值 :c_r半年同比 :c_y2y半年环比 :c_c2c季度(q): 当期 :t当期回溯值 :t_r当期同比 :t_y2y当期环比 :t_c2c单季 :c单季回溯值 :c_r单季同比 :c_y2y单季环比 :c_c2c; 利润表: 年(y): 累积 :t累积回溯值 :t_r累积同比 :t_y2y半年(hy): 累积 :t累积回溯值 :t_r累积同比 :t_y2y累积环比 :t_c2c半年 :c半年回溯值 :c_r半年同比 :c_y2y半年环比 :c_c2c半年年比 :c_2yTTM :ttmTTM同比 :ttm_y2yTTM环比 :ttm_c2c季度(q): 累积 :t累积回溯值 :t_r累积同比 :t_y2y累积环比 :t_c2c单季 :c单季回溯值 :c_r单季同比 :c_y2y单季环比 :c_c2c单季年比 :c_2yTTM :ttmTTM同比 :ttm_y2yTTM环比 :ttm_c2c; 现金流量表: 年(y): 累积 :t累积回溯值 :t_r累积同比 :t_y2y半年(hy): 累积 :t累积回溯值 :t_r累积同比 :t_y2y累积环比 :t_c2c半年 :c半年回溯值 :c_r半年同比 :c_y2y半年环比 :c_c2c半年年比 :c_2yTTM :ttmTTM同比 :ttm_y2yTTM环比 :ttm_c2c季度(q): 累积 :t累积回溯值 :t_r累积同比 :t_y2y累积环比 :t_c2c单季 :c单季回溯值 :c_r单季同比 :c_y2y单季环比 :c_c2c单季年比 :c_2yTTM :ttmTTM同比 :ttm_y2yTTM环比 :ttm_c2c tableName.fieldName 资产负债表 一、资产总计 : bs.ta长期股权投资 : bs.ltei投资性房地产 : bs.rei固定资产 : bs.fa固定资产占总资产比率 : bs.fa_ta_r使用权资产 : bs.roua无形资产 : bs.ia商誉 : bs.gw商誉占净资产比率 : bs.gw_toe_r递延所得税资产 : bs.dita二、负债合计 : bs.tl资产负债率 : bs.tl_ta_r拆入资金 : bs.pfbaofi应付职工薪酬 : bs.sawp应交税费 : bs.tp应付债券 : bs.bp递延所得税负债 : bs.ditl三、所有者权益合计 : bs.toe股东权益占比 : bs.toe_ta_r股本 : bs.sc其他权益工具 : bs.oei(其中)优先股 : bs.psioei(其中)永续债 : bs.pcsioei资本公积 : bs.capr减：库存股 : bs.is其他综合收益 : bs.oci专项储备 : bs.rr盈余公积 : bs.surr一般风险准备金 : bs.pogr未分配利润 : bs.rtp外币报表折算差额 : bs.er归属于母公司股东及其他权益持有者的权益合计 : bs.tetshaoehopc归属于母公司普通股股东权益合计 : bs.tetoshopc少数股东权益 : bs.etmsh四、员工情况员工人数 : bs.ep_stn五、股本、股东以及估值市值 : bs.mc总股本 : bs.tsc流通股本 : bs.csc总股东人数(季度) : bs.shnA股股东人数(季度) : bs.shn_om 利润表 一、营业收入 : ps.oi其他业务收入 : ps.ooi税金及附加 : ps.tas投资收益 : ps.ivi(其中)对联营企业及合营企业的投资收益 : ps.iifaajv汇兑收益 : ps.ei公允价值变动收益 : ps.ciofv信用减值损失 : ps.cilor资产减值损失 : ps.ailor其他资产减值损失 : ps.oail其他业务成本 : ps.ooe三、营业利润 : ps.op营业利润率 : ps.op_s_r加：营业外收入 : ps.noi减：营业外支出 : ps.noe四、利润总额 : ps.tp减：所得税费用 : ps.ite有效税率 : ps.ite_tp_r五、净利润 : ps.np净利润率 : ps.np_s_r(一)持续经营净利润 : ps.npfco(二)终止经营净利润 : ps.npfdco归属于母公司股东及其他权益持有者的净利润 : ps.npatshaoehopc归属于母公司普通股股东的净利润 : ps.npatoshopc少数股东损益 : ps.npatmsh归属于母公司普通股股东的扣除非经常性损益的净利润 : ps.npadnrpatoshaopc扣非净利润占比 : ps.npadnrpatoshaopc_npatoshopc_r九、分红、融资及涨跌幅分红金额 : ps.daA股分红金额 : ps.da_omA股融资金额 : ps.fa_om十、客户及供应商 现金流量表 一、经营活动产生的现金流量收取利息、手续费及佣金的现金 : cfs.crfifac收到的其他与经营活动有关现金 : cfs.crrtooa经营活动现金流入小计 : cfs.stciffoa支付利息、手续费及佣金的现金 : cfs.cpfifac支付给职工及为职工支付的现金 : cfs.cptofe支付的各种税费 : cfs.cpft支付的其他与经营活动有关现金 : cfs.cprtooa经营活动现金流出小计 : cfs.stcoffoa经营活动产生的现金流量净额 : cfs.ncffoa二、投资活动产生的现金流量金额收回投资收到的现金 : cfs.crfrci取得投资收益所收到的现金 : cfs.crfii处置固定资产、无形资产及其他长期资产收到的现金 : cfs.crfdofiaolta收到的其他与投资活动相关的现金 : cfs.crrtoia投资活动现金流入小计 : cfs.stcifia购建固定资产、无形资产及其他长期资产所支付的现金 : cfs.cpfpfiaolta投资所支付的现金 : cfs.cpfi支付的其他与投资活动有关的现金 : cfs.cprtoia投资活动现金流出小计 : cfs.stcoffia投资活动产生的现金流量净额 : cfs.ncffia三、筹资活动产生的现金流量吸收投资收到的现金 : cfs.crfai发行债券收到的现金 : cfs.crfib收到的其他与筹资活动有关的现金 : cfs.crrtofa筹资活动产生的现金流入小计 : cfs.stcifffa偿付债务支付的现金 : cfs.cpfbrp分配股利、利润或偿付利息所支付的现金 : cfs.cpfdapdoi支付的其他与筹资活动有关的现金 : cfs.cprtofa筹资活动产生的现金流出小计 : cfs.stcofffa筹资活动产生的现金流量净额 : cfs.ncfffa四、汇率变动对现金及现金等价物的影响 : cfs.iocacedtfier期初现金及现金等价物的余额 : cfs.bocaceatpb现金及现金等价物的净增加额 : cfs.niicace期末现金及现金等价物净余额 : cfs.bocaceatpe五、附注净利润 : cfs.np加：资产减值准备 : cfs.ioa信用减值损失 : cfs.cilor固定资产折旧、油气资产折耗、生产性生物资产折旧 : cfs.dofx_dooaga_dopba投资性房地产的折旧及摊销 : cfs.daaorei使用权资产摊销 : cfs.aoroua无形资产摊销 : cfs.aoia长期待摊费用摊销 : cfs.aoltde处置固定资产、无形资产和其他长期资产的损失 : cfs.lodofaiaaolta固定资产报废损失 : cfs.lfsfa公允价值变动损失 : cfs.lfcifv财务费用 : cfs.fe投资损失 : cfs.il递延所得税资产减少 : cfs.didita递延所得税负债增加 : cfs.iiditl存货的减少 : cfs.dii经营性应收项目的减少 : cfs.dior经营性应付项目的增加 : cfs.iiop其他 : cfs.o一年内到期的可转换公司债券 : cfs.cbdwioy融资租入固定资产 : cfs.flofa经营活动产生的现金流量净额 : cfs.ncffoa_dup 财务指标 一、人均指标员工人数 : m.ep_stn (expressionCalculateType参考资产负债表) 人均净利润 : m.np_pc (expressionCalculateType参考利润表) 人均薪酬 : m.s_pc (expressionCalculateType参考现金流量表) 总股本 : m.tsc (expressionCalculateType参考资产负债表) 归属于母公司普通股股东的每股收益 : m.npatoshopc_ps (expressionCalculateType参考利润表) 归属于母公司普通股股东的每股扣非收益 : m.npadnrpatoshaopc_ps (expressionCalculateType参考利润表) 归属于母公司普通股股东的每股股东权益 : m.tetoshopc_ps (expressionCalculateType参考资产负债表) 每股资本公积 : m.cr_ps (expressionCalculateType参考资产负债表) 每股未分配利润 : m.rp_ps (expressionCalculateType参考资产负债表) 每股分红 : m.da_ps (expressionCalculateType参考利润表) 每股经营活动产生的现金流量 : m.stciffoa_ps (expressionCalculateType参考现金流量表) 每股经营活动产生的现金流量净额 : m.ncffoa_ps (expressionCalculateType参考现金流量表) 三、盈利能力归属于母公司普通股股东的ROE : m.roe_atoshaopc (expressionCalculateType参考利润表) 归属于母公司普通股股东的扣非ROE : m.roe_adnrpatoshaopc (expressionCalculateType参考利润表) 归属于少数股股东的ROE : m.roe_atomsh (expressionCalculateType参考利润表) 净资产收益率(ROE) : m.roe (expressionCalculateType参考利润表) 杠杆倍数 : m.l (expressionCalculateType参考资产负债表) 总资产收益率(ROA) : m.roa (expressionCalculateType参考利润表) 总资产周转率 : m.ta_to (expressionCalculateType参考利润表) 净利润率 : m.np_s_r (expressionCalculateType参考利润表) 四、营运能力(周转率)固定资产周转率 : m.fa_tor (expressionCalculateType参考利润表) 五、营运能力(周转天数)固定资产周转天数 : m.fa_ds (expressionCalculateType参考利润表) 股东权益周转天数 : m.toe_ds (expressionCalculateType参考利润表) 总资产周转天数 : m.ta_ds (expressionCalculateType参考利润表) 六、偿债及资本结构资产负债率 : m.tl_ta_r (expressionCalculateType参考资产负债表) 固定资产占总资产比率 : m.fa_ta_r (expressionCalculateType参考资产负债表) 七、现金流量自由现金流量 : m.fcf (expressionCalculateType参考现金流量表) 经投融产生的现金流量净额 : m.ncffoaiafa (expressionCalculateType参考现金流量表) 经营活动产生的现金流量净额对营业利润的比率 : m.ncffoa_op_r (expressionCalculateType参考利润表) 经营活动产生的现金流量净额对净利润的比率 : m.ncffoa_np_r (expressionCalculateType参考利润表) 经营活动产生的现金流量净额对固定资产的比率 : m.ncffoa_fa_r (expressionCalculateType参考现金流量表) |

### 示例

```json
{
    "date": "2025-09-30",
    "stockCodes": [
        "490000"
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
            "date": "2025-09-30T00:00:00+08:00",
            "currency": "CNY",
            "reportDate": "2025-10-31T00:00:00+08:00",
            "reportType": "third_quarterly_report",
            "standardDate": "2025-09-30T00:00:00+08:00",
            "q": {
                "ps": {
                    "oi": {
                        "t": 2894735402145
                    }
                }
            },
            "stockCode": "490000"
        }
    ]
}
```
