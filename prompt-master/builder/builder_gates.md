{
  "_meta": {
    "module": "builder-gates",
    "role": "gates G1-G5",
    "version": "v5.3"
  },
  "gates": {
    "G1_syntax": {
      "check": "平台语法匹配度",
      "mj": "自然语言+--参数",
      "sd": "(tag:weight)+[neg:-w]",
      "flux": "自然长句有限括号",
      "dall_e": "纯自然语言无符号",
      "video_universal": "英文自然叙事句无符号",
      "video_cn_domestic": "全中文自然描述无符号",
      "domestic_cn_image": "全中文自然描述无符号",
      "fix": "重组为正确语法"
    },
    "G2_conflict": {
      "check": "正反向矛盾检测",
      "fix": "移除矛盾项"
    },
    "G3_safety": {
      "_ref": "core.safety (唯一数据源)",
      "check": "安全违规复查，违规分类见core.safety: BLOCK/REFUSE/ADJUST/PHYSICS_WARN",
      "pass": "无BLOCK级且无REFUSE级违规项"
    },
    "G4_length": {
      "check": "长度合规，分平台执行不同标准",
      "_principle": "不同平台的最优长度差异巨大。国际平台(MJ/SD)吃标签堆叠，国内平台(豆包)吃短句精炼。必须按目标平台的标准裁剪，而非一刀切。",
      "standards": {
        "midjourney": {
          "max": 80,
          "unit": "关键词",
          "note": "MJ对长提示词宽容度高，但超过100词后效果递减"
        },
        "stable_diffusion": {
          "max": 75,
          "unit": "关键词(含权重标记)",
          "note": "SD的CLIP模型对前75词注意力最高，后面衰减快"
        },
        "flux": {
          "max": 300,
          "unit": "字符(英文)",
          "note": "Flux偏好自然段落，但超300字开始丢失细节"
        },
        "dall_e": {
          "max": 400,
          "unit": "字符",
          "note": "DALL-E 3支持长描述，但过长的场景描述会冲突"
        },
        "doubao": {
          "max": 80,
          "unit": "中文字",
          "note": "豆包硬限制，超出部分被截断或忽略。最佳区间40-70字"
        },
        "qwen": {
          "max": 150,
          "unit": "中文字",
          "note": "千问中等长度，分句清晰效果好"
        },
        "wenxin": {
          "max": 120,
          "unit": "中文字",
          "note": "文心偏精炼，超过120字注意力和质量双降"
        },
        "hunyuan": {
          "max": 120,
          "unit": "中文字",
          "note": "同文心"
        },
        "video_universal": {
          "max": 600,
          "unit": "字符(英文)",
          "note": "视频平台通用上限"
        },
        "video_cn_domestic": {
          "max": 200,
          "unit": "中文字",
          "note": "国内视频平台建议精简"
        }
      },
      "trim_priority": {
        "_rule": "超标时按以下顺序从低到高裁剪，保留高优先级内容",
        "priority_order": [
          {
            "tier": 1,
            "keep": [
              "主体描述",
              "核心风格词",
              "平台关键参数"
            ],
            "reason": "不可裁剪，这是用户明确要的"
          },
          {
            "tier": 2,
            "keep": [
              "主要环境/场景",
              "关键光影方向"
            ],
            "reason": "重要但可压缩为一句话"
          },
          {
            "tier": 3,
            "keep": [
              "构图视角",
              "色彩基调"
            ],
            "reason": "有则更好，没有也能生成"
          },
          {
            "tier": 4,
            "trim_first": [
              "相机具体型号",
              "镜头参数(f/1.8等)",
              "film grain等质感细节",
              "重复的同义词",
              "very/really等弱修饰词",
              "第二套以上的风格同义词"
            ],
            "reason": "装饰性元素，最先牺牲"
          }
        ]
      },
      "overflow_action": "先按trim_priority裁剪，裁后仍超标则触发G5_quality进一步精简"
    },
    "G5_quality": {
      "check": "关键词质量",
      "remove": [
        "very",
        "really",
        "beautifully",
        "amazingly"
      ],
      "replace_with_specific": true
    }
  },
  "focus_mechanism": {
    "_status": "MOVED_UPSTREAM",
    "_note": "v5.3起，focus_mechanism从builder内部提升为独立节点(位于research与builder之间)。本段保留作为规则参考定义。执行时机由SKILL.md flow的聚焦节点控制，不再由builder内部触发。",
    "_problem_solved": "解决'什么都要'导致的提示词无焦点问题。没有焦点的提示词=每个维度平均用力=每个效果都打折",
    "_when": "在字段填充完成后、模板组装前执行。先聚焦再构建，而非构建完再裁剪。",
    "_core_idea": "一张好图只需要1个视觉锚点+2个支撑元素，不是6个维度的总和。",
    "_integration_point": "research输出detail_json -> 聚焦层(focus)输出focused_json -> builder接收focused_json后直接填充编译",
    "steps": [
      {
        "step": 1,
        "name": "确定主锚点(Primary Anchor)",
        "ask": "用户最想让人第一眼看到/感受到的是什么？",
        "capture_from": "research阶段用户强调最多的词/重复提到的元素/情绪词",
        "examples": {
          "'橘猫'是锚点": "猫的表情和姿态是核心，其他都是衬托",
          "'赛博朋克氛围'是锚点": "霓虹光影是核心，具体物体可模糊处理",
          "'电影感'是锚点": "构图和影调是核心，主体可以简化"
        },
        "_rule": "只能选1个锚点，不可多选。犹豫时选用户输入中最早出现的具象名词。"
      },
      {
        "step": 2,
        "name": "选择2个支撑元素(Supporting Elements)",
        "options": [
          "风格/画风",
          "光影/色调",
          "环境/场景",
          "构图/视角",
          "情绪/氛围"
        ],
        "rule": "从以上5个中选最服务于锚点的2个，其余放弃或降级为1个词带过",
        "example": "锚点=橘猫 → 支撑=[环境:雨后街道] + [风格:电影感] → 放弃[相机参数][色彩细节][质感描述]"
      },
      {
        "step": 3,
        "name": "分配字数/词数预算",
        "budget_table": {
          "midjourney": {
            "anchor": "40%",
            "support_each": "20%",
            "others_total": "20%"
          },
          "stable_diffusion": {
            "anchor_weight": "1.4+",
            "support_weight": "1.2+",
            "others_weight": "1.0"
          },
          "doubao": {
            "anchor": "25-30字",
            "support_each": "10-15字",
            "others_total": "≤10字"
          },
          "qwen": {
            "anchor": "40-50字",
            "support_each": "20-30字",
            "others_total": "≤30字"
          },
          "flux/dall_e": {
            "anchor": "1-2句",
            "support_each": "1句",
            "others_total": "半句"
          }
        }
      },
      {
        "step": 4,
        "name": "按预算构建，超出的直接丢弃不进入输出",
        "anti_pattern": "禁止行为：把收集到的所有信息都塞进输出",
        "check_question": "如果删掉这句话，用户要的核心效果还在吗？在→可删 | 不在→保留"
      }
    ],
    "output_format": "内部使用，对用户不可见。最终输出的是聚焦后的提示词本身。",
    "_integration_note": "builder不再主动调用focus。focused_json由上游聚焦层传入，builder只负责填充+编译。"
  }
}