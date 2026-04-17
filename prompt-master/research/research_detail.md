{
  "_meta": {
    "module": "research-detail",
    "role": "L5细节采集+话术+评分+自检",
    "version": "v5.3"
  },
  "funnel_L5_final_detail": {
    "label": "最终细节 — 画面里到底有什么？",
    "desc": "漏斗最窄层。基于L1-L4锁定的精确范围（知道类型、知道内容方向、知道平台、知道模型），只在这个框架内精准填充细节。不再发散，不再换方向。",
    "collection_framework": {
      "dim_what": {
        "weight": 25,
        "label": "核心内容",
        "capture": "画什么/拍什么的核心视觉元素",
        "questions": [
          "主体是什么？（人物/动物/物体/场景）",
          "主体的关键特征？（颜色/形状/姿态/表情）",
          "必须出现的元素？"
        ]
      },
      "dim_feel": {
        "weight": 20,
        "label": "风格与情绪",
        "capture": "整体感觉/氛围/情绪基调",
        "questions": [
          "想要的具体风格/画风？",
          "情绪氛围？（温暖/冷峻/梦幻/紧张/宁静...）",
          "有参考作品或艺术家吗？"
        ]
      },
      "dim_where": {
        "weight": 15,
        "label": "场景与环境",
        "capture": "在哪里发生/背景环境",
        "questions": [
          "场景/地点？",
          "时间？（白天/夜晚/黄昏/黎明）",
          "天气/环境条件？"
        ]
      },
      "dim_platform": {
        "weight": 15,
        "label": "平台与模型（必问！）",
        "capture": "在哪个平台生成，用什么模型。此维度未确认前禁止进入builder",
        "questions": [
          "用什么平台生成？（MJ/SD/Flux/DALL-E/豆包/可灵/Sora/不确定我推荐）",
          "有偏好的模型版本吗？（不知道就用默认）"
        ],
        "_critical": true
      },
      "dim_size_usage": {
        "weight": 15,
        "label": "尺寸与用途",
        "capture": "输出尺寸比例和最终使用场景",
        "questions": [
          "需要什么比例？（横屏16:9 / 竖屏9:16 / 方形1:1 / 其他）",
          "用途？（社交分享/壁纸/商业物料/头像/打印/其他）"
        ],
        "_note": "尺寸决定--ar参数，用途影响风格倾向和质量词选择"
      },
      "dim_extra": {
        "weight": 10,
        "label": "特殊约束",
        "capture": "额外偏好与禁忌",
        "questions": [
          "一定要避免的元素？",
          "特殊文字/水印/标志要求？",
          "其他补充？"
        ]
      }
    },
    "input_level_map": {
      "level_1": {
        "threshold": "<=10字",
        "strategy": "重度补全，P0字段+大量智能默认值"
      },
      "level_2": {
        "threshold": "11-30字",
        "strategy": "适度补全，P0+部分P1字段"
      },
      "level_3": {
        "threshold": "31-80字",
        "strategy": "精准拆解，P0+P1+部分P2字段"
      },
      "level_4": {
        "threshold": ">80字",
        "strategy": "完整拆解+防膨胀裁剪，全字段激活"
      }
    },
    "_output_L5": "detail_json(完整字段数据)，准备传入builder构建"
  },
  "scripts_one_pass": {
    "script_blank": {
      "when": "输入极短(<=10字)且无明显有效信息",
      "text": "我先确认几个关键点，一次回答就好不用每条都答:\n\n1. 你想画/做什么?(核心主体)\n2. 想要什么感觉或风格?\n3. 用什么平台?(MJ/SD/Flux/DALL-E/豆包/可灵/Sora...不确定我推荐)\n4. 要什么比例?(横屏/竖屏/方形/无所谓)"
    },
    "script_subject_only": {
      "when": "只有主体缺其他",
      "text": "收到!主体是{subject}。再补三个:\n1. 想要什么风格?(写实/插画/电影感/动漫...)\n2. 用什么平台生成?不知道我推荐\n3. 用途和尺寸有要求吗?"
    },
    "script_subject_style": {
      "when": "有主体和风格缺平台",
      "text": "明白了!{subject} + {style}风格。还需要:\n1. 用什么平台?(MJ/SD/Flux/DALL-E/豆包/可灵/不确定帮我选)\n2. 尺寸比例有要求吗?"
    },
    "script_most_complete": {
      "when": "平台已确认，创作内容和风格齐全，只缺尺寸/用途",
      "text": "信息够了!开始构建。默认用{platform}标准参数，想到要调整的随时说。\n💡 如果你还想要其他平台的版本，告诉我，我可以同时输出多个平台的提示词"
    },
    "script_platform_unsure": {
      "when": "表达了意图但不清楚平台选择",
      "text": "平台推荐:\n追求美感->Midjourney | 追求可控->Stable Diffusion\n追求简洁->Flux/DALL-E | 国内->豆包/千问 | 视频->Sora(电影) 可灵(中文)\n你倾向哪种?"
    },
    "script_with_reference": {
      "when": "用户上传了参考图/视频",
      "text": "参考图收到!确认下:\n1. 哪部分想保留?(构图/色彩/氛围?)\n2. 主体要换吗?还是保持原样微调?\n3. 目标平台?(必须指定一个或让我推荐)"
    },
    "_termination_rule": "一轮对话一次输出。用户回复后立即结束调研阶段进入builder。不循环追问。"
  },
  "scoring": {
    "pass_threshold": 60,
    "high_threshold": 75,
    "medium_threshold": 45,
    "decision_matrix": {
      ">=75": "高置信度，直接进入builder",
      "45-74": "中置信度，builder自检升级严格度",
      "<45": "低置信度，⚠警告标记贯穿后续全程，安全检查加严",
      "user_declined": "极低置信度阻断级，建议用户提供更多信息后再继续"
    }
  },
  "post_research_selfcheck": {
    "purpose": "模拟脑内渲染，基于已确定的平台+模型提前发现偏差",
    "bias_library": {
      "mj_common": [
        "过度堆砌标签(应用自然语言)",
        "忽略--ar/--q等参数",
        "混入SD式括号权重"
      ],
      "sd_common": [
        "写成自然段落(应拆为标签)",
        "忘记negative prompt",
        "权重值不合理(>1.5或<0.7)"
      ],
      "flux_common": [
        "文字乱码风险",
        "复杂场景丢元素",
        "长文本精度下降"
      ],
      "dalle_common": [
        "加入非自然语言符号",
        "超字符限制",
        "过度字面理解"
      ],
      "domestic_common": [
        "英文关键词过多",
        "保留括号权重符号"
      ],
      "video_common": [
        "缺少运动描述",
        "运镜术语不准确",
        "时长超出平台限制"
      ]
    }
  }
}