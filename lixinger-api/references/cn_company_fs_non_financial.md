# API文档/大陆/公司接口/财务报表/非金融

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/cn/company/fs/non_financial
> API Key: `cn/company/fs/non_financial`

---

## 财报数据API

**简要描述:** 获取财务数据，如营业收入、ROE等。

**请求URL:** `https://open.lixinger.com/api/cn/company/fs/non_financial`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/cn/company/fs/non_financial](https://www.lixinger.com/api/open-api/html-doc/cn/company/fs/non_financial)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 股票代码数组。 stockCodes长度>=1且<=100，格式如下：["300750","600519","600157"]。 请参考 股票信息API 获取合法的stockCode。 需要注意的是，当传入startDate时只能传入一个股票代码。 |
| date | No | String: latest \| YYYY-MM-DD (北京时间) | 信息日期。 用于获取指定日期数据。 由于每个季度的最后一天为财报日，请确保传入正确的日期，例如：2017-03-31、2017-06-30、2017-09-30、2017-12-31 或 latest。 其中，传入 **latest** 会得到最近1.1年内的最新财报数据。 需要注意的是，startDate和date至少要传一个。 |
| startDate | No | String: YYYY-MM-DD (北京时间) | 信息起始时间。 用于获取一定时间范围内的数据。 **开始和结束的时间间隔不超过10年** 需要注意的是，startDate和date至少要传一个。 |
| endDate | No | String: YYYY-MM-DD (北京时间) | 信息结束时间。 用于获取一定时间范围内的数据。 默认值是上周一。 需要注意的是，请与startDate一起使用。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| metricsList | Yes | Array | 指标数组，指标格式为[granularity].[tableName].[fieldName].[expressionCalculateType]。 比如，你想获取营业总收入累计原始值以及应收账款当期同比值，对应的metricsList设置为：["q.ps.toi.t", "q.bs.ar.c_y2y"]。 需要注意的是，当stockCodes长度大于1时最多只能选取48个指标；当stockCodes长度等于1时最多只能获取128 个指标。 **当前支持:** granularity 年 : `y`; 半年 : `hy`; 季度 : `q` expressionCalculateType 资产负债表: 年(y): 当期 :t当期回溯值 :t_r当期同比 :t_y2y当期环比 :t_c2c半年(hy): 当期 :t当期回溯值 :t_r当期同比 :t_y2y当期环比 :t_c2c半年 :c半年回溯值 :c_r半年同比 :c_y2y半年环比 :c_c2c季度(q): 当期 :t当期回溯值 :t_r当期同比 :t_y2y当期环比 :t_c2c单季 :c单季回溯值 :c_r单季同比 :c_y2y单季环比 :c_c2c; 利润表: 年(y): 累积 :t累积回溯值 :t_r累积同比 :t_y2y半年(hy): 累积 :t累积回溯值 :t_r累积同比 :t_y2y累积环比 :t_c2c半年 :c半年回溯值 :c_r半年同比 :c_y2y半年环比 :c_c2c半年年比 :c_2yTTM :ttmTTM同比 :ttm_y2yTTM环比 :ttm_c2c季度(q): 累积 :t累积回溯值 :t_r累积同比 :t_y2y累积环比 :t_c2c单季 :c单季回溯值 :c_r单季同比 :c_y2y单季环比 :c_c2c单季年比 :c_2yTTM :ttmTTM同比 :ttm_y2yTTM环比 :ttm_c2c; 现金流量表: 年(y): 累积 :t累积回溯值 :t_r累积同比 :t_y2y半年(hy): 累积 :t累积回溯值 :t_r累积同比 :t_y2y累积环比 :t_c2c半年 :c半年回溯值 :c_r半年同比 :c_y2y半年环比 :c_c2c半年年比 :c_2yTTM :ttmTTM同比 :ttm_y2yTTM环比 :ttm_c2c季度(q): 累积 :t累积回溯值 :t_r累积同比 :t_y2y累积环比 :t_c2c单季 :c单季回溯值 :c_r单季同比 :c_y2y单季环比 :c_c2c单季年比 :c_2yTTM :ttmTTM同比 :ttm_y2yTTM环比 :ttm_c2c tableName.fieldName 资产负债表 一、资产总计 : bs.ta净营运资本 : bs.nwc流动资产合计 : bs.tca流动资产占比 : bs.tca_ta_r货币资金 : bs.cabb货币资金占比 : bs.cabb_ta_r结算备付金 : bs.sr拆出资金 : bs.pwbaofi交易性金融资产 : bs.tfa衍生金融资产(流动) : bs.cdfa应收票据及应收账款 : bs.nraar(其中)应收票据 : bs.nr(其中)应收账款 : bs.ar应收款项融资 : bs.rf预付款项 : bs.ats应收保费 : bs.pr应收分保账款 : bs.rir应收分保合同准备金 : bs.crorir其他应收款 : bs.or(其中)应收利息 : bs.ir(其中)应收股利 : bs.dr买入返售金融资产 : bs.fahursa存货 : bs.i(其中)数据资源 : bs.i_dr合同资产 : bs.ca持有待售资产 : bs.ahfs发放贷款及垫款(流动) : bs.claatc待摊费用 : bs.pe一年内到期的非流动资产 : bs.ncadwioy其他流动资产 : bs.oca流动比率 : bs.tca_tcl_r速动比率 : bs.q_r非流动资产合计 : bs.tnca非流动资产占比 : bs.tnca_ta_r重资产占比 : bs.ah_ta_r发放贷款及垫款(非流动) : bs.nclaatc债权投资 : bs.cri其他债权投资 : bs.ocri可供出售金融资产(非流动) : bs.ncafsfa持有至到期投资 : bs.htmi长期应收款 : bs.ltar长期股权投资 : bs.ltei其他权益工具投资 : bs.oeii其他非流动金融资产 : bs.oncfa投资性房地产 : bs.rei固定资产 : bs.fa(其中)固定资产清理 : bs.dofa固定资产占总资产比率 : bs.fa_ta_r在建工程 : bs.cip(其中)工程物资 : bs.es在建工程占固定资产比率 : bs.cip_fa_r生产性生物资产 : bs.pba油气资产 : bs.oaga公益性生物资产 : bs.pwba使用权资产 : bs.roua无形资产 : bs.ia(其中)数据资源 : bs.ia_dr开发支出 : bs.rade(其中)数据资源 : bs.rade_dr商誉 : bs.gw商誉占净资产比率 : bs.gw_toe_r长期待摊费用 : bs.ltpe递延所得税资产 : bs.dita其他非流动资产 : bs.onca二、负债合计 : bs.tl有息负债 : bs.lwi有息负债率 : bs.lwi_ta_r资产负债率 : bs.tl_ta_r流动负债合计 : bs.tcl流动负债占比 : bs.tcl_tl_r短期借款 : bs.stl向中央银行借款 : bs.bfcb拆入资金 : bs.pfbaofi衍生金融负债 : bs.dfl交易性金融负债 : bs.tfl应付票据及应付账款 : bs.npaap(其中)应付票据 : bs.np(其中)应付账款 : bs.ap预收账款 : bs.afc合同负债 : bs.cl卖出回购金融资产 : bs.fasurpa吸收存款及同业存放 : bs.dfcab代理买卖证券款 : bs.stoa代理承销证券款 : bs.ssoa应付职工薪酬 : bs.sawp应交税费 : bs.tp其他应付款 : bs.oap(其中)应付利息 : bs.intp(其中)应付股利 : bs.dp应付手续费及佣金 : bs.facp应付分保账款 : bs.rip持有待售负债 : bs.lhfs一年内到期的非流动负债 : bs.ncldwioy一年内到期的递延收益 : bs.didwioy预计负债(流动) : bs.cal短期应付债券 : bs.stbp其他流动负债 : bs.ocl非流动负债合计 : bs.tncl非流动负债占比 : bs.tncl_tl_r保险合同准备金 : bs.icr长期借款 : bs.ltl应付债券 : bs.bp(其中)优先股 : bs.psibp(其中)永续债 : bs.pcsibp租赁负债 : bs.ll长期应付款 : bs.ltap(其中)专项应付款 : bs.sap长期应付职工薪酬 : bs.ltpoe预计负债(非流动) : bs.ncal长期递延收益 : bs.ltdi递延所得税负债 : bs.ditl其他非流动负债 : bs.oncl三、所有者权益合计 : bs.toe股东权益占比 : bs.toe_ta_r股本 : bs.sc其他权益工具 : bs.oei(其中)优先股 : bs.psioei(其中)永续债 : bs.pcsioei资本公积 : bs.capr减：库存股 : bs.is其他综合收益 : bs.oci专项储备 : bs.rr盈余公积 : bs.surr一般风险准备金 : bs.pogr未分配利润 : bs.rtp外币报表折算差额 : bs.er归属于母公司股东及其他权益持有者的权益合计 : bs.tetshaoehopc归属于母公司普通股股东权益合计 : bs.tetoshopc归属于母公司普通股股东的每股股东权益 : bs.tetoshopc_ps少数股东权益 : bs.etmsh四、员工情况员工人数 : bs.ep_stn博士人数 : bs.ep_pn硕士人数 : bs.ep_mn学士人数 : bs.ep_bn大专人数 : bs.ep_jcn高中及以下人数 : bs.ep_hsabn生产人员人数 : bs.ep_psn销售人员人数 : bs.ep_spn技术人员人数 : bs.ep_tsn财务人员人数 : bs.ep_fon行政人员人数 : bs.ep_asn其他人员人数 : bs.ep_osn五、股本、股东以及估值市值 : bs.mc总股本 : bs.tsc流通股本 : bs.csc总股东人数(季度) : bs.shnA股股东人数(季度) : bs.shn_om第一大股东持仓占总股本比例 : bs.shbt1sh_tsc_r前十大股东持仓占总股本比例 : bs.shbt10sh_tsc_r前十大流通股东持仓占流通股本比例 : bs.shbt10sh_csc_r进公募基金前十大持仓占流通股本比例 : bs.shbt10poof_csc_r公募基金持仓占流通股本比例 : bs.shbpoof_csc_r公募基金+自由流通股东持仓占自由流通股本比例 : bs.shbeosh_poof_ecsc_rPE-TTM : bs.pe_ttmPE-TTM(扣非) : bs.d_pe_ttmPB : bs.pbPB(不含商誉) : bs.pb_wo_gwPS-TTM : bs.ps_ttmPCF-TTM : bs.pcf_ttm股息率 : bs.dyr 利润表 一、营业总收入 : ps.toi营业收入 : ps.oi利息收入 : ps.ii已赚保费 : ps.ep手续费及佣金收入 : ps.faci其他业务收入 : ps.ooi二、营业总成本 : ps.toc营业成本 : ps.oc毛利率(GM) : ps.gp_m利息支出 : ps.ie手续费及佣金支出 : ps.face退保金 : ps.s保险合同赔付支出 : ps.ce提取保险责任准备金净额 : ps.iiicr保单红利支出 : ps.phdrfpip分保费用 : ps.rie税金及附加 : ps.tas销售费用 : ps.se管理费用 : ps.ae研发费用 : ps.rade(备注)资本化研发支出 : ps.crade(备注)资本化研发支出占比 : ps.crade_r财务费用 : ps.fe(其中)利息费用 : ps.ieife(其中)利息收入 : ps.iiife销售费用率 : ps.se_r管理费用率 : ps.ae_r研发费用率 : ps.rade_r财务费用率 : ps.fe_r营业费用率 : ps.oe_r四项费用率 : ps.foe_r加：其他收益 : ps.oic投资收益 : ps.ivi(其中)对联营企业及合营企业的投资收益 : ps.iifaajv(其中)以摊余成本计量的金融资产终止确认产生的投资收益 : ps.iftdofamaac汇兑收益 : ps.ei净敞口套期收益 : ps.nehb公允价值变动收益 : ps.ciofv信用减值损失 : ps.cilor资产减值损失 : ps.ailor其他资产减值损失 : ps.oail资产处置收益 : ps.adi其他业务成本 : ps.ooe核心利润 : ps.cp核心利润率 : ps.cp_r三、营业利润 : ps.op营业利润率 : ps.op_s_r其他营业利润率 : ps.op_op_r加：营业外收入 : ps.noi(其中)非流动资产毁损报废利得 : ps.ncadarg减：营业外支出 : ps.noe(其中)非流动资产毁损报废损失 : ps.ncadarl四、利润总额 : ps.tp研发费占利润总额比值 : ps.rade_tp_r息税前净利润(EBIT) : ps.ebit息税折旧及摊销前盈利(EBITDA) : ps.ebitda减：所得税费用 : ps.ite有效税率 : ps.ite_tp_r五、净利润 : ps.np净利润率 : ps.np_s_r(一)持续经营净利润 : ps.npfco(二)终止经营净利润 : ps.npfdco归属于母公司股东及其他权益持有者的净利润 : ps.npatshaoehopc归属于母公司普通股股东的净利润 : ps.npatoshopc少数股东损益 : ps.npatmsh归属于母公司普通股股东的扣除非经常性损益的净利润 : ps.npadnrpatoshaopc扣非净利润占比 : ps.npadnrpatoshaopc_npatoshopc_r归属于母公司普通股股东的加权ROE : ps.wroe归属于母公司普通股股东的扣非加权ROE : ps.wdroe六、基本每股收益 : ps.beps稀释每股收益 : ps.deps七、综合收益总额 : ps.tci归属于母公司股东及其他权益持有者的综合收益总额 : ps.tciatshaoehopc归属于母公司普通股股东的综合收益总额 : ps.tciatoshopc归属于少数股东的综合收益总额 : ps.tciatmsh其他综合收益的税后净额 : ps.natooci八、区域收入境内收入 : ps.d_oi境内营业成本 : ps.d_oc境内收入占比 : ps.d_oi_r境内毛利率 : ps.d_gp_m海外收入 : ps.o_oi海外营业成本 : ps.o_oc海外收入占比 : ps.o_oi_r海外毛利率 : ps.o_gp_m九、分红、融资及涨跌幅分红金额 : ps.da分红率 : ps.d_np_rA股分红金额 : ps.da_omA股融资金额 : ps.fa_om年度涨跌幅 : ps.spc_a十、客户及供应商前五大客户收入占比 : ps.tfci_r前五大供应商采购占比 : ps.tfsp_r 现金流量表 一、经营活动产生的现金流量销售商品、提供劳务收到的现金 : cfs.crfscapls发放贷款及垫款的净减少额 : cfs.ndilaatc客户存款和同业及其他金融机构存放款项净增加额 : cfs.niicdadfbaofi向中央银行借款净增加额 : cfs.niibfcb向其他金融机构拆入资金净增加额 : cfs.niipfofi收到原保险合同保费取得的现金 : cfs.crfp收到再保险业务现金净额 : cfs.ncrfrib保户储金及投资款净增加额 : cfs.niiphd为交易目的而持有的金融资产净减少额 : cfs.ndifahftp拆入资金净增加额 : cfs.niipfbaofi卖出回购业务资金净增加额 : cfs.niifasurpaioa收取利息、手续费及佣金的现金 : cfs.crfifac代理买卖证券收到的现金净额 : cfs.ncrfstoa收到的税费返还 : cfs.crfwbot收到的其他与经营活动有关现金 : cfs.crrtooa经营活动现金流入小计 : cfs.stciffoa购买商品、接收劳务支付的现金 : cfs.cpfpcarls发放贷款及垫款的净增加额 : cfs.niilaatc存放中央银行和同业及其他金融机构款项净增加额 : cfs.niibwcbbaofi向其他金融机构拆入资金净减少额 : cfs.ndipfofi支付原保险合同赔付等款项的现金 : cfs.cpfc拆出资金增加额 : cfs.niipwbaofi买入返售金融资产净增加额 : cfs.niifahursaioa支付保单红利的现金 : cfs.cpfphd为交易目的而持有的金融资产净增加额 : cfs.niifahftp支付利息、手续费及佣金的现金 : cfs.cpfifac支付给职工及为职工支付的现金 : cfs.cptofe支付的各种税费 : cfs.cpft支付的其他与经营活动有关现金 : cfs.cprtooa经营活动现金流出小计 : cfs.stcoffoa经营活动产生的现金流量净额 : cfs.ncffoa二、投资活动产生的现金流量金额收回投资收到的现金 : cfs.crfrci取得投资收益所收到的现金 : cfs.crfii处置固定资产、无形资产及其他长期资产收到的现金 : cfs.crfdofiaolta处置子公司、合营联营企业及其他营业单位收到的现金净额 : cfs.ncrfdossajvaou(其中)处置子公司或其他营业单位收到的现金净额 : cfs.ncrfdossaou(其中)处置合营或联营公司所收到的现金 : cfs.ncrfdoaajv收到的其他与投资活动相关的现金 : cfs.crrtoia投资活动现金流入小计 : cfs.stcifia购建固定资产、无形资产及其他长期资产所支付的现金 : cfs.cpfpfiaolta投资所支付的现金 : cfs.cpfi质押贷款净增加额 : cfs.niipl取得子公司、合营联营企业及其他营业单位支付的现金净额 : cfs.ncpfbssajvaou(其中)取得子公司及其营业单位支付的现金净额 : cfs.ncpfbssaou(其中)取得联营及合营公司支付的现金净额 : cfs.ncpfbajv支付的其他与投资活动有关的现金 : cfs.cprtoia投资活动现金流出小计 : cfs.stcoffia投资活动产生的现金流量净额 : cfs.ncffia三、筹资活动产生的现金流量吸收投资收到的现金 : cfs.crfai(其中)子公司吸收少数股东投资收到的现金 : cfs.crfamshibss取得借款收到的现金 : cfs.crfl发行债券收到的现金 : cfs.crfib收到的其他与筹资活动有关的现金 : cfs.crrtofa筹资活动产生的现金流入小计 : cfs.stcifffa偿付债务支付的现金 : cfs.cpfbrp分配股利、利润或偿付利息所支付的现金 : cfs.cpfdapdoi(其中)子公司支付少数股东股利及利润 : cfs.cpfdapomshpbss支付的其他与筹资活动有关的现金 : cfs.cprtofa筹资活动产生的现金流出小计 : cfs.stcofffa筹资活动产生的现金流量净额 : cfs.ncfffa四、汇率变动对现金及现金等价物的影响 : cfs.iocacedtfier期初现金及现金等价物的余额 : cfs.bocaceatpb现金及现金等价物的净增加额 : cfs.niicace期末现金及现金等价物净余额 : cfs.bocaceatpe五、附注净利润 : cfs.np加：资产减值准备 : cfs.ioa信用减值损失 : cfs.cilor固定资产折旧、油气资产折耗、生产性生物资产折旧 : cfs.dofx_dooaga_dopba投资性房地产的折旧及摊销 : cfs.daaorei使用权资产摊销 : cfs.aoroua无形资产摊销 : cfs.aoia长期待摊费用摊销 : cfs.aoltde处置固定资产、无形资产和其他长期资产的损失 : cfs.lodofaiaaolta固定资产报废损失 : cfs.lfsfa公允价值变动损失 : cfs.lfcifv财务费用 : cfs.fe投资损失 : cfs.il递延所得税资产减少 : cfs.didita递延所得税负债增加 : cfs.iiditl存货的减少 : cfs.dii经营性应收项目的减少 : cfs.dior经营性应付项目的增加 : cfs.iiop其他 : cfs.o一年内到期的可转换公司债券 : cfs.cbdwioy融资租入固定资产 : cfs.flofa经营活动产生的现金流量净额 : cfs.ncffoa_dup 财务指标 一、人均指标员工人数 : m.ep_stn (expressionCalculateType参考资产负债表) 人均营业总收入 : m.toi_pc (expressionCalculateType参考利润表) 人均净利润 : m.np_pc (expressionCalculateType参考利润表) 人均薪酬 : m.s_pc (expressionCalculateType参考现金流量表) 二、每股指标总股本 : m.tsc (expressionCalculateType参考资产负债表) 归属于母公司普通股股东的每股收益 : m.npatoshopc_ps (expressionCalculateType参考利润表) 归属于母公司普通股股东的每股扣非收益 : m.npadnrpatoshaopc_ps (expressionCalculateType参考利润表) 归属于母公司普通股股东的每股股东权益 : m.tetoshopc_ps (expressionCalculateType参考资产负债表) 每股资本公积 : m.cr_ps (expressionCalculateType参考资产负债表) 每股未分配利润 : m.rp_ps (expressionCalculateType参考资产负债表) 每股分红 : m.da_ps (expressionCalculateType参考利润表) 每股经营活动产生的现金流量 : m.stciffoa_ps (expressionCalculateType参考现金流量表) 每股经营活动产生的现金流量净额 : m.ncffoa_ps (expressionCalculateType参考现金流量表) 三、盈利能力归属于母公司普通股股东的加权ROE : m.wroe (expressionCalculateType参考利润表) 归属于母公司普通股股东的扣非加权ROE : m.wdroe (expressionCalculateType参考利润表) 归属于母公司普通股股东的ROE : m.roe_atoshaopc (expressionCalculateType参考利润表) 归属于母公司普通股股东的扣非ROE : m.roe_adnrpatoshaopc (expressionCalculateType参考利润表) 归属于少数股股东的ROE : m.roe_atomsh (expressionCalculateType参考利润表) 净资产收益率(ROE) : m.roe (expressionCalculateType参考利润表) 杠杆倍数 : m.l (expressionCalculateType参考资产负债表) 总资产收益率(ROA) : m.roa (expressionCalculateType参考利润表) 总资产周转率 : m.ta_to (expressionCalculateType参考利润表) 净利润率 : m.np_s_r (expressionCalculateType参考利润表) 毛利率(GM) : m.gp_m (expressionCalculateType参考利润表) 有形资产回报率(ROTA) : m.rota (expressionCalculateType参考利润表) 资本回报率(ROIC) : m.roic (expressionCalculateType参考利润表) 资本收益率(ROC) : m.roc (expressionCalculateType参考利润表) 四、营运能力(周转率)预付账款周转率 : m.ats_tor (expressionCalculateType参考利润表) 合同资产周转率 : m.ca_tor (expressionCalculateType参考利润表) 存货周转率 : m.i_tor (expressionCalculateType参考利润表) 应收票据和应收账款周转率 : m.nraar_tor (expressionCalculateType参考利润表) 应收票据周转率 : m.nr_tor (expressionCalculateType参考利润表) 应收账款周转率 : m.ar_tor (expressionCalculateType参考利润表) 应收款项融资周转率 : m.rf_tor (expressionCalculateType参考利润表) 预收账款周转率 : m.afc_tor (expressionCalculateType参考利润表) 合同负债周转率 : m.cl_tor (expressionCalculateType参考利润表) 应付票据和应付账款周转率 : m.npaap_tor (expressionCalculateType参考利润表) 应付票据周转率 : m.np_tor (expressionCalculateType参考利润表) 应付账款周转率 : m.ap_tor (expressionCalculateType参考利润表) 固定资产周转率 : m.fa_tor (expressionCalculateType参考利润表) 五、营运能力(周转天数)预付账款周转天数 : m.ats_ds (expressionCalculateType参考利润表) 合同资产周转天数 : m.ca_ds (expressionCalculateType参考利润表) 存货周转天数 : m.i_ds (expressionCalculateType参考利润表) 应收票据和应收账款周转天数 : m.nraar_ds (expressionCalculateType参考利润表) 应收票据周转天数 : m.nr_ds (expressionCalculateType参考利润表) 应收账款周转天数 : m.ar_ds (expressionCalculateType参考利润表) 应收款项融资周转天数 : m.rf_ds (expressionCalculateType参考利润表) 预收账款周转天数 : m.afc_ds (expressionCalculateType参考利润表) 合同负债周转天数 : m.cl_ds (expressionCalculateType参考利润表) 应付票据和应付账款周转天数 : m.npaap_ds (expressionCalculateType参考利润表) 应付票据周转天数 : m.np_ds (expressionCalculateType参考利润表) 应付账款周转天数 : m.ap_ds (expressionCalculateType参考利润表) 营业周转天数 : m.b_ds (expressionCalculateType参考利润表) 净现金周转天数(CCC) : m.m_ds (expressionCalculateType参考利润表) 固定资产周转天数 : m.fa_ds (expressionCalculateType参考利润表) 流动资产周转天数 : m.tca_ds (expressionCalculateType参考利润表) 股东权益周转天数 : m.toe_ds (expressionCalculateType参考利润表) 总资产周转天数 : m.ta_ds (expressionCalculateType参考利润表) 六、偿债及资本结构资产负债率 : m.tl_ta_r (expressionCalculateType参考资产负债表) 有息负债率 : m.lwi_ta_r (expressionCalculateType参考资产负债表) 货币资金占流动负债比率 : m.cabb_tcl_r (expressionCalculateType参考资产负债表) 流动比率 : m.c_r (expressionCalculateType参考资产负债表) 速动比率 : m.q_r (expressionCalculateType参考资产负债表) 固定资产占总资产比率 : m.fa_ta_r (expressionCalculateType参考资产负债表) 清算价值比率 : m.lv_r (expressionCalculateType参考资产负债表) 七、现金流量自由现金流量 : m.fcf (expressionCalculateType参考现金流量表) 经投融产生的现金流量净额 : m.ncffoaiafa (expressionCalculateType参考现金流量表) 销售商品提供劳务收到的现金对营业收入的比率 : m.crfscapls_oi_r (expressionCalculateType参考利润表) 经营活动产生的现金流量净额对营业利润的比率 : m.ncffoa_op_r (expressionCalculateType参考利润表) 经营活动产生的现金流量净额对净利润的比率 : m.ncffoa_np_r (expressionCalculateType参考利润表) 销售商品提供劳务收到的现金对总资产的比率 : m.crfscapls_ta_r (expressionCalculateType参考现金流量表) 经营活动产生的现金流量净额对固定资产的比率 : m.ncffoa_fa_r (expressionCalculateType参考现金流量表) |

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
    "date": "2025-09-30",
    "stockCodes": [
        "300750",
        "600519",
        "600157"
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
            "date": "2025-09-30T00:00:00+08:00",
            "currency": "CNY",
            "q": {
                "ps": {
                    "toi": {
                        "t": 283071987000
                    }
                }
            },
            "reportDate": "2025-10-21T00:00:00+08:00",
            "reportType": "third_quarterly_report",
            "standardDate": "2025-09-30T00:00:00+08:00",
            "stockCode": "300750"
        },
        {
            "date": "2025-09-30T00:00:00+08:00",
            "currency": "CNY",
            "q": {
                "ps": {
                    "toi": {
                        "t": 130903889635
                    }
                }
            },
            "reportDate": "2025-10-30T00:00:00+08:00",
            "reportType": "third_quarterly_report",
            "standardDate": "2025-09-30T00:00:00+08:00",
            "stockCode": "600519"
        },
        {
            "date": "2025-09-30T00:00:00+08:00",
            "currency": "CNY",
            "q": {
                "ps": {
                    "toi": {
                        "t": 17728119064
                    }
                }
            },
            "reportDate": "2025-10-30T00:00:00+08:00",
            "reportType": "third_quarterly_report",
            "standardDate": "2025-09-30T00:00:00+08:00",
            "stockCode": "600157"
        }
    ]
}
```
