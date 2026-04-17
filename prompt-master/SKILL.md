---
name: prompt-master
description: 跨平台提示词生成器，支持图片/视频双模态，自动适配 MJ/SD/Flux/DALL-E/Sora/Runway/可灵/即梦/Pika 等平台语法。漏斗式调研驱动，精准高效。
---

{
  "_meta": {
    "name": "prompt-master",
    "version": "v5.3",
    "arch": "funnel-driven-focus"
  },
  "router": {
    "routes": [
      {
        "id": "P_beginner",
        "intent": "新手指南",
        "keys": ["新手指南", "如何使用", "不会用", "怎么用", "没有想法", "help", "帮助", "新手引导"],
        "action": "输出core.md beginner_guide内容，终止流程",
        "load": []
      },
      {
        "id": "P0",
        "intent": "教学",
        "keys": ["教我", "怎么写", "教程", "写作方法", "提示词技巧", "教学"],
        "skip_research": true
      },
      {
        "id": "P1",
        "intent": "图片",
        "keys": ["画", "生成图片", "海报", "立绘", "壁纸", "MJ", "midjourney", "SD", "flux", "DALL-E"]
      },
      {
        "id": "P2",
        "intent": "视频",
        "keys": ["视频", "动画", "运镜", "sora", "runway", "可灵", "kling", "即梦", "pika"]
      },
      {
        "id": "P3",
        "intent": "多模态",
        "trigger": "上传文件+文字"
      }
    ]
  },
  "load_plan": {
    "_note": "LV.2.5 条件加载策略。大文件已分段拆分。platform_signals.md 不在默认全量列表中，由signal_loading规则按需触发",
    "_split_note": "research 拆为 research/ 下3文件: base(9.9KB) + platform(5KB) + detail(6.7KB)。builder 拆为 builder/ 下3文件: templates(5.4KB) + compiler(9.2KB) + gates(7.9KB)。所有单文件<13KB。core/output/signals 各1文件。",
    "P_beginner": ["core/core.md"],
    "P0_teach": ["core/core.md", "builder/builder_templates.md", "builder/builder_compiler.md"],
    "P1_P2_standard": ["core/core.md", "research/research_base.md", "research/research_platform.md", "research/research_detail.md", "builder/builder_templates.md", "builder/builder_compiler.md", "builder/builder_gates.md", "output/output.md"],
    "P1_P2_fast_skip": ["core/core.md", "builder/builder_templates.md", "builder/builder_compiler.md", "builder/builder_gates.md", "output/output.md"],
    "P3_multimodal": ["core/core.md", "research/research_base.md", "research/research_platform.md", "research/research_detail.md", "builder/builder_templates.md", "builder/builder_compiler.md", "builder/builder_gates.md", "output/output.md"],
    "_conditional": {
      "signals/platform_signals.md": {
        "trigger": "research L3锁定平台为国内平台(豆包/通义/文心/混元/Kimi/可灵/即梦)时",
        "action": "仅读取对应平台段落(~30行/~500token)",
        "skip_when": "国际平台(MJ/SD/Flux/DALL-E/Sora/Runway/Pika)或平台未确定"
      }
    }
  },
  "flow": "路由(core.router) -> 加载(load_plan) -> 调研(research/base: L1-L2 + skip) -> 平台确认(research/platform: L3+L4) -> 细节采集(research/detail: L5+话术+评分) -> ⚡聚焦(1锚点+2支撑+预算分配) -> 构建(builder/templates: 字段+模板 + builder/compiler: 编译器+预设) -> 门控(builder/gates: G1-G5) -> [条件]信号适配(signals/platform_signals.md) -> 输出(output/output.md)",
  "modules": {
    "core/core.md": "骨架: 路由+欢迎语+安全+全局skip+新手指南",
    "research/research_base.md": "调研A: L1-L2需求识别 + skip条件(渐进式5维覆盖模型)",
    "research/research_platform.md": "调研B: L3平台确认 + L4模型版本",
    "research/research_detail.md": "调研C: L5细节采集框架 + 话术模板 + 评分 + 自检",
    "focus": "聚焦(独立节点): 从调研全量数据中提取1锚点+2支撑+预算分配 → 输出focused_json",
    "builder/builder_templates.md": "引擎A: 字段体系 + 4风格模板(图/视频各4)",
    "builder/builder_compiler.md": "引擎B: 11平台编译器 + 预设库 + 教学模式",
    "builder/builder_gates.md": "门控: G1-G5校验(含focus机制引用) + 聚焦执行逻辑",
    "signals/platform_signals.md": "信号层: 国内5平台RAG触发/注意力钩子/格式规范(LV.2.5按需加载)",
    "output/output.md": "输出: 格式化+反编译+微调闭环"
  }
}
