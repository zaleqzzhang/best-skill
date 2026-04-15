# API文档/大陆/行业接口/申万2021版/财务报表/证券

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/industry/fs/sw_2021/security
> API Key: `cn/industry/fs/sw_2021/security`

---

## 财报数据API

**简要描述:** 获取财务数据，如营业收入、ROE等。

**说明:**

- 指标计算请参考行业财务数据计算

**请求URL:** `https://open.lixinger.com/api/cn/industry/fs/sw_2021/security`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/industry/fs/sw_2021/security](https://www.lixinger.com/api/open-api/html-doc/cn/industry/fs/sw_2021/security)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 行业代码数组。 stockCodes长度>=1且<=100，格式如下：["490100"]。 请参考 行业信息API 获取合法的stockCode。 需要注意的是，当传入startDate时只能传入一个股票代码。 |
| date | No | String: latest \| YYYY-MM-DD (北京时间) | 信息日期。 用于获取指定日期数据。 由于每个季度的最后一天为财报日，请确保传入正确的日期，例如：2017-03-31、2017-06-30、2017-09-30、2017-12-31 或 latest。 其中，传入 **latest** 会得到最近1.1年内的最新财报数据。 需要注意的是，startDate和date至少要传一个。 |
| startDate | No | String: YYYY-MM-DD (北京时间) | 信息起始时间。 用于获取一定时间范围内的数据。 **开始和结束的时间间隔不超过10年** 需要注意的是，startDate和date至少要传一个。 |
| endDate | No | String: YYYY-MM-DD (北京时间) | 信息结束时间。 用于获取一定时间范围内的数据。 默认值是上周一。 需要注意的是，请与startDate一起使用。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[tableName].[fieldName].[expressionCalculateType]。 比如，你想获取营业总收入累计原始值以及应收账款当期同比值，对应的metricsList设置为：["q.ps.toi.t", "q.bs.ar.c_y2y"]。 需要注意的是，当stockCodes长度大于1时最多只能选取48个指标；当stockCodes长度等于1时最多只能获取128 个指标。 **当前支持:** granularity 年 : `y`; 半年 : `hy`; 季度 : `q` expressionCalculateType 资产负债表: 年(y): 当期 :t当期回溯值 :t_r当期同比 :t_y2y当期环比 :t_c2c半年(hy): 当期 :t当期回溯值 :t_r当期同比 :t_y2y当期环比 :t_c2c半年 :c半年回溯值 :c_r半年同比 :c_y2y半年环比 :c_c2c季度(q): 当期 :t当期回溯值 :t_r当期同比 :t_y2y当期环比 :t_c2c单季 :c单季回溯值 :c_r单季同比 :c_y2y单季环比 :c_c2c; 利润表: 年(y): 累积 :t累积回溯值 :t_r累积同比 :t_y2y半年(hy): 累积 :t累积回溯值 :t_r累积同比 :t_y2y累积环比 :t_c2c半年 :c半年回溯值 :c_r半年同比 :c_y2y半年环比 :c_c2c半年年比 :c_2yTTM :ttmTTM同比 :ttm_y2yTTM环比 :ttm_c2c季度(q): 累积 :t累积回溯值 :t_r累积同比 :t_y2y累积环比 :t_c2c单季 :c单季回溯值 :c_r单季同比 :c_y2y单季环比 :c_c2c单季年比 :c_2yTTM :ttmTTM同比 :ttm_y2yTTM环比 :ttm_c2c; 现金流量表: 年(y): 累积 :t累积回溯值 :t_r累积同比 :t_y2y半年(hy): 累积 :t累积回溯值 :t_r累积同比 :t_y2y累积环比 :t_c2c半年 :c半年回溯值 :c_r半年同比 :c_y2y半年环比 :c_c2c半年年比 :c_2yTTM :ttmTTM同比 :ttm_y2yTTM环比 :ttm_c2c季度(q): 累积 :t累积回溯值 :t_r累积同比 :t_y2y累积环比 :t_c2c单季 :c单季回溯值 :c_r单季同比 :c_y2y单季环比 :c_c2c单季年比 :c_2yTTM :ttmTTM同比 :ttm_y2yTTM环比 :ttm_c2c tableName.fieldName 资产负债表 一、资产总计 : bs.ta货币资金 : bs.cabb(其中)客户存款 : bs.choboc货币资金占比 : bs.cabb_ta_r结算备付金 : bs.sr(其中)客户备付金 : bs.dhoboc融出资金 : bs.ma衍生金融资产 : bs.dfa存出保证金 : bs.rfd应收账款 : bs.ar应收利息 : bs.ir买入返售金融资产 : bs.fahursa金融投资： : bs.t_fi#以公允价值计量且其变动计入当期损益的金融投资 : bs.fiafvtpol#以摊余成本计量的金融投资 : bs.fiaac#以公允价值计量且其变动计入其他综合收益的债务工具投资 : bs.diafvtoci#指定为以公允价值计量且其变动计入其他综合收益的权益工具投资 : bs.deiafvtoci#可供出售金融资产 : bs.afsfa#持有至到期投资 : bs.htmi长期股权投资 : bs.ltei投资性房地产 : bs.rei固定资产 : bs.fa固定资产占总资产比率 : bs.fa_ta_r在建工程 : bs.cip使用权资产 : bs.roua无形资产 : bs.ia(其中)数据资源 : bs.ia_dr商誉 : bs.gw商誉占净资产比率 : bs.gw_toe_r递延所得税资产 : bs.dita持有待售资产 : bs.ahfs其他资产 : bs.oa二、负债合计 : bs.tl资产负债率 : bs.tl_ta_r短期借款 : bs.stl应付短期融资款 : bs.stfip拆入资金 : bs.pfbaofi衍生金融负债 : bs.dfl以公允价值计量且其变动计入当期损益的金融负债 : bs.flafvtpol卖出回购金融资产 : bs.fasurpa代理买卖证券款 : bs.stoa代理承销证券款 : bs.ssoa应付职工薪酬 : bs.sawp应交税费 : bs.tp应付账款 : bs.ap应付利息 : bs.intp合同负债 : bs.cl预计负债 : bs.al长期借款 : bs.ltl应付债券 : bs.bp租赁负债 : bs.ll递延所得税负债 : bs.ditl其他负债 : bs.ol三、所有者权益合计 : bs.toe股东权益占比 : bs.toe_ta_r股本 : bs.sc其他权益工具 : bs.oei(其中)优先股 : bs.psioei(其中)永续债 : bs.pcsioei资本公积 : bs.capr减：库存股 : bs.is其他综合收益 : bs.oci专项储备 : bs.rr盈余公积 : bs.surr一般风险准备金 : bs.pogr未分配利润 : bs.rtp外币报表折算差额 : bs.er归属于母公司股东及其他权益持有者的权益合计 : bs.tetshaoehopc归属于母公司普通股股东权益合计 : bs.tetoshopc少数股东权益 : bs.etmsh四、员工情况员工人数 : bs.ep_stn五、股本、股东以及估值市值 : bs.mc总股本 : bs.tsc流通股本 : bs.csc总股东人数(季度) : bs.shnA股股东人数(季度) : bs.shn_om六、券商特殊指标 — 母公司净资本及有关风险控制指标净资本 : bs.pc_nc(其中)核心净资本 : bs.pc_cnc(其中)附属净资本 : bs.pc_snc净资产 : bs.pc_na负债 : bs.pc_l各项风险资本准备之和 : bs.pc_trcr风险覆盖率 : bs.pc_rcr资本杠杆率 : bs.pc_clr流动性覆盖率 : bs.pc_lcr净稳定资金率 : bs.pc_nsfr净资本/净资产 : bs.pc_nc_na_r净资本/负债 : bs.pc_nc_l_r净资产/负债 : bs.pc_na_l_r自营权益类证券及其衍生品/净资本 : bs.pc_pesaid_nc_r自营非权益类证券及其衍生品/净资本 : bs.pc_pnesaid_nc_r 利润表 一、营业收入 : ps.oi净利息收入 : ps.nii(其中)利息收入 : ps.ii(其中)利息支出 : ps.ie手续费及佣金净收入 : ps.nfaci(其中)经纪业务净收入 : ps.nfifb(其中)投资银行业务净收入 : ps.nfifib(其中)资产管理业务净收入 : ps.nfifam投资收益 : ps.ivi(其中)对联营企业及合营企业的投资收益 : ps.iifaajv(其中)以摊余成本计量的金融资产终止确认产生的投资收益 : ps.iftdofamaac其他收益 : ps.oic公允价值变动收益 : ps.ciofv汇兑收益 : ps.ei其他业务收入 : ps.ooi资产处置收益 : ps.adi二、营业支出 : ps.oe税金及附加 : ps.tas业务及管理费用 : ps.baae资产减值损失 : ps.ailor信用减值损失 : ps.cilor其他资产减值损失 : ps.oail其他业务成本 : ps.ooe三、营业利润 : ps.op营业利润率 : ps.op_s_r加：营业外收入 : ps.noi减：营业外支出 : ps.noe四、利润总额 : ps.tp减：所得税费用 : ps.ite有效税率 : ps.ite_tp_r五、净利润 : ps.np净利润率 : ps.np_s_r(一)持续经营净利润 : ps.npfco(二)终止经营净利润 : ps.npfdco归属于母公司股东及其他权益持有者的净利润 : ps.npatshaoehopc归属于母公司普通股股东的净利润 : ps.npatoshopc少数股东损益 : ps.npatmsh归属于母公司普通股股东的扣除非经常性损益的净利润 : ps.npadnrpatoshaopc扣非净利润占比 : ps.npadnrpatoshaopc_npatoshopc_r九、分红、融资及涨跌幅分红金额 : ps.daA股分红金额 : ps.da_omA股融资金额 : ps.fa_om十、客户及供应商 现金流量表 一、经营活动产生的现金流量为交易目的而持有的金融资产净减少额 : cfs.ndifahftp处置可供出售金融资产收到的现金净额 : cfs.ncrfdoafsfaioa融出资金净减少额 : cfs.ndima拆入资金净增加额 : cfs.niipfbaofi卖出回购业务资金净增加额 : cfs.niifasurpaioa收取利息、手续费及佣金的现金 : cfs.crfifac代理买卖证券收到的现金净额 : cfs.ncrfstoa代理承销证券收到的现金净额 : cfs.ncrfssoa收到的其他与经营活动有关现金 : cfs.crrtooa经营活动现金流入小计 : cfs.stciffoa为交易目的而持有的金融资产净增加额 : cfs.niifahftp购置可供出售金融资产支付的现金净额 : cfs.ncpfbafsfaioa融出资金净增加额 : cfs.niima拆出资金增加额 : cfs.niipwbaofi买入返售金融资产净增加额 : cfs.niifahursaioa支付利息、手续费及佣金的现金 : cfs.cpfifac支付给职工及为职工支付的现金 : cfs.cptofe支付的各种税费 : cfs.cpft支付的其他与经营活动有关现金 : cfs.cprtooa经营活动现金流出小计 : cfs.stcoffoa经营活动产生的现金流量净额 : cfs.ncffoa二、投资活动产生的现金流量金额收回投资收到的现金 : cfs.crfrci取得投资收益所收到的现金 : cfs.crfii处置固定资产、无形资产及其他长期资产收到的现金 : cfs.crfdofiaolta处置子公司、合营联营企业及其他营业单位收到的现金净额 : cfs.ncrfdossajvaou(其中)处置子公司或其他营业单位收到的现金净额 : cfs.ncrfdossaou(其中)处置合营或联营公司所收到的现金 : cfs.ncrfdoaajv收到的其他与投资活动相关的现金 : cfs.crrtoia投资活动现金流入小计 : cfs.stcifia投资所支付的现金 : cfs.cpfi购建固定资产、无形资产及其他长期资产所支付的现金 : cfs.cpfpfiaolta取得子公司、合营联营企业及其他营业单位支付的现金净额 : cfs.ncpfbssajvaou(其中)取得子公司及其营业单位支付的现金净额 : cfs.ncpfbssaou(其中)取得联营及合营公司支付的现金净额 : cfs.ncpfbajv支付的其他与投资活动有关的现金 : cfs.cprtoia投资活动现金流出小计 : cfs.stcoffia投资活动产生的现金流量净额 : cfs.ncffia三、筹资活动产生的现金流量吸收投资收到的现金 : cfs.crfai(其中)子公司吸收少数股东投资收到的现金 : cfs.crfamshibss取得借款收到的现金 : cfs.crfl发行债券收到的现金 : cfs.crfib收到的其他与筹资活动有关的现金 : cfs.crrtofa筹资活动产生的现金流入小计 : cfs.stcifffa偿付债务支付的现金 : cfs.cpfbrp分配股利、利润或偿付利息所支付的现金 : cfs.cpfdapdoi(其中)子公司支付少数股东股利及利润 : cfs.cpfdapomshpbss支付的其他与筹资活动有关的现金 : cfs.cprtofa筹资活动产生的现金流出小计 : cfs.stcofffa筹资活动产生的现金流量净额 : cfs.ncfffa四、汇率变动对现金及现金等价物的影响 : cfs.iocacedtfier期初现金及现金等价物的余额 : cfs.bocaceatpb现金及现金等价物的净增加额 : cfs.niicace期末现金及现金等价物净余额 : cfs.bocaceatpe五、附注净利润 : cfs.np加：资产减值准备 : cfs.ioa信用减值损失 : cfs.cilor固定资产折旧、油气资产折耗、生产性生物资产折旧 : cfs.dofx_dooaga_dopba投资性房地产的折旧及摊销 : cfs.daaorei使用权资产摊销 : cfs.aoroua无形资产摊销 : cfs.aoia长期待摊费用摊销 : cfs.aoltde处置固定资产、无形资产和其他长期资产的损失 : cfs.lodofaiaaolta固定资产报废损失 : cfs.lfsfa公允价值变动损失 : cfs.lfcifv财务费用 : cfs.fe投资损失 : cfs.il递延所得税资产减少 : cfs.didita递延所得税负债增加 : cfs.iiditl存货的减少 : cfs.dii经营性应收项目的减少 : cfs.dior经营性应付项目的增加 : cfs.iiop其他 : cfs.o一年内到期的可转换公司债券 : cfs.cbdwioy融资租入固定资产 : cfs.flofa经营活动产生的现金流量净额 : cfs.ncffoa_dup 财务指标 一、人均指标员工人数 : m.ep_stn (expressionCalculateType参考资产负债表) 人均营业收入 : m.oi_pc (expressionCalculateType参考利润表) 人均净利润 : m.np_pc (expressionCalculateType参考利润表) 人均薪酬 : m.s_pc (expressionCalculateType参考现金流量表) 二、券商特殊指标 — 母公司净资本及有关风险控制指标净资本 : m.pc_nc (expressionCalculateType参考资产负债表) (其中)核心净资本 : m.pc_cnc (expressionCalculateType参考资产负债表) (其中)附属净资本 : m.pc_snc (expressionCalculateType参考资产负债表) 净资产 : m.pc_na (expressionCalculateType参考资产负债表) 负债 : m.pc_l (expressionCalculateType参考资产负债表) 各项风险资本准备之和 : m.pc_trcr (expressionCalculateType参考资产负债表) 风险覆盖率 : m.pc_rcr (expressionCalculateType参考资产负债表) 资本杠杆率 : m.pc_clr (expressionCalculateType参考资产负债表) 流动性覆盖率 : m.pc_lcr (expressionCalculateType参考资产负债表) 净稳定资金率 : m.pc_nsfr (expressionCalculateType参考资产负债表) 净资本/净资产 : m.pc_nc_na_r (expressionCalculateType参考资产负债表) 净资本/负债 : m.pc_nc_l_r (expressionCalculateType参考资产负债表) 净资产/负债 : m.pc_na_l_r (expressionCalculateType参考资产负债表) 自营权益类证券及其衍生品/净资本 : m.pc_pesaid_nc_r (expressionCalculateType参考资产负债表) 自营非权益类证券及其衍生品/净资本 : m.pc_pnesaid_nc_r (expressionCalculateType参考资产负债表) 三、每股指标总股本 : m.tsc (expressionCalculateType参考资产负债表) 归属于母公司普通股股东的每股收益 : m.npatoshopc_ps (expressionCalculateType参考利润表) 归属于母公司普通股股东的每股扣非收益 : m.npadnrpatoshaopc_ps (expressionCalculateType参考利润表) 归属于母公司普通股股东的每股股东权益 : m.tetoshopc_ps (expressionCalculateType参考资产负债表) 每股资本公积 : m.cr_ps (expressionCalculateType参考资产负债表) 每股未分配利润 : m.rp_ps (expressionCalculateType参考资产负债表) 每股分红 : m.da_ps (expressionCalculateType参考利润表) 每股经营活动产生的现金流量 : m.stciffoa_ps (expressionCalculateType参考现金流量表) 每股经营活动产生的现金流量净额 : m.ncffoa_ps (expressionCalculateType参考现金流量表) 四、盈利能力归属于少数股股东的ROE : m.roe_atomsh (expressionCalculateType参考利润表) 归属于母公司普通股股东的ROE : m.roe_atoshaopc (expressionCalculateType参考利润表) 归属于母公司普通股股东的扣非ROE : m.roe_adnrpatoshaopc (expressionCalculateType参考利润表) 净资产收益率(ROE) : m.roe (expressionCalculateType参考利润表) 杠杆倍数 : m.l (expressionCalculateType参考资产负债表) 总资产收益率(ROA) : m.roa (expressionCalculateType参考利润表) 总资产周转率 : m.ta_to (expressionCalculateType参考利润表) 净利润率 : m.np_s_r (expressionCalculateType参考利润表) 五、营运能力(周转率)固定资产周转率 : m.fa_tor (expressionCalculateType参考利润表) 六、营运能力(周转天数)固定资产周转天数 : m.fa_ds (expressionCalculateType参考利润表) 股东权益周转天数 : m.toe_ds (expressionCalculateType参考利润表) 总资产周转天数 : m.ta_ds (expressionCalculateType参考利润表) 七、偿债及资本结构资产负债率 : m.tl_ta_r (expressionCalculateType参考资产负债表) 固定资产占总资产比率 : m.fa_ta_r (expressionCalculateType参考资产负债表) 八、现金流量自由现金流量 : m.fcf (expressionCalculateType参考现金流量表) 经投融产生的现金流量净额 : m.ncffoaiafa (expressionCalculateType参考现金流量表) 经营活动产生的现金流量净额对营业利润的比率 : m.ncffoa_op_r (expressionCalculateType参考利润表) 经营活动产生的现金流量净额对净利润的比率 : m.ncffoa_np_r (expressionCalculateType参考利润表) 经营活动产生的现金流量净额对固定资产的比率 : m.ncffoa_fa_r (expressionCalculateType参考现金流量表) |

### 示例

```json
{
    "date": "2025-09-30",
    "stockCodes": [
        "490100"
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
                        "t": 429251671957
                    }
                }
            },
            "stockCode": "490100"
        }
    ]
}
```
