{
  "_meta": {
    "module": "research",
    "role": "唯一入口，漏斗式调研",
    "version": "v5.3"
  },
  "_desc": "替代原独立路由。用户输入即为L1起点，逐层收窄。调研=路由，不存在单独的路由步骤。",
  "_output_format": {
    "structure": "[创作内容 + 平台 + 模型 + 尺寸 + 用途]",
    "example_image": "{type:image, content:橘猫东京街头, style:赛博朋克电影感, platform:mj, model:v6, size:16:9, use:壁纸}",
    "example_video": "{type:video, content:城市延时摄影, style:电影级叙事, platform:sora, model:Sora, size:1920x1080, use:社交媒体}",
    "_purpose": "五要素共同决定输出提示词的精确方向：platform→编译器语法，model→参数约束，size→宽高比/分辨率参数，use→风格倾向与质量词选择，content+type→模板与字段池"
  },
  "funnel_philosophy": "用户的第一次输入就是L1需求起点。调研不是猜测意图，而是帮用户从模糊到精确发现自己要什么。每层依赖上层结论，由大到小，循序渐进。类比图书馆：需求→分类架→出版社→版本号→具体那一本。模型存在偏差可能，只有逐层调研才能确认适用范围。",
  "skip_conditions": {
    "_note": "渐进式调研覆盖模型：5个维度，每步独立判断。不再使用二元(全有/全无)跳过逻辑。",
    "_ref": "core.global_skip_conditions",
    "_supplement": "research特有的补充规则：teach_mode跳过时输出版本号v5.3-teach，load:[core/core.md,builder/builder_templates.md,builder/builder_compiler.md]；tune_mode跳过时load:[core/core.md,builder/builder_templates.md,builder/builder_compiler.md,builder/builder_gates.md,output/output.md]",
    "progressive_coverage": {
      "_model": "5维调研渐进覆盖。每维命中=跳过该维的提问。未命中=必须问。覆盖度决定后续路径：",
      "dimensions": [
        {
          "id": "D1",
          "name": "创作内容",
          "weight": "required",
          "detect": "用户说了具体要画/拍什么（主体+内容描述），不是只说了一个大类关键词"
        },
        {
          "id": "D2",
          "name": "风格情绪",
          "weight": "required",
          "detect": "用户明确指定了风格/画风/感觉（写实/赛博朋克/二次元/电影感等），不是模糊的'好看''漂亮'"
        },
        {
          "id": "D3",
          "name": "平台与模型",
          "weight": "required_critical",
          "detect": "用户说出platform_map中的明确平台名(MJ/SD/豆包/通义等)。描述性词汇(电影感/高质量/AI生成)不视为平台"
        },
        {
          "id": "D4",
          "name": "尺寸比例",
          "weight": "required",
          "detect": "用户提到尺寸/比例/分辨率(16:9/竖版/4K/手机壁纸等)"
        },
        {
          "id": "D5",
          "name": "用途场景",
          "weight": "recommended",
          "detect": "用户说明用途(头像/海报/壁纸/商业/社交媒体)"
        }
      ],
      "coverage_matrix": {
        "5/5": {
          "action": "全部覆盖，直接进入聚焦+构建，无需任何提问",
          "example": "用豆包画一个赛博朋克风格的猫娘，16:9横屏做壁纸"
        },
        "4/5": {
          "action": "仅缺1个推荐维度(D5)，智能补全默认值后进入构建，不提问",
          "note": "D5用途可从size推断(16:9→壁纸/1:1→头像)，或留空"
        },
        "3/5": {
          "action": "缺2个维度，必须追问缺失项后才能构建",
          "_rule": "即使D1-D2已覆盖，D3(平台)是critical未覆盖就必须问",
          "example": "猫娘、百色、现代风格 → 缺D3平台+D4/D5 → 必须问平台和尺寸"
        },
        "2/5": {
          "action": "缺3个以上维度，走重度补全话术(script_subject_style或script_blank)",
          "note": "通常只有主体(D1)，需要大量智能默认值"
        },
        "≤1/5": {
          "action": "极度模糊，走script_blank引导式提问",
          "note": "用户可能不知道自己想要什么"
        }
      },
      "_anti_pattern": {
        "old_binary": "旧逻辑：三要素齐全就跳过 → 导致用户说了主体+风格但没说平台就直接输出了错误结果",
        "new_progressive": "新逻辑：数覆盖了几步 → 还差几步就问几步 → D3平台是硬门槛，没有就不能进builder"
      },
      "_execution": {
        "step1": "扫描用户输入，逐一对照5个维度的detect条件",
        "step2": "计算覆盖率 N/5",
        "step3": "查coverage_matrix决定下一步",
        "step4": "N≥4才允许跳过部分或全部调研",
        "step5": "N≤3时输出对应话术模板，等待用户回复后再进入builder"
      }
    }
  },
  "funnel_L1_need": {
    "label": "需求识别 — 用户想要什么？",
    "desc": "用户的第一次输入即为原始素材。判断本次交互属于哪个大类，这是漏斗最顶层，口子最大。",
    "_note": "这一层不做安全检查、不做平台推断、不做细节采集。只回答一个问题：用户要什么类型的内容？",
    "branches": {
      "image_gen": {
        "label": "图片生成",
        "keys": [
          "画",
          "图片",
          "生图",
          "立绘",
          "摄影",
          "壁纸",
          "照片",
          "海报",
          "生成",
          "创建",
          "制作",
          "给图",
          "做一张",
          "帮我画",
          "image",
          "draw",
          "generate",
          "设计"
        ],
        "content_type": "image",
        "next": "L2"
      },
      "video_gen": {
        "label": "视频生成",
        "keys": [
          "视频",
          "动态",
          "镜头",
          "分镜",
          "运动",
          "慢动作",
          "动画",
          "动起来",
          "运镜",
          "帧",
          "秒",
          "duration",
          "video",
          "可灵",
          "keling",
          "sora",
          "runway"
        ],
        "content_type": "video",
        "next": "L2"
      },
      "multimodal_input": {
        "label": "多模态输入(有文件)",
        "condition": "用户上传了文件",
        "sub_route": "图片文件走image流程 / 视频文件走video流程 / 需确认用途(图生图/图生视频/反编译)",
        "next": "L2或decompile"
      },
      "teach_request": {
        "label": "教学模式",
        "keys": [
          "教我",
          "怎么写",
          "写作方法",
          "提示词技巧",
          "教学",
          "教程"
        ],
        "content_type": "teach",
        "next": "终止漏斗，直出type=teach"
      },
      "chat_fallback": {
        "label": "未识别/闲聊",
        "action": "输出welcome语后终止，load:[]",
        "_note": "L1全部不命中才到这里。不是路由兜底，而是漏斗第一层就筛掉了"
      }
    },
    "_output_L1": "content_type初步确定(image/video/teach/chat/decompile)"
  },
  "funnel_L2_content_detail": {
    "label": "创作内容细化 — 具体做什么？",
    "desc": "基于L1确定的类型，收窄到具体的创作内容方向。这一层决定后续使用哪套字段池和风格模板。",
    "_note": "这里不问平台、不问模型，只聚焦于'创作内容本身是什么'",
    "for_image_content": {
      "style_class_A": {
        "label": "写实摄影方向",
        "keys": [
          "写实",
          "摄影",
          "照片",
          "真实感",
          "photorealistic",
          "8k"
        ],
        "template_ref": "A类写实摄影模板"
      },
      "style_class_B": {
        "label": "二次元插画方向",
        "keys": [
          "二次元",
          "动漫",
          "anime",
          "赛璐璐",
          "立绘",
          "手游风"
        ],
        "template_ref": "B类二次元模板"
      },
      "style_class_C": {
        "label": "创意/混合方向",
        "keys": [
          "混合",
          "创意",
          "拼贴",
          "mixed media",
          "collage"
        ],
        "template_ref": "C类聚焦特写模板"
      },
      "style_class_D": {
        "label": "信息图表方向",
        "keys": [
          "信息图",
          "图表",
          "流程图",
          "infographic",
          "科学",
          "示意图"
        ],
        "template_ref": "D类信息图模板"
      },
      "style_unknown": {
        "label": "无法归类",
        "action": "E类归纳流程 → 识别风格锚点 → 拆解光影公式 → 提取色彩编码 → 归纳构图范式 → 提炼质感清单 → 输出5个视觉基因"
      }
    },
    "for_video_content": {
      "narrative_cinema": {
        "label": "电影级叙事",
        "keys": [
          "电影",
          "电影感",
          "cinematic",
          "叙事"
        ]
      },
      "fast_commercial": {
        "label": "快节奏商业",
        "keys": [
          "广告",
          "商业",
          "快剪",
          "节奏",
          "commercial"
        ]
      },
      "nature_docu": {
        "label": "自然纪录片",
        "keys": [
          "纪录片",
          "自然",
          "documentary"
        ]
      },
      "art_experiment": {
        "label": "艺术实验",
        "keys": [
          "艺术",
          "实验",
          "抽象",
          "experimental",
          "abstract"
        ]
      }
    },
    "_output_L2": "创作内容方向(style_direction) + 主体描述初步(subject_draft)"
  }
}