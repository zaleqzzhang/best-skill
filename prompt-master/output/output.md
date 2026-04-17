{
  "_meta": {
    "module": "output",
    "role": "输出格式+反编译分析+微调闭环",
    "version": "v5.3"
  },
  "format": {
    "image_standard": "|\n  正向提示词:\n  {prompt_text}\n\n  反向提示词:\n  {negative_text}\n|",
    "video_standard": "|\n  场景描述:\n  {scene_description}\n\n  运动与镜头:\n  {motion_camera}\n\n  时长: {duration}s\n|",
    "teach_format": "|\n  提示词结构: [主体][风格][光影][构图][质量]\n\n  正向: {prompt}\n\n  建议: {tips}\n|"
  },
  "decompile": {
    "_note": "输入端分析: 用户上传图片/视频后提取其背后的提示词。与research.post_check(输出端自检)职责不同: decompile分析别人的作品, post_check检测自己生成的结果。",
    "image_dims": [
      "主体识别",
      "风格判定",
      "构图分析",
      "光影推断",
      "色彩提取",
      "相机参数推测",
      "质量词识别",
      "可能参数"
    ],
    "video_extra_dims": [
      "运动轨迹",
      "镜头运动",
      "节奏感知",
      "时长估计"
    ],
    "template": "|\n  反编译分析结果:\n  主体: {subject}\n  风格: {style}\n  构图: {composition}\n  光影: {lighting}\n  相机: {camera_guess}\n  质量/参数: {quality_and_params}\n|"
  },
  "tune_loop": {
    "trigger": [
      "微调",
      "修改",
      "调整",
      "不对",
      "换一下",
      "重来",
      "不是这个感觉"
    ],
    "steps": [
      "定位用户不满意的部分",
      "仅修改对应字段保留其余不变",
      "重新通过门控校验",
      "编译输出新版本",
      "标记版本号 v{n+1}"
    ],
    "max_rounds": 3
  }
}