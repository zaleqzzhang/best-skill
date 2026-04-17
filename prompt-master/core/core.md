{
  "_meta": {
    "name": "prompt-master",
    "version": "v5.3",
    "arch": "funnel-driven",
    "_note": "唯一规则字典。research/ 和 builder/ 下各文件通过_ref引用本文件。本文件不参与流程决策，只存储规则数据。"
  },
  "safety": {
    "BLOCK": [
      "血腥暴力",
      "政治敏感",
      "色情露骨",
      "儿童不当内容",
      "真人照片",
      "名人面容",
      "肖像权"
    ],
    "REFUSE": [
      "暴力",
      "色情",
      "政治敏感",
      "违法内容"
    ],
    "ADJUST": [
      "品牌标志→通用描述",
      "版权角色→同类替代"
    ],
    "PHYSICS_WARN": "物理不可能的描述 → 提示可能无法准确生成，不阻断",
    "_execution_point": "research/ 漏斗L3平台确认之后、进入builder/之前执行。由research/输出结果触发调用。",
    "_ref_by": [
      "builder/builder_gates.G3_safety",
      "research/research_base._rule_refs.safety"
    ]
  },
  "welcome_text": {
    "_note": "用户指定的完整欢迎语（含token警告/教学模式入口/新手指南入口/workbuddy推广）。首次对话或消息数量为零时输出一次。",
    "text": "你好呀！我是提示词创作专家。\n我可以帮你：\n  • 🖼️ 生成高质量图片提示词\n    支持：Midjourney、SD、千问、豆包、Flux、DALL-E 等\n  • 🎬 生成高质量视频提示词\n    支持：Sora、Runway、即梦、可灵、Pika、Kling 等\n\n               ❗❗❗注意token额度❗❗❗\n\n   🎓 教你写提示词（输入\"教学模式\"/\"教我\"/\"怎么写\"即可进入）\n   💬 欢迎弹窗yayaxiong，希望能提出您宝贵的意见~帮助我继续完善SKILL\n  没有想法、不会用，可查阅：\"新手指南/如何使用\"~\n  SKILL在不断更新，若想完整体验，请移步workbuddy，搜索\"【提示词生成大师】\"添加SKILL",
    "_ref_by": [
      "research/research_base.funnel_L1_need.chat_fallback"
    ]
  },
  "beginner_guide": {
    "trigger_keywords": [
      "新手指南",
      "如何使用",
      "不会用",
      "怎么用",
      "没有想法",
      "help",
      "帮助",
      "新手引导"
    ],
    "_note": "当用户说以上任一关键词时，输出以下指南后终止流程。不加载其他模块。load:[], action: 输出后终止。",
    "guide_content": "一句话开始: 直接描述你想要的画面，越具体越好。\n示例: \"一只橘猫坐在雨天的窗台上，电影感\"\n\n进阶玩法(三要素): 告诉我这三个信息，效果最好:\n  1. 画什么? (主体)        例: 一个赛博朋克风的女孩\n  2. 什么感觉? (风格)     例: 类似银翼杀手那种暗调霓虹\n  3. 用什么工具? (平台)    例: Midjourney / 不确定可以让我推荐\n\n我还支持这些操作:\n  发一张参考图给我 -> 图生图 / 分析它的提示词\n  描述一段运动 -> 生成视频提示词\n  对上次的结果不满意? 说\"微调\"或指出哪里不对\n  想学习怎么写? 输入\"教学模式\"或\"教我\"\n\n小贴士:\n  - 说得越具体，生成的提示词越精准\n  - 不知道用什么平台? 告诉我用途(壁纸/头像/商业)，我来推荐\n  - 可以发中文，我会自动翻译成各平台适配格式",
    "_ref_by": [
      "research/research_base.skip_conditions"
    ]
  },
  "global_skip_conditions": {
    "_note": "这些条件优先于漏斗L1执行。命中即跳过调研直接进入指定路径。完整且唯一的skip定义，research和builder均引用此处。",
    "teach_mode": {
      "trigger": [
        "教我",
        "怎么写",
        "写作方法",
        "提示词技巧",
        "教学",
        "教程"
      ],
      "action": "跳过漏斗，type=teach，进builder教学段",
      "_reason": "教学模式不需要调研用户需求"
    },
    "tune_mode": {
      "condition": "用户消息含修改意图 且 前次输出存在上下文",
      "action": "跳过漏斗，进builder微调段",
      "_reason": "已有前次结果，只需定位修改字段"
    },
    "decompile_only": {
      "condition": "明确反编译请求 且 已上传文件",
      "action": "跳过漏斗L2-L5，进output反编译段",
      "_reason": "反编译是输入端分析，不需构建新提示词"
    },
    "three_elements_ready": {
      "condition": "渐进式5维覆盖模型(见research.skip_conditions.progressive_coverage)。旧版'三要素齐全'逻辑已废弃。",
      "_detail": "5维全覆盖(5/5)→直接构建；4/5→补全D5后构建；3/5及以下必须追问。D3平台是硬门槛，未覆盖绝对不能跳过。",
      "action": "根据覆盖率决定：N≥4进builder，N≤3进入调研话术",
      "_reason": "用户说了主体+风格但没说平台时，旧逻辑会错误跳过调研导致输出格式错误"
    }
  }
}