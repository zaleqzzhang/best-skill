{
  "_meta": {
    "module": "platform_signals",
    "role": "平台模型信号层：通过结构化标记激活各平台RAG/注意力机制，加速响应+降低token消耗",
    "version": "v5.3",
    "_when_to_load": "research/ 确认L3平台后，builder/compiler编译前加载本文件。与compiler并列执行。"
  },
  "_philosophy": "每个国内大模型的训练语料、tokenizer、attention模式不同。同样的中文描述在不同平台上产生的效果差异巨大。本文件不是替换compiler，而是在编译器输出的基础上，追加一层'平台原生适配'——让输出看起来像这个平台的原生用户写出来的，而不是翻译过来的。",
  "signals": {
    "doubao": {
      "_platform": "豆包(字节跳动)",
      "_model_trait": "偏好短句排比、前置主体、强画面感动词。训练数据含大量抖音/头条风格的短内容。tokenizer对中文分粒度细，长句容易语义漂移。",
      "rag_triggers": {
        "_note": "这些关键词会触发豆包内置知识库的相关语料召回，利用而非对抗",
        "trigger_words": [
          "Midjourney风格提示词",
          "Stable Diffusion正向提示词",
          "AI绘画提示词模板",
          "电影感画面描述"
        ],
        "_usage": "在输出中自然嵌入上述词汇，引导RAG拉取对应高质量语料作为隐式参考"
      },
      "attention_hooks": {
        "_note": "让模型的注意力优先落在这些位置",
        "primary_anchor": "[主体] 必须放在句首或第一分句的核心位置，豆包模型对首部token赋予更高attention权重",
        "visual_verb": "每句话必须有1个强视觉动词（坐/站/走/飞/流淌/倒映），避免纯形容词堆砌",
        "color_number_rule": "颜色不超过2种，数字不超过1组，过多属性分散attention"
      },
      "output_format": {
        "_ref": "max_length以 builder/builder_gates.G4_length.standards 为权威。此处仅做信号层格式参考。",
        "structure": "{主语} {动作/状态}，{环境}。{氛围}。",
        "example_good": "橘猫蹲在窗台上，尾巴垂下来。雨后的街道亮着霓虹灯。冷色调电影感。",
        "example_bad": "一只毛茸茸可爱的橙色斑纹猫咪正优雅地坐在被雨水打湿的东京都市街道旁的木质窗台边缘上，它的目光凝视着远方，背景是充满赛博朋克风格的霓虹灯光和反射在地面上水洼中的绚丽色彩，整体呈现出一种孤独而又神秘的氛围感，仿佛来自未来的科幻电影场景一般令人着迷",
        "max_length": 80,
        "sentence_count": "3-5句，每句≤15字",
        "forbidden": [
          "英文单词超过2个",
          "括号嵌套",
          "连续3个以上形容词",
          "超过15字的长句",
          "抽象名词连续出现(氛围/意境/感觉/情绪)"
        ]
      },
      "token_optimization": {
        "_strategy": "豆包对重复/冗余敏感，精简即加速",
        "remove_patterns": [
          "的之乎者也等虚词",
          "非常/极其/特别等程度副词重叠",
          "类似...那样的比喻句"
        ]
      }
    },
    "tongyi": {
      "_platform": "通义千问(阿里)",
      "_model_trait": "偏技术文档风格，对结构化标记(分号/编号)响应好。训练数据含大量电商商品描述，对产品感/材质感的描述能力强。",
      "rag_triggers": {
        "trigger_words": [
          "AI绘画提示词",
          "图像生成prompt",
          "视觉设计描述"
        ],
        "_usage": "通义内置电商图片语料丰富， trigger后可召回商品摄影级描述范式"
      },
      "attention_hooks": {
        "primary_anchor": "[主体+材质] 通义对物质性描述attention高，强调纹理/质感/材料",
        "semantic_grouping": "用分号;分隔同类别元素(颜色;光影;构图)，通义tokenizer对分号有特殊segmentation处理",
        "quantity_precision": "数字和量词要精确(一束光/三道阴影)，模糊数量降低置信度"
      },
      "output_format": {
        "structure": "{主体}(材质/质感);{动作};{环境};{光影};{风格}",
        "example_good": "橘猫(绒毛发质);蹲姿;雨后木窗台;霓虹侧光;赛博朋克冷调",
        "example_bad": "一只很可爱的橘猫坐在窗台上看着外面的街道，有很多霓虹灯，感觉很有电影的那种感觉",
        "max_length": 100,
        "sentence_count": "分号分隔4-6段",
        "forbidden": [
          "纯自然段落无标点分隔",
          "感叹号多于1个",
          "口语化表达(挺好看的/感觉不错)"
        ]
      },
      "token_optimization": {
        "_strategy": "利用分号结构化减少连接词token消耗",
        "remove_patterns": [
          "因为...所以...",
          "不仅...而且...",
          "以及/同时/此外等连接词"
        ]
      }
    },
    "wenxin": {
      "_platform": "文心一言(百度)",
      "_model_trait": "偏新闻/叙事文风，对完整句子结构要求高。训练数据含大量百科和新闻文本，对事实性描述稳定但对创意性描述偏保守。",
      "rag_triggers": {
        "trigger_words": [
          "画面描述",
          "场景描写",
          "影视镜头语言"
        ],
        "_usage": "文心内置影视/文学语料，可召回专业镜头术语"
      },
      "attention_hooks": {
        "primary_anchor": "[时间+地点] 文心对时空锚定attention高，先交代何时何地再展开画面",
        "narrative_chain": "按时间顺序展开(远→近→特写)，文心的叙事attention是序列式的",
        "emotion_label": "情绪词放在句末作总结，不插在中间打断视觉流"
      },
      "output_format": {
        "structure": "{时间}，{地点}。{远景}。{中景}。{近景/特写}。{整体氛围}。",
        "example_good": "雨夜，东京街头。远处霓虹闪烁。街面上积水映着光。一只橘猫蹲在窗边。清冷的都市气息。",
        "example_bad": "赛博朋克风格的橘猫在东京街头雨夜中的霓虹灯下显得非常有电影感，光线很好看",
        "max_length": 120,
        "sentence_count": "5-7句，按景别递进",
        "forbidden": [
          "缺少时空交代直接描述主体",
          "倒装句",
          "过长修饰语插入主谓之间"
        ]
      },
      "token_optimization": {
        "_strategy": "景别递进结构天然去重，避免反复描述同一元素",
        "remove_patterns": [
          "同一元素在不同距离重复出现(除非有意为之)",
          "回指代词(它/这/那)过多"
        ]
      }
    },
    "hunyuan": {
      "_platform": "混元(腾讯)",
      "_model_trait": "偏社交/对话风格，对人物表情和情感互动描述强。训练数据含微信生态内容，对人像/社交场景理解深。",
      "rag_triggers": {
        "trigger_words": [
          "人像摄影提示词",
          "角色设定描述",
          "表情动作描写"
        ],
        "_usage": "混元内置人像/社交语料丰富，人像类prompt效果显著优于风景"
      },
      "attention_hooks": {
        "primary_anchor": "[表情/神态] 混元对面部特征attention极高，有人物时必写表情",
        "interaction_signal": "描述人物与环境/他人的互动关系(看向/倚靠/伸手)，静态摆拍效果差",
        "social_context": "暗示观看者视角(镜头前/画面外/迎面走来)，增加代入感"
      },
      "output_format": {
        "structure": "{人物}(表情+神态){姿态}{与环境的关系}{环境}{观者视角暗示}",
        "example_good": "女孩(微微侧头浅笑)靠在栏杆上，风吹起发梢。身后城市灯火渐暗。她似乎在看向镜头外的某处。",
        "example_bad": "一个漂亮的女孩站在阳台上，背景是城市夜景",
        "max_length": 110,
        "sentence_count": "4-6句",
        "forbidden": [
          "人物无表情描述",
          "纯静态摆拍无动态感",
          "缺少观者视角"
        ]
      },
      "token_optimization": {
        "_strategy": "聚焦人物+互动，环境一笔带过",
        "remove_patterns": [
          "大段环境描写(非人物主体时除外)",
          "与情感无关的技术参数"
        ]
      }
    },
    "moonshot": {
      "_platform": "月之暗面/Kimi",
      "_model_trait": "长context窗口优势极大(200K+)，对复杂指令和多层嵌套理解好。适合精细描述但容易过度生成。",
      "rag_triggers": {
        "trigger_words": [
          "详细画面描述",
          "多模态提示词",
          "长文本图像生成"
        ],
        "_usage": "Kimi的长context特性使其能容纳更多参考语料"
      },
      "attention_hooks": {
        "primary_anchor": "[层次嵌套] Kimi对括号/嵌套结构的解析能力最强，可以用(主(次(细节)))结构",
        "detail_tolerance": "Kimi能处理比其他平台多30-50%的信息密度，不必过度裁剪",
        "chain_of_thought": "可以在描述中嵌入因果逻辑(因为A所以B)，Kimi能保持长程依赖不被截断"
      },
      "output_format": {
        "structure": "{核心场景}(其中{细节层1}(内含{微观细节}))。{因果关系延伸}。{可选技术备注}。",
        "example_good": "雨夜东京街头(积水如镜(倒映着粉色与青色的霓虹光带))。橘猫蹲在窗沿上(胡须微颤)。因为刚下过雨，空气中有湿润的金属气味。--ar 16:9 --style raw",
        "example_bad": "猫在街上，有霓虹灯，下雨了",
        "max_length": 150,
        "sentence_count": "3-5句(允许句内有嵌套)",
        "forbidden": [
          "过度简化导致浪费长context优势",
          "单句信息密度过低"
        ]
      },
      "token_optimization": {
        "_strategy": "Kimi不怕长，怕的是信息密度低。与其缩短不如提升有效信息占比",
        "remove_patterns": [
          "空泛填充词(美丽的/好看的/不错的)",
          "重复表达同一意思的不同说法"
        ]
      }
    }
  },
  "_cross_platform_rules": {
    "_note": "适用于所有国内平台的通用信号规则",
    "chinese_native": {
      "rule": "国内平台全部使用简体中文输出，英文仅限专有名词(MJ/SD/Flux等品牌名和不可替代的技术术语)",
      "exception_list": [
        "Midjourney",
        "Stable Diffusion",
        "DALL-E",
        "Sora",
        "Runway",
        "Flux",
        "Pika",
        "Kling",
        "niji",
        "SDXL",
        "Gen-3",
        "bokeh",
        "cinematic"
      ]
    },
    "signal_markers": {
      "_note": "可选：在输出前后添加轻量标记以强化平台对内容类型的识别",
      "image_start": "可选添加: [🖼️ 图像提示词]",
      "video_start": "可选添加: [🎬 视频提示词]",
      "_warning": "标记不应计入长度限制，且不是所有平台都需要。豆包建议不加(干扰简洁性)；Kimi建议加上(帮助长context定位)"
    },
    "anti_pattern_library": {
      "_note": "所有国内平台共用的反模式，任何平台都不应该出现",
      "patterns": [
        {
          "pattern": "英文段落>20个单词",
          "reason": "国产模型英文能力普遍弱于中文，长英文导致语义退化",
          "fix": "翻译为中文或保留<5个关键英文术语"
        },
        {
          "pattern": "括号嵌套>=3层",
          "reason": "除Kimi外多数平台tokenizer对深层嵌套解析不稳定",
          "fix": "展平为一维列表或降到2层以内"
        },
        {
          "pattern": "连续>=5个逗号分隔的无结构列表",
          "reason": "失去层次感，模型attention均匀散开无法聚焦",
          "fix": "分组或用分号/换行重构"
        },
        {
          "pattern": "纯形容词堆砌(无动词/名词)",
          "reason": "缺乏视觉锚点，模型无法构建具体画面",
          "fix": "强制每个形容词绑定一个具体名词"
        }
      ]
    }
  },
  "_integration_point": {
    "where": "builder/compiler 编译器原始输出后、G4门控前插入",
    "flow_step": "compiler原始输出 → platform_signals适配(根据L3确定的平台加载对应signals) → G4长度检查(使用该平台专属标准) → G5质量优化 → 最终输出",
    "_fallback": "如果目标平台不在signals定义中，使用domestic_cn_image默认规则，输出警告日志但不阻断"
  }
}