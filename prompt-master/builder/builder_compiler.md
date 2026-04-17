{
  "_meta": {
    "module": "builder-compiler",
    "role": "compiler+presets",
    "version": "v5.3"
  },
  "compiler": {
    "midjourney": {
      "template": "{desc}, {tags} {params}",
      "params": {
        "ar": "--ar {w}:{h}",
        "s": "--s {0-1000}",
        "niji": "--niji 5"
      },
      "example": "a fluffy tabby cat on a tokyo street at night, neon reflections on wet pavement, 35mm f/1.8 bokeh, photorealistic 8k --ar 16:9 --s 250"
    },
    "stable_diffusion": {
      "template_pos": "({subj}:1.4), ({comp}:1.2), ({light}:1.1), [{style_tags}]",
      "template_neg": "[{common_negatives}, {style_negatives}]",
      "example_pos": "(a fluffy tabby cat:1.4), (tokyo street at night:1.2), (neon reflections:1.2), (bokeh:1.1), (photorealistic:1.1)",
      "example_neg": "[cartoon:0.8], [anime:0.8], [blurry:0.8], [low quality:0.9]"
    },
    "flux": {
      "template": "{full_natural_paragraph_under_300_words}",
      "example": "A fluffy tabby cat sitting on a Tokyo street at night, neon sign reflections shimmering across the wet pavement below. Shot on a 35mm lens at f/1.8 with beautiful bokeh. Photorealistic and cinematic in 8K quality."
    },
    "dall_e": {
      "template": "{complete_narrative_no_params_no_symbols}",
      "example": "A photorealistic image of a fluffy orange tabby cat perched on a bench edge on a quiet Tokyo street at night. Rain has just passed, leaving the pavement wet and reflective. Neon signs cast pink and cyan glows across the scene. Shot from eye level with shallow depth of field blurring background into soft bokeh circles. Cinematic and atmospheric."
    },
    "video_universal": {
      "template": "{subject_desc}. The {cam_move} captures it as {motion_desc}. {env_light}. Duration: {dur}s.",
      "example": "A lone figure walks steadily down a rain-soaked Tokyo street at night, holding an umbrella that sways gently. A low-angle tracking shot follows from behind as neon pink and cyan light reflects off the wet pavement. Duration: 10 seconds.",
      "_note": "适用于Sora/Runway/Pika等国际视频平台，英文自然叙事句"
    },
    "video_cn_domestic": {
      "template": "{中文场景描述}。镜头采用{运镜方式}，展现{运动描述}。环境与光影：{环境光影描述}。时长约{duration}秒。",
      "example": "一位孤独的行人走在雨夜的东京街头，手持一把微微摇晃的雨伞。低角度跟拍镜头从身后跟随，霓虹粉色和蓝色的光反射在湿漉漉的路面上。时长约10秒。",
      "_note": "适用于可灵(Kling)/即梦等国内视频平台，全中文自然描述，无英文关键词，无特殊符号",
      "rules": [
        "全中文输出，不堆砌英文标签",
        "不用括号权重和数值参数",
        "用逗号分隔元素，句号表示逻辑分段"
      ]
    },
    "domestic_cn_image": {
      "_note": "国内图片平台通用默认编译器，各子平台有独立覆盖规则",
      "template": "{完整中文叙事段落，自然语言描述}",
      "example": "一只毛茸茸的橘猫坐在东京夜晚的街头上，霓虹灯的倒影映在潮湿的地面上。35mm镜头拍摄，光圈f/1.8产生柔和虚化效果，照片级真实感，电影氛围。",
      "rules": [
        "全部使用中文自然语言",
        "不使用任何括号、权重符号、参数标记",
        "形容词用中文修饰词表达(比较/非常/极其)代替数值权重",
        "保持流畅的句子结构，类似写一段画面描述文"
      ],
      "sub_platforms": {
        "_ref": "各子平台的max_length以 builder/builder_gates.G4_length.standards 为权威标准。此处仅做编译时参考。",
        "doubao": {
          "name": "豆包",
          "max_length": 80,
          "max_length_unit": "字",
          "style_guide": "豆包对短句+画面感强的描述效果最佳。避免过长从句，每句话控制在15字以内。重点突出主体和核心氛围，辅助元素不超过2个。偏好具体名词(如'橘猫''霓虹招牌')而非抽象形容(如'梦幻般的美感')。英文单词会导致效果下降，必须纯中文。",
          "anti_patterns": [
            "超过100字的长段落",
            "堆砌3个以上光影形容词",
            "包含英文关键词",
            "用'非常/极其/特别'连续修饰",
            "一句话里超过3个逗号"
          ],
          "good_example": "橘猫坐在雨后的东京街头，霓虹灯光倒映在积水里，毛茸茸的身体微微发抖。电影质感，暖色调。",
          "bad_example": "一只非常可爱的毛茸茸的橘猫坐在一个充满赛博朋克风格的雨后东京街道上，周围有各种颜色的neon sign灯光反射在wet pavement上，营造出一种极其梦幻而又带有电影cinematic感觉的氛围，光线是warm tone的，细节非常丰富..."
        },
        "qwen": {
          "name": "千问",
          "max_length": 150,
          "max_length_unit": "字",
          "style_guide": "千问能处理中等长度描述，支持一定的细节层次。可以分2-3个句子，第一句定主体，第二句补环境，第三句给风格。允许少量常用英文专有名词(Midjourney风格等)但不推荐。"
        },
        "wenxin": {
          "name": "文心一言",
          "max_length": 120,
          "max_length_unit": "字",
          "style_guide": "文心偏写实风格表现好，对构图词敏感。强调空间关系和主体位置。避免过度艺术化的抽象描述。"
        },
        "hunyuan": {
          "name": "混元",
          "max_length": 120,
          "max_length_unit": "字",
          "style_guide": "混元对人像和场景还原能力强，适合带人物情感描述的提示词。"
        }
      }
    }
  },
  "presets": {
    "image": [
      {
        "name": "赛博朋克",
        "keywords": [
          "cyberpunk",
          "neon-lit",
          "futuristic city",
          "rainy streets",
          "holographic"
        ]
      },
      {
        "name": "吉卜力/动漫",
        "keywords": [
          "studio ghibli",
          "hand drawn animation",
          "soft pastel colors",
          "whimsical",
          "peaceful scenery"
        ]
      },
      {
        "name": "水彩风",
        "keywords": [
          "watercolor painting",
          "soft washes",
          "wet-on-wet",
          "pigment blooms",
          "paper texture"
        ]
      },
      {
        "name": "电影感",
        "keywords": [
          "cinematic shot",
          "film still",
          "anamorphic lens",
          "color graded",
          "moody lighting"
        ]
      },
      {
        "name": "极简主义",
        "keywords": [
          "minimalist",
          "clean composition",
          "negative space",
          "muted palette",
          "simple elegant"
        ]
      }
    ],
    "video": [
      {
        "name": "电影级叙事",
        "keywords": [
          "cinematic storytelling",
          "slow reveal",
          "emotional pacing",
          "narrative driven",
          "character focus"
        ],
        "motion_tags": [
          "slow push in",
          "gentle pan",
          "dolly tracking",
          "static contemplative"
        ],
        "platform_hint": "Sora/Runway最佳"
      },
      {
        "name": "快节奏商业",
        "keywords": [
          "high energy commercial",
          "dynamic cuts",
          "product showcase",
          "vibrant motion",
          "beat-synced"
        ],
        "motion_tags": [
          "fast zoom",
          "quick whip pan",
          "snap cuts",
          "rhythm matching"
        ],
        "platform_hint": "Pika/即梦适合"
      },
      {
        "name": "自然纪录片",
        "keywords": [
          "documentary style",
          "observational",
          "natural ambient",
          "authentic moment",
          "candid footage"
        ],
        "motion_tags": [
          "handheld subtle",
          "follow shot slow",
          "environmental pan",
          "static wide establishing"
        ],
        "platform_hint": "可灵/Sora"
      },
      {
        "name": "艺术实验",
        "keywords": [
          "avant-garde visual",
          "surreal transition",
          "abstract morphing",
          "symbolic imagery",
          "dreamlike flow"
        ],
        "motion_tags": [
          "morph dissolve",
          "particle swarm",
          "time-lapse blend",
          "non-linear edit"
        ],
        "platform_hint": "Runway/Pika"
      }
    ]
  },
  "teach_mode": {
    "template": "|\n  提示词结构: [主体] [风格] [构图/运动] [光影] [质量]\n\n  正向: {positive_prompt}\n\n  反向: {negative_prompt}\n\n  参数建议: {params}\n|",
    "feedback": "对结果不满意？告诉我想调整哪个部分，我帮你微调。"
  }
}