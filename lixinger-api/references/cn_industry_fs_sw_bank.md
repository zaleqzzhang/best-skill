# API文档/大陆/行业接口/申万/财务报表/银行

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/industry/fs/sw/bank
> API Key: `cn/industry/fs/sw/bank`

---

## 财报数据API

**简要描述:** 获取财务数据，如营业收入、ROE等。

**说明:**

- 指标计算请参考行业财务数据计算

**请求URL:** `https://open.lixinger.com/api/cn/industry/fs/sw/bank`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/industry/fs/sw/bank](https://www.lixinger.com/api/open-api/html-doc/cn/industry/fs/sw/bank)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 行业代码数组。 stockCodes长度>=1且<=100，格式如下：["480000"]。 请参考 行业信息API 获取合法的stockCode。 需要注意的是，当传入startDate时只能传入一个股票代码。 |
| date | No | String: latest \| YYYY-MM-DD (北京时间) | 信息日期。 用于获取指定日期数据。 由于每个季度的最后一天为财报日，请确保传入正确的日期，例如：2017-03-31、2017-06-30、2017-09-30、2017-12-31 或 latest。 其中，传入 **latest** 会得到最近1.1年内的最新财报数据。 需要注意的是，startDate和date至少要传一个。 |
| startDate | No | String: YYYY-MM-DD (北京时间) | 信息起始时间。 用于获取一定时间范围内的数据。 **开始和结束的时间间隔不超过10年** 需要注意的是，startDate和date至少要传一个。 |
| endDate | No | String: YYYY-MM-DD (北京时间) | 信息结束时间。 用于获取一定时间范围内的数据。 默认值是上周一。 需要注意的是，请与startDate一起使用。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[tableName].[fieldName].[expressionCalculateType]。 比如，你想获取营业总收入累计原始值以及应收账款当期同比值，对应的metricsList设置为：["q.ps.toi.t", "q.bs.ar.c_y2y"]。 需要注意的是，当stockCodes长度大于1时最多只能选取48个指标；当stockCodes长度等于1时最多只能获取128 个指标。 **当前支持:** granularity 年 : `y`; 半年 : `hy`; 季度 : `q` expressionCalculateType 资产负债表: 年(y): 当期 :t当期回溯值 :t_r当期同比 :t_y2y当期环比 :t_c2c半年(hy): 当期 :t当期回溯值 :t_r当期同比 :t_y2y当期环比 :t_c2c半年 :c半年回溯值 :c_r半年同比 :c_y2y半年环比 :c_c2c季度(q): 当期 :t当期回溯值 :t_r当期同比 :t_y2y当期环比 :t_c2c单季 :c单季回溯值 :c_r单季同比 :c_y2y单季环比 :c_c2c; 利润表: 年(y): 累积 :t累积回溯值 :t_r累积同比 :t_y2y半年(hy): 累积 :t累积回溯值 :t_r累积同比 :t_y2y累积环比 :t_c2c半年 :c半年回溯值 :c_r半年同比 :c_y2y半年环比 :c_c2c半年年比 :c_2yTTM :ttmTTM同比 :ttm_y2yTTM环比 :ttm_c2c季度(q): 累积 :t累积回溯值 :t_r累积同比 :t_y2y累积环比 :t_c2c单季 :c单季回溯值 :c_r单季同比 :c_y2y单季环比 :c_c2c单季年比 :c_2yTTM :ttmTTM同比 :ttm_y2yTTM环比 :ttm_c2c; 现金流量表: 年(y): 累积 :t累积回溯值 :t_r累积同比 :t_y2y半年(hy): 累积 :t累积回溯值 :t_r累积同比 :t_y2y累积环比 :t_c2c半年 :c半年回溯值 :c_r半年同比 :c_y2y半年环比 :c_c2c半年年比 :c_2yTTM :ttmTTM同比 :ttm_y2yTTM环比 :ttm_c2c季度(q): 累积 :t累积回溯值 :t_r累积同比 :t_y2y累积环比 :t_c2c单季 :c单季回溯值 :c_r单季同比 :c_y2y单季环比 :c_c2c单季年比 :c_2yTTM :ttmTTM同比 :ttm_y2yTTM环比 :ttm_c2c tableName.fieldName 资产负债表 一、资产总计 : bs.ta现金及存放中央银行款项 : bs.cabwcb(其中)现金 : bs.c(其中)存放中央银行款项 : bs.bwcb存放同业及其他金融机构款项 : bs.bwbaofi贵金属 : bs.pm拆出资金 : bs.pwbaofi买入返售金融资产 : bs.fahursa发放贷款及垫款 : bs.laatc衍生金融资产 : bs.dfa金融投资： : bs.t_fi#以公允价值计量且其变动计入当期损益的金融投资 : bs.fiafvtpol#以摊余成本计量的金融投资 : bs.fiaac#以公允价值计量且其变动计入其他综合收益的金融投资 : bs.fiafvtoci#以公允价值计量且其变动计入其他综合收益的债务工具投资 : bs.diafvtoci#指定为以公允价值计量且其变动计入其他综合收益的权益工具投资 : bs.deiafvtoci#可供出售金融资产 : bs.afsfa#持有至到期投资 : bs.htmi#应收款项投资 : bs.ri应收利息 : bs.ir长期应收款 : bs.ltar长期股权投资 : bs.ltei投资性房地产 : bs.rei固定资产 : bs.fa固定资产占总资产比率 : bs.fa_ta_r在建工程 : bs.cip使用权资产 : bs.roua无形资产 : bs.ia商誉 : bs.gw商誉占净资产比率 : bs.gw_toe_r递延所得税资产 : bs.dita其他资产 : bs.oa二、负债合计 : bs.tl资产负债率 : bs.tl_ta_r向中央银行借款 : bs.bfcb同业存入及拆入 : bs.dapfbaofi(其中)同业及其他金融机构存放款项 : bs.dfbaofi(其中)拆入资金 : bs.pfbaofi衍生金融负债 : bs.dfl以公允价值计量且其变动计入当期损益的金融负债 : bs.flafvtpol卖出回购金融资产 : bs.fasurpa客户存款 : bs.cd应付职工薪酬 : bs.sawp应交税费 : bs.tp合同负债 : bs.cl租赁负债 : bs.ll预计负债 : bs.al应付利息 : bs.intp应付债券 : bs.bp递延所得税负债 : bs.ditl其他负债 : bs.ol三、所有者权益合计 : bs.toe股东权益占比 : bs.toe_ta_r股本 : bs.sc其他权益工具 : bs.oei(其中)优先股 : bs.psioei(其中)永续债 : bs.pcsioei资本公积 : bs.capr减：库存股 : bs.is其他综合收益 : bs.oci专项储备 : bs.rr盈余公积 : bs.surr一般风险准备金 : bs.pogr未分配利润 : bs.rtp外币报表折算差额 : bs.er归属于母公司股东及其他权益持有者的权益合计 : bs.tetshaoehopc归属于母公司普通股股东权益合计 : bs.tetoshopc少数股东权益 : bs.etmsh四、核心指标五、贷款质量贷款和垫款总额 : bs.tlaatc(其中)正常类贷款 : bs.p_pf(其中)关注类贷款 : bs.sm_pf(其中)不良贷款余额 : bs.npl次级类贷款 : bs.s_npl可疑类贷款 : bs.d_npl损失类贷款 : bs.l_npl(其中)逾期贷款 : bs.tol(其中)逾期90天贷款 : bs.lofmt3m(其中)重组贷款 : bs.rl(其中)逾期超过90天的重组贷款 : bs.rlofmt90d(其中)贷款损失准备 : bs.llr正常类贷款迁徙率 : bs.p_pf_mr关注类贷款迁徙率 : bs.sm_pf_mr次级类贷款迁徙率 : bs.s_npl_mr可疑类贷款迁徙率 : bs.d_npl_mr不良率 : bs.npl_tlaatc_r拨贷比 : bs.llr_tlaatc_r不良贷款拨备覆盖率 : bs.llr_npl_r逾期贷款率 : bs.tol_tlaatc_r逾期90天贷款率 : bs.lofmt3m_tlaatc_r重组贷款率 : bs.rl_tlaatc_r逾期90天重组贷款率 : bs.rlofmt90d_tlaatc_r六、员工情况员工人数 : bs.ep_stn七、股本、股东以及估值市值 : bs.mc总股本 : bs.tsc流通股本 : bs.csc总股东人数(季度) : bs.shnA股股东人数(季度) : bs.shn_om 利润表 一、营业收入 : ps.oi净利息收入 : ps.nii(其中)利息收入 : ps.ii(其中)利息支出 : ps.ie净息收入占比 : ps.nii_bi_r非息收入 : ps.nonii非息收入占比 : ps.nonii_bi_r手续费及佣金净收入 : ps.nfaci(其中)手续费及佣金收入 : ps.faci(其中)手续费及佣金支出 : ps.face公允价值变动收益 : ps.ciofv投资收益 : ps.ivi(其中)对联营企业及合营企业的投资收益 : ps.iifaajv汇兑收益 : ps.ei其他业务收入 : ps.ooi二、营业支出 : ps.oe税金及附加 : ps.tas业务及管理费用 : ps.baae其他业务成本 : ps.ooe收入成本比 : ps.c_i_r信用减值损失 : ps.cilor资产减值损失 : ps.ailor其他资产减值损失 : ps.oail三、营业利润 : ps.op营业利润率 : ps.op_s_r加：营业外收入 : ps.noi减：营业外支出 : ps.noe四、利润总额 : ps.tp减：所得税费用 : ps.ite有效税率 : ps.ite_tp_r五、净利润 : ps.np净利润率 : ps.np_s_r(一)持续经营净利润 : ps.npfco(二)终止经营净利润 : ps.npfdco归属于母公司股东及其他权益持有者的净利润 : ps.npatshaoehopc归属于母公司普通股股东的净利润 : ps.npatoshopc少数股东损益 : ps.npatmsh归属于母公司普通股股东的扣除非经常性损益的净利润 : ps.npadnrpatoshaopc扣非净利润占比 : ps.npadnrpatoshaopc_npatoshopc_r九、分红、融资及涨跌幅分红金额 : ps.daA股分红金额 : ps.da_omA股融资金额 : ps.fa_om十、客户及供应商 现金流量表 一、经营活动产生的现金流量发放贷款及垫款的净减少额 : cfs.ndilaatc向中央银行借款净增加额 : cfs.niibfcb客户存款和同业及其他金融机构存放款项净增加额 : cfs.niicdadfbaofi(其中)客户存款净增加额 : cfs.niicd(其中)同业及其他金融机构存放款项净增加额 : cfs.niidfbaofi存放中央银行和同业及其他金融机构款项净减少额 : cfs.ndibwcbbaofi(其中)存放中央银行款项净减少额 : cfs.ndibwcb(其中)存放同业及其他金融机构款项净减少额 : cfs.ndibwbaofi拆入资金及卖出回购金融资产净增加额 : cfs.niipfbaoiafasurpa(其中)拆入资金净增加额 : cfs.niipfbaofi(其中)卖出回购业务资金净增加额 : cfs.niifasurpaioa拆出资金及买入返售金融资产净减少额 : cfs.ndipwbaofiafahursa(其中)拆出资金净减少额 : cfs.ndipwbaofi(其中)买入返售金融资产款净减少额 : cfs.ndifahursaioa为交易目的而持有的金融资产净减少额 : cfs.ndifahftp收取利息、手续费及佣金的现金 : cfs.crfifac收到的其他与经营活动有关现金 : cfs.crrtooa经营活动现金流入小计 : cfs.stciffoa发放贷款及垫款的净增加额 : cfs.niilaatc向中央银行借款净减少额 : cfs.ndibfcb客户存款和同业及其他金融机构存放款项净减少额 : cfs.ndicdadfbaofi(其中)客户存款净减少额 : cfs.ndicd(其中)同业及其他金融机构存放款项净减少额 : cfs.ndidfbaofi存放中央银行和同业及其他金融机构款项净增加额 : cfs.niibwcbbaofi(其中)存放中央银行款净增加额 : cfs.niibwcb(其中)存放同业及其他金融机构款项净增加额 : cfs.niibwbaofi拆入资金及卖出回购金融资产款净减少额 : cfs.ndipfbaofiafasurpa(其中)拆入资金净减少额 : cfs.ndipfbaofi(其中)卖出回购业务资金净减少额 : cfs.ndifasurpaioa拆出资金及买入返售金融资产净增加额 : cfs.niipwbaofiafahursa(其中)拆出资金增加额 : cfs.niipwbaofi(其中)买入返售金融资产净增加额 : cfs.niifahursaioa为交易目的而持有的金融资产净增加额 : cfs.niifahftp支付利息、手续费及佣金的现金 : cfs.cpfifac支付给职工及为职工支付的现金 : cfs.cptofe支付的各种税费 : cfs.cpft支付的其他与经营活动有关现金 : cfs.cprtooa经营活动现金流出小计 : cfs.stcoffoa经营活动产生的现金流量净额 : cfs.ncffoa二、投资活动产生的现金流量金额收回投资收到的现金 : cfs.crfrci取得投资收益所收到的现金 : cfs.crfii处置固定资产、无形资产及其他长期资产收到的现金 : cfs.crfdofiaolta处置子公司、合营联营企业及其他营业单位收到的现金净额 : cfs.ncrfdossajvaou(其中)处置子公司或其他营业单位收到的现金净额 : cfs.ncrfdossaou(其中)处置合营或联营公司所收到的现金 : cfs.ncrfdoaajv收到的其他与投资活动相关的现金 : cfs.crrtoia投资活动现金流入小计 : cfs.stcifia投资所支付的现金 : cfs.cpfi购建固定资产、无形资产及其他长期资产所支付的现金 : cfs.cpfpfiaolta取得子公司、合营联营企业及其他营业单位支付的现金净额 : cfs.ncpfbssajvaou(其中)取得子公司及其营业单位支付的现金净额 : cfs.ncpfbssaou(其中)取得联营及合营公司支付的现金净额 : cfs.ncpfbajv支付的其他与投资活动有关的现金 : cfs.cprtoia投资活动现金流出小计 : cfs.stcoffia投资活动产生的现金流量净额 : cfs.ncffia三、筹资活动产生的现金流量吸收投资收到的现金 : cfs.crfai(其中)子公司吸收少数股东投资收到的现金 : cfs.crfamshibss资产证券化收到的现金 : cfs.crfas发行存款证收到的现金 : cfs.crfdc发行债券收到的现金 : cfs.crfib发行同业存单收到的现金 : cfs.crfnibcod发行永续债收到的现金 : cfs.crfipcs上市募集资金总额 : cfs.crfipo收到的其他与筹资活动有关的现金 : cfs.crrtofa筹资活动产生的现金流入小计 : cfs.stcifffa偿还已发行存款证支付的现金 : cfs.cpfdcrp偿付债务支付的现金 : cfs.cpfbrp偿还已发行同业存单支付的现金 : cfs.cpfnibcodrp偿还债券利息支付的现金 : cfs.cpfbip分配股利、利润或偿付利息所支付的现金 : cfs.cpfdapdoi(其中)子公司支付少数股东股利及利润 : cfs.cpfdapomshpbss赎回非控制性权益支付的现金 : cfs.cpfncer支付新股发行费用 : cfs.cpfipo支付的其他与筹资活动有关的现金 : cfs.cprtofa筹资活动产生的现金流出小计 : cfs.stcofffa筹资活动产生的现金流量净额 : cfs.ncfffa四、汇率变动对现金及现金等价物的影响 : cfs.iocacedtfier期初现金及现金等价物的余额 : cfs.bocaceatpb现金及现金等价物的净增加额 : cfs.niicace期末现金及现金等价物净余额 : cfs.bocaceatpe五、附注净利润 : cfs.np加：资产减值准备 : cfs.ioa信用减值损失 : cfs.cilor固定资产折旧、油气资产折耗、生产性生物资产折旧 : cfs.dofx_dooaga_dopba投资性房地产的折旧及摊销 : cfs.daaorei使用权资产摊销 : cfs.aoroua无形资产摊销 : cfs.aoia长期待摊费用摊销 : cfs.aoltde处置固定资产、无形资产和其他长期资产的损失 : cfs.lodofaiaaolta固定资产报废损失 : cfs.lfsfa公允价值变动损失 : cfs.lfcifv财务费用 : cfs.fe投资损失 : cfs.il递延所得税资产减少 : cfs.didita递延所得税负债增加 : cfs.iiditl存货的减少 : cfs.dii经营性应收项目的减少 : cfs.dior经营性应付项目的增加 : cfs.iiop其他 : cfs.o一年内到期的可转换公司债券 : cfs.cbdwioy融资租入固定资产 : cfs.flofa经营活动产生的现金流量净额 : cfs.ncffoa_dup 财务指标 一、人均指标员工人数 : m.ep_stn (expressionCalculateType参考资产负债表) 人均营业收入 : m.oi_pc (expressionCalculateType参考利润表) 人均净利润 : m.np_pc (expressionCalculateType参考利润表) 人均薪酬 : m.s_pc (expressionCalculateType参考现金流量表) 二、银行特有指标客户存款 : m.cd (expressionCalculateType参考资产负债表) 发放贷款及垫款 : m.laatc (expressionCalculateType参考资产负债表) 贷存比 : m.laatc_cd_r (expressionCalculateType参考资产负债表) 贷款和垫款总额 : m.tlaatc (expressionCalculateType参考资产负债表) 关注类贷款 : m.sm_pf (expressionCalculateType参考资产负债表) 不良贷款余额 : m.npl (expressionCalculateType参考资产负债表) 贷款损失准备 : m.llr (expressionCalculateType参考资产负债表) 逾期贷款 : m.tol (expressionCalculateType参考资产负债表) 逾期90天贷款 : m.lofmt3m (expressionCalculateType参考资产负债表) 重组贷款 : m.rl (expressionCalculateType参考资产负债表) 逾期超过90天的重组贷款 : m.rlofmt90d (expressionCalculateType参考资产负债表) 不良率 : m.npl_tlaatc_r (expressionCalculateType参考资产负债表) 不良贷款拨备覆盖率 : m.llr_npl_r (expressionCalculateType参考资产负债表) 拨贷比 : m.llr_tlaatc_r (expressionCalculateType参考资产负债表) 逾期贷款率 : m.tol_tlaatc_r (expressionCalculateType参考资产负债表) 逾期90天贷款率 : m.lofmt3m_tlaatc_r (expressionCalculateType参考资产负债表) 重组贷款率 : m.rl_tlaatc_r (expressionCalculateType参考资产负债表) 逾期90天重组贷款率 : m.rlofmt90d_tlaatc_r (expressionCalculateType参考资产负债表) 三、每股指标总股本 : m.tsc (expressionCalculateType参考资产负债表) 归属于母公司普通股股东的每股收益 : m.npatoshopc_ps (expressionCalculateType参考利润表) 归属于母公司普通股股东的每股扣非收益 : m.npadnrpatoshaopc_ps (expressionCalculateType参考利润表) 归属于母公司普通股股东的每股股东权益 : m.tetoshopc_ps (expressionCalculateType参考资产负债表) 每股资本公积 : m.cr_ps (expressionCalculateType参考资产负债表) 每股未分配利润 : m.rp_ps (expressionCalculateType参考资产负债表) 每股分红 : m.da_ps (expressionCalculateType参考利润表) 每股经营活动产生的现金流量 : m.stciffoa_ps (expressionCalculateType参考现金流量表) 每股经营活动产生的现金流量净额 : m.ncffoa_ps (expressionCalculateType参考现金流量表) 四、盈利能力归属于少数股股东的ROE : m.roe_atomsh (expressionCalculateType参考利润表) 归属于母公司普通股股东的ROE : m.roe_atoshaopc (expressionCalculateType参考利润表) 归属于母公司普通股股东的扣非ROE : m.roe_adnrpatoshaopc (expressionCalculateType参考利润表) 净资产收益率(ROE) : m.roe (expressionCalculateType参考利润表) 杠杆倍数 : m.l (expressionCalculateType参考资产负债表) 总资产收益率(ROA) : m.roa (expressionCalculateType参考利润表) 总资产周转率 : m.ta_to (expressionCalculateType参考利润表) 净利润率 : m.np_s_r (expressionCalculateType参考利润表) 五、营运能力(周转率)固定资产周转率 : m.fa_tor (expressionCalculateType参考利润表) 六、营运能力(周转天数)固定资产周转天数 : m.fa_ds (expressionCalculateType参考利润表) 股东权益周转天数 : m.toe_ds (expressionCalculateType参考利润表) 总资产周转天数 : m.ta_ds (expressionCalculateType参考利润表) 七、偿债及资本结构资产负债率 : m.tl_ta_r (expressionCalculateType参考资产负债表) 固定资产占总资产比率 : m.fa_ta_r (expressionCalculateType参考资产负债表) 八、现金流量自由现金流量 : m.fcf (expressionCalculateType参考现金流量表) 经投融产生的现金流量净额 : m.ncffoaiafa (expressionCalculateType参考现金流量表) 经营活动产生的现金流量净额对营业利润的比率 : m.ncffoa_op_r (expressionCalculateType参考利润表) 经营活动产生的现金流量净额对净利润的比率 : m.ncffoa_np_r (expressionCalculateType参考利润表) 经营活动产生的现金流量净额对固定资产的比率 : m.ncffoa_fa_r (expressionCalculateType参考现金流量表) |

### 示例

```json
{
    "date": "2025-09-30",
    "stockCodes": [
        "480000"
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
                        "t": 4320475250898
                    }
                }
            },
            "stockCode": "480000"
        }
    ]
}
```
