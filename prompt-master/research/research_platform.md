{
  "_meta": {
    "module": "research-platform",
    "role": "L3平台确认+L4模型版本",
    "version": "v5.3"
  },
  "funnel_L3_platform": {
    "label": "平台确认 — 在哪里生成？",
    "desc": "平台决定编译器语法规则和参数体系。这是关键分叉点——不同平台输出格式完全不同。同一内容在不同平台的写法完全不一样。",
    "_note": "平台信息直接影响后续加载范围——确定MJ就只读MJ编译器段，确定SD就只读SD编译器段",
    "platform_map": {
      "mj": {
        "name": "Midjourney",
        "keys": [
          "mj",
          "midjourney",
          "MJ"
        ],
        "syntax": "自然语言+参数后缀，不用括号权重",
        "compiler_section": "compiler.mj"
      },
      "sd": {
        "name": "Stable Diffusion",
        "keys": [
          "sd",
          "stable diffusion",
          "SD"
        ],
        "syntax": "括号权重+标记加权",
        "compiler_section": "compiler.sd"
      },
      "flux": {
        "name": "Flux",
        "keys": [
          "flux",
          "Flux"
        ],
        "syntax": "自然长句，有限括号权重",
        "compiler_section": "compiler.flux"
      },
      "dalle": {
        "name": "DALL-E",
        "keys": [
          "dalle",
          "DALL-E",
          "dall-e"
        ],
        "syntax": "纯自然语言，无特殊语法",
        "compiler_section": "compiler.dalle"
      },
      "sora": {
        "name": "Sora",
        "keys": [
          "sora",
          "Sora"
        ],
        "syntax": "自然叙事句",
        "compiler_section": "compiler.video"
      },
      "runway": {
        "name": "Runway",
        "keys": [
          "runway",
          "Runway"
        ],
        "syntax": "自然叙事句",
        "compiler_section": "compiler.video"
      },
      "keling": {
        "name": "可灵/Kling",
        "keys": [
          "可灵",
          "keling",
          "Kling"
        ],
        "syntax": "中文自然描述",
        "compiler_section": "compiler.video_cn"
      },
      "jimeng": {
        "name": "即梦",
        "keys": [
          "即梦",
          "jimeng"
        ],
        "syntax": "中文自然描述",
        "compiler_section": "compiler.domestic_cn"
      },
      "pika": {
        "name": "Pika",
        "keys": [
          "pika",
          "Pika"
        ],
        "syntax": "自然叙事句",
        "compiler_section": "compiler.video"
      },
      "domestic_img": {
        "name": "国内图片平台(千问/豆包/文心/混元)",
        "keys": [
          "千问",
          "豆包",
          "文心",
          "混元",
          "通义"
        ],
        "syntax": "全中文，权重转修饰词",
        "compiler_section": "compiler.domestic_cn"
      }
    },
    "auto_recommend": {
      "when": "用户未指定任何平台",
      "logic": [
        "写实/摄影方向→推荐Midjourney",
        "二次元/动漫方向→推荐SD或MJ-niji",
        "视频电影感→推荐Sora",
        "视频快节奏→推荐Runway",
        "视频中文语境→推荐可灵/即梦",
        "不确定/通用→根据L2创作内容方向匹配默认平台"
      ],
      "_rule": "推荐不超过3个选项，需用户确认后才锁定平台"
    },
    "_output_L3": "platform(精确平台标识) + syntax_rule(对应语法规则引用) + compiler_section(builder内精确段落名)"
  },
  "funnel_L4_model": {
    "label": "模型版本 — 用哪个模型？",
    "desc": "同一平台下可能有多个模型版本，模型影响效果上限和参数约束。确定模型后可以精确定位builder内的参数配置。",
    "_note": "模型是最精确的分叉点。确定了model=SDXL vs SD1.5，后续的参数约束、质量预期、防膨胀策略都不同",
    "models_by_platform": {
      "mj": [
        "v6",
        "v6.1",
        "niji6",
        "niji5"
      ],
      "sd": [
        "SDXL",
        "SD1.5",
        "Turbo",
        "Lightning"
      ],
      "flux": [
        "Flux.1-dev",
        "Flux.1-schnell"
      ],
      "dalle": [
        "DALL-E 3",
        "DALL-E 2"
      ],
      "sora": [
        "Sora"
      ],
      "runway": [
        "Gen-3",
        "Gen-2"
      ],
      "keling": [
        "可灵1.5",
        "可灵1.0"
      ],
      "jimeng": [
        "即梦2.1"
      ],
      "domestic": [
        "默认模型"
      ]
    },
    "unknown_handling": "用户未指定具体版本时，使用该平台当前主力模型的默认配置。内部构建时按对应模型约束处理，输出时不强行标注模型名除非用户明确要求。",
    "_output_L4": "model(具体版本字符串 或 null表示用默认) + param_constraints(参数约束引用)"
  }
}