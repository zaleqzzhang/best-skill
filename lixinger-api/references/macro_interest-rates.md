# API文档/宏观/利率

> Vibe Coding URL: https://www.lixinger.com/api/open-api/html-doc/macro/interest-rates
> API Key: `macro/interest-rates`

---

## 利率API

**简要描述:** 获取利率数据，如活期存款等。

**请求URL:** `https://open.lixinger.com/api/macro/interest-rates`

**url for vibe coding:** [https://www.lixinger.com/api/open-api/html-doc/macro/interest-rates](https://www.lixinger.com/api/open-api/html-doc/macro/interest-rates)

**请求方式:** POST

**参数:**

| 参数名称 | 必选 | 数据类型 | 说明 |
| --- | --- | --- | --- |
| token | Yes | String | 我的Token 页有用户专属且唯一的Token。 |
| startDate | Yes | String: YYYY-MM-DD (北京时间) | 信息起始时间。 **开始和结束的时间间隔不超过10年** |
| endDate | Yes | String: YYYY-MM-DD (北京时间) | 信息结束时间。 |
| limit | No | Number | 返回最近数据的数量。 limit仅在请求数据为date range的情况下生效。 |
| areaCode | Yes | String | 区域编码，如{areaCode}。 **当前支持:** 大陆: `cn`; 香港: `hk`; 美国: `us` |
| metricsList | Yes | Array | 指标数组。如['rmb_bdirofi_d']。 大陆支持: 活期存款 : `rmb_bdirofi_d`; 定期存款（三个月） : `rmb_bdirofi_m3`; 定期存款（半年） : `rmb_bdirofi_hy`; 定期存款（一年） : `rmb_bdirofi_y1`; 定期存款（两年） : `rmb_bdirofi_y2`; 定期存款（三年） : `rmb_bdirofi_y3`; 定期存款（五年） : `rmb_bdirofi_y5`; 贷款：六个月以内（含六个月） : `rmb_blrofi_wm6`; 贷款：一年以内（含一年） : `rmb_blrofi_wy1`; 贷款：六个月至一年（含一年） : `rmb_blrofi_m6ty1`; 贷款：一至三年（含三年） : `rmb_blrofi_y1ty3`; 贷款：三至五年（含五年） : `rmb_blrofi_y3ty5`; 贷款：一至五年（含五年） : `rmb_blrofi_y1ty5`; 贷款：五年以上 : `rmb_blrofi_mty5`; 一年期LRP : `lpr_y1`; 五年及以上LPR : `lpr_y5`; 三个月期MLF利率 : `mlf_m3_r`; 六个月期MLF利率 : `mlf_m6_r`; 一年期MLF利率 : `mlf_y1_r`; 1个周Shibor : `shibor_w1`; 2个周Shibor : `shibor_w2`; 1个月Shibor : `shibor_m1`; 3个月Shibor : `shibor_m3`; 6个月Shibor : `shibor_m6`; 9个月Shibor : `shibor_m9`; 1年Shibor : `shibor_y1`; 隔夜Shibor : `shibor_on`; 中债商业银行同业存单(AAA)隔夜收益率 : `cdnaaa_d1`; 中债商业银行同业存单(AAA)1周收益率 : `cdnaaa_w1`; 中债商业银行同业存单(AAA)1个月收益率 : `cdnaaa_m1`; 中债商业银行同业存单(AAA)6个月收益率 : `cdnaaa_m6`; 中债商业银行同业存单(AAA)1年收益率 : `cdnaaa_y1`; 隔夜回购定盘利率(FR001) : `fr_d1`; 七天回购定盘利率(FR007) : `fr_d7`; 十四天回购定盘利率(FR014) : `fr_d14`; 银银间隔夜回购定盘利率(FDR001) : `fdr_d1`; 银银间七天回购定盘利率(FDR007) : `fdr_d7`; 银银间十四天回购定盘利率(FDR014) : `fdr_d14` 美国支持: 联邦基金（有效） : `eff`; 金融商业票据：1个月 : `fcp_m1`; 金融商业票据：2个月 : `fcp_m2`; 金融商业票据：3个月 : `fcp_m3`; 非金融商业票据：1个月 : `nfcp_m1`; 非金融商业票据：2个月 : `nfcp_m2`; 非金融商业票据：3个月 : `nfcp_m3`; 银行优惠贷款 : `bpl`; 贴现窗主要信贷 : `dwpc`; 国库券（二级市场）：4周 : `smtb_w4`; 国库券（二级市场）：3个月 : `smtb_m3`; 国库券（二级市场）：6个月 : `smtb_m6`; 国库券（二级市场）：1年 : `smtb_y1`; 通货膨胀指数：5年 : `ii_y5`; 通货膨胀指数：7年 : `ii_y7`; 通货膨胀指数：10年 : `ii_y10`; 通货膨胀指数：20年 : `ii_y20`; 通货膨胀指数：30年 : `ii_y30`; 通货膨胀指数长期平均值 : `ltavg` 香港支持: 1周Hibor : `hibor_w1`; 2周Hibor : `hibor_w2`; 1个月Hibor : `hibor_m1`; 3个月Hibor : `hibor_m3`; 6个月Hibor : `hibor_m6`; 9个月Hibor : `hibor_m9`; 1年Hibor : `hibor_y1`; 隔夜Hibor : `hibor_on` |

### 示例

```json
{
    "areaCode": "cn",
    "startDate": "2016-03-20",
    "endDate": "2026-03-20",
    "metricsList": [
        "rmb_bdirofi_d"
    ],
    "token": "***********"
}
```

### 返回结果

```json
{
    "code": 1,
    "message": "success",
    "data": []
}
```
