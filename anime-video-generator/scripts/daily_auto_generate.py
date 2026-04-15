#!/usr/bin/env python3
"""
每日自动生成动漫短视频脚本
从腾讯视频国漫角色库中随机选取一位角色，自动生成 15-30 秒短视频。

使用方式：
    python3 daily_auto_generate.py --token <TOKEN> [--output-dir ./videos] [--duration 30] [--resolution 720p]
    python3 daily_auto_generate.py --token <TOKEN> --publish-xiaohongshu --publish-douyin

依赖：requests
"""

import argparse
import json
import os
import random
import sys
import time
import importlib.util
from datetime import datetime

# ==================== 国漫角色数据库 ====================
# 格式: {"name": 角色名, "gender": 性别, "anime": 动漫名, "scenes": [场景描述列表]}
CHARACTER_DATABASE = [
    # ===== 斗罗大陆 =====
    {
        "name": "唐三", "gender": "男", "anime": "斗罗大陆",
        "scenes": [
            "蓝银草武魂觉醒，蓝色光芒从掌心涌出，神秘森林背景，月光照耀",
            "昊天锤第二武魂显现，黑色巨锤凌空，雷电环绕，气势磅礴",
            "海神岛试炼，金色海神三叉戟在手，海浪翻涌，神光万丈",
            "成神之路，金光万丈，天地变色，神位降临，万众瞩目",
            "与比比东终极对决，双武魂齐出，蓝银与昊天交织",
        ],
    },
    {
        "name": "戴沐白", "gender": "男", "anime": "斗罗大陆",
        "scenes": [
            "白虎武魂附体，白色猛虎虚影笼罩全身，虎啸山林",
            "白虎流星雨技能释放，金色光点如流星般坠落",
            "与朱竹清双人武魂融合，幽冥白虎显现，黑白交织",
        ],
    },
    {
        "name": "奥斯卡", "gender": "男", "anime": "斗罗大陆",
        "scenes": [
            "食神之力觉醒，七彩光芒环绕，丹药浮空",
            "制作香肠武魂，搞笑而又实用的辅助场面，金光闪烁",
        ],
    },
    {
        "name": "马红俊", "gender": "男", "anime": "斗罗大陆",
        "scenes": [
            "邪火凤凰武魂释放，烈焰冲天，火焰凤凰展翅",
            "凤凰涅槃重生，浴火而出，金红色羽翼展开",
        ],
    },
    {
        "name": "小舞", "gender": "女", "anime": "斗罗大陆",
        "scenes": [
            "柔骨兔武魂显现，粉色光芒环绕，长发飘逸，月光下翩翩起舞",
            "为唐三献祭，化作粉色光点消散，催人泪下，温柔目光",
            "十万年魂环觉醒，金色光环升起，兔耳若隐若现",
            "复活归来，与唐三深情相拥，花瓣纷飞",
        ],
    },
    {
        "name": "朱竹清", "gender": "女", "anime": "斗罗大陆",
        "scenes": [
            "幽冥灵猫武魂，黑色猫影闪现，极速移动，夜色中的暗影",
            "幽冥斩技能释放，黑色刀光划破夜空，凌厉无比",
        ],
    },
    {
        "name": "宁荣荣", "gender": "女", "anime": "斗罗大陆",
        "scenes": [
            "九宝琉璃塔武魂释放，七彩琉璃光柱冲天，绚丽夺目",
            "辅助增幅全队，金色光环笼罩队友，温暖而强大",
        ],
    },
    # ===== 斗破苍穹 =====
    {
        "name": "萧炎", "gender": "男", "anime": "斗破苍穹",
        "scenes": [
            "异火吞噬，青莲地心火觉醒，蓝色火焰席卷全身，威压四方",
            "佛怒火莲释放，多色火莲在掌心旋转绽放，毁天灭地",
            "三年之约对决纳兰嫣然，一飞冲天，意气风发",
            "炎帝之路，吞噬陀舍古帝玉，帝焰降世，万火臣服",
        ],
    },
    {
        "name": "药尘", "gender": "男", "anime": "斗破苍穹",
        "scenes": [
            "炼药大师展示，丹炉中火焰翻涌，药香四溢，仙气缭绕",
            "骨灵冷火显现，白色幽冷火焰飘荡，诡异而强大",
        ],
    },
    {
        "name": "薰儿", "gender": "女", "anime": "斗破苍穹",
        "scenes": [
            "古族血脉觉醒，金色纹路浮现全身，高贵典雅",
            "与萧炎并肩作战，火焰与金光交织，默契无间",
        ],
    },
    {
        "name": "美杜莎女王", "gender": "女", "anime": "斗破苍穹",
        "scenes": [
            "蛇族女王霸气登场，紫色蛇瞳闪烁，冷艳逼人",
            "化形为人，绝美容颜显现，冷艳高贵，紫衣飘飘",
        ],
    },
    {
        "name": "云韵", "gender": "女", "anime": "斗破苍穹",
        "scenes": [
            "海波东冰封中觉醒，冰晶碎裂，寒气四溢",
            "御风飞行，白衣飘飘，云海之上，仙姿绰约",
        ],
    },
    # ===== 完美世界 =====
    {
        "name": "石昊", "gender": "男", "anime": "完美世界",
        "scenes": [
            "至尊骨觉醒，金色符文浮现胸口，光芒万丈",
            "荒天帝之姿，一人对抗万族，气吞山河，拳碎星辰",
            "雷劫之下突破，雷电交加中浴火重生，天地为之震颤",
            "与仙王对决，拳碎虚空，星辰陨落，无敌之姿",
        ],
    },
    {
        "name": "火灵儿", "gender": "女", "anime": "完美世界",
        "scenes": [
            "火灵族公主登场，通体火红，烈焰环绕，高贵不凡",
            "与石昊初遇，火焰与金光碰撞，电光火石",
        ],
    },
    # ===== 武动乾坤 =====
    {
        "name": "林动", "gender": "男", "anime": "武动乾坤",
        "scenes": [
            "吞噬祖符觉醒，黑色漩涡在掌心旋转，吞噬万物",
            "大荒试炼场中战斗，拳风呼啸，力量爆发",
            "与异魔族终极对决，祖符之力全开，天地为之变色",
        ],
    },
    {
        "name": "绫清竹", "gender": "女", "anime": "武动乾坤",
        "scenes": [
            "九天之主降临，冰蓝色光芒笼罩天地，清冷出尘",
            "冰灵之力释放，万物冰封，冰花绽放",
        ],
    },
    {
        "name": "应欢欢", "gender": "女", "anime": "武动乾坤",
        "scenes": [
            "暗之主力量觉醒，黑暗能量涌动，亦正亦邪",
            "复杂表情特写，光暗交织的内心挣扎",
        ],
    },
    # ===== 吞噬星空 =====
    {
        "name": "罗峰", "gender": "男", "anime": "吞噬星空",
        "scenes": [
            "星空中飞行，宇宙背景壮阔无比，星辰点点",
            "暗金色战刀劈斩，刀光划破星空，势不可挡",
            "与虫族大战，战甲覆体，力战群敌，英勇无畏",
            "不朽之火觉醒，金色火焰燃遍全身，超越极限",
        ],
    },
    {
        "name": "罗峰之妻许晴", "gender": "女", "anime": "吞噬星空",
        "scenes": [
            "温柔守候，夕阳下等待归来的身影，深情凝望",
        ],
    },
    # ===== 一念永恒 =====
    {
        "name": "白小纯", "gender": "男", "anime": "一念永恒",
        "scenes": [
            "不灭之火炼体，全身火焰缠绕却毫发无伤，坚韧不拔",
            "逆河宗试炼，搞怪又热血的战斗场面，笑中带泪",
            "通天河畔修炼，水花四溅，灵气汇聚，天人合一",
        ],
    },
    {
        "name": "杜灵儿", "gender": "女", "anime": "一念永恒",
        "scenes": [
            "剑修之姿，万剑齐发，剑光如雨，凌厉绝美",
            "与白小纯初遇，清冷气质，冰雪聪明",
        ],
    },
    # ===== 仙逆 =====
    {
        "name": "王林", "gender": "男", "anime": "仙逆",
        "scenes": [
            "逆仙之路，一步踏出万丈虚空，孤傲决绝",
            "古神之力觉醒，第三只眼睁开，天地变色，万物臣服",
            "星辰之下独行，孤傲背影，衣袂飘飘",
        ],
    },
    {
        "name": "李慕婉", "gender": "女", "anime": "仙逆",
        "scenes": [
            "红衣飘飘，回眸一笑，花瓣纷飞，倾国倾城",
        ],
    },
    # ===== 凡人修仙传 =====
    {
        "name": "韩立", "gender": "男", "anime": "凡人修仙传",
        "scenes": [
            "青竹蜂云剑齐出，万剑归宗，剑光璀璨",
            "化婴期突破，金丹碎裂化为元婴，天降异象",
            "与南宫婉并肩作战，剑光与法术交织，配合默契",
        ],
    },
    {
        "name": "南宫婉", "gender": "女", "anime": "凡人修仙传",
        "scenes": [
            "紫灵之力释放，紫色光芒璀璨，美丽而强大",
            "冰封千年后苏醒，冰晶缓缓碎裂，重见天日",
        ],
    },
    # ===== 少年歌行 =====
    {
        "name": "雷无桀", "gender": "男", "anime": "少年歌行",
        "scenes": [
            "天启剑出鞘，金色剑气冲天，势不可挡",
            "雪月城上独立，白衣胜雪，俯瞰天下",
        ],
    },
    {
        "name": "萧瑟", "gender": "男", "anime": "少年歌行",
        "scenes": [
            "百里东君之姿，红衣似火，潇洒不羁",
            "长刀出鞘，刀意纵横，快意恩仇",
        ],
    },
    {
        "name": "司空千落", "gender": "女", "anime": "少年歌行",
        "scenes": [
            "无双城主登场，霸气侧漏，英姿飒爽",
            "剑舞翩翩，花瓣与剑光齐飞，美不胜收",
        ],
    },
]

# ==================== 分镜模板 ====================
STORYBOARD_TEMPLATE = """你是一位专业的动漫视频分镜师。请根据角色信息和场景描述，为一个{duration}秒的动漫短视频设计{num_clips}个分镜片段。

角色信息：
- 角色名：{character_name}
- 所属动漫：{anime_name}
- 性别：{gender}
- 场景描述：{scene_desc}

要求：
1. 每个片段约5秒，需要有连贯的叙事逻辑
2. 包含镜头描述（远景/中景/近景/特写）
3. 描述角色动作、表情、特效
4. 添加动漫画风和画质描述
5. 输出为英文（视频生成模型对英文效果更好）
6. 每个片段控制在 50 词以内

请严格按以下 JSON 格式输出，不要有其他内容：
[
  {{"clip": 1, "prompt": "英文提示词"}},
  {{"clip": 2, "prompt": "英文提示词"}},
  ...
]"""

# ==================== 社交平台文案模板 ====================
SOCIAL_COPY_TEMPLATE = """你是一位专业的短视频运营文案策划。请为以下国漫角色短视频生成社交平台发布文案。

角色信息：
- 角色名：{character_name}
- 所属动漫：{anime_name}
- 场景：{scene_desc}

请生成以下内容（中文）：
1. 标题（15-30字，吸引眼球，包含角色名和动漫名）
2. 正文描述（50-100字，引发共鸣和互动）
3. 话题标签（5-8个，以#开头）

请严格按以下 JSON 格式输出，不要有其他内容：
{{
  "title": "标题内容",
  "description": "正文描述",
  "hashtags": ["#标签1", "#标签2", ...]
}}"""


def load_generate_video_module(script_dir: str):
    """动态加载 generate_video 模块"""
    module_path = os.path.join(script_dir, "generate_video.py")
    spec = importlib.util.spec_from_file_location("generate_video", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_concat_module(script_dir: str):
    """动态加载 concat_videos 模块"""
    module_path = os.path.join(script_dir, "concat_videos.py")
    spec = importlib.util.spec_from_file_location("concat_videos", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def random_select_character() -> dict:
    """从角色库中随机选取一位角色"""
    character = random.choice(CHARACTER_DATABASE)
    print(f"🎲 今日随机角色: {character['name']}（{character['gender']}）- 《{character['anime']}》")
    return character


def generate_storyboard(character: dict, token: str, duration: int = 30) -> list:
    """使用 AI 生成分镜脚本"""
    import requests
    
    num_clips = max(3, duration // 5)  # 每 5 秒一个片段
    scene_desc = random.choice(character["scenes"])
    
    print(f"📋 正在生成 {num_clips} 个分镜片段...")
    print(f"   场景: {scene_desc}")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": "hunyuan-turbos-latest",
        "messages": [
            {
                "role": "user",
                "content": STORYBOARD_TEMPLATE.format(
                    duration=duration,
                    num_clips=num_clips,
                    character_name=character["name"],
                    anime_name=character["anime"],
                    gender=character["gender"],
                    scene_desc=scene_desc,
                ),
            }
        ],
        "temperature": 0.8,
        "max_tokens": 1500,
    }
    
    try:
        api_base = os.environ.get("HUNYUAN_API_BASE", "https://api.hunyuan.cloud.tencent.com/v1")
        resp = requests.post(
            f"{api_base}/chat/completions",
            headers=headers,
            json=payload,
            timeout=60,
        )
        resp.raise_for_status()
        result = resp.json()
        content = result["choices"][0]["message"]["content"].strip()
        
        # 提取 JSON 部分
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        clips = json.loads(content)
        print(f"✅ 分镜生成完成，共 {len(clips)} 个片段")
        for clip in clips:
            print(f"   片段 {clip['clip']}: {clip['prompt'][:60]}...")
        return clips
        
    except Exception as e:
        print(f"⚠️ AI 分镜生成失败: {e}")
        print(f"   使用默认分镜模板...")
        # 回退：使用默认分镜
        return generate_default_storyboard(character, num_clips)


def generate_default_storyboard(character: dict, num_clips: int) -> list:
    """生成默认分镜（当 AI 生成失败时的回退方案）"""
    scene = random.choice(character["scenes"])
    name = character["name"]
    anime = character["anime"]
    
    templates = [
        f"Wide establishing shot, {name} from {anime} standing in mystical landscape, Chinese donghua style, atmospheric fog, cinematic lighting, 4K anime quality",
        f"Medium close-up of {name}, determined expression, wind blowing hair and clothes, detailed character design, Chinese anime style, dramatic lighting",
        f"Dynamic action shot, {name} unleashing power, {scene}, energy particles, vibrant special effects, fluid animation, epic Chinese donghua",
        f"Epic wide shot, {name} at full power, {scene}, massive energy explosion, spectacular visual effects, cinematic camera orbit, professional animation",
        f"Dramatic close-up, {name} transformation complete, glowing eyes, powerful aura, intricate details, Chinese donghua masterpiece quality",
        f"Final wide shot, {name} standing victorious, {scene}, golden light rays, peaceful aftermath, beautiful Chinese anime scenery, fade to light",
    ]
    
    clips = []
    for i in range(num_clips):
        idx = i % len(templates)
        clips.append({"clip": i + 1, "prompt": templates[idx]})
    return clips


def generate_social_copy(character: dict, token: str) -> dict:
    """使用 AI 生成社交平台发布文案"""
    import requests
    
    scene_desc = random.choice(character["scenes"])
    
    print(f"📝 正在生成社交平台文案...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": "hunyuan-turbos-latest",
        "messages": [
            {
                "role": "user",
                "content": SOCIAL_COPY_TEMPLATE.format(
                    character_name=character["name"],
                    anime_name=character["anime"],
                    scene_desc=scene_desc,
                ),
            }
        ],
        "temperature": 0.9,
        "max_tokens": 500,
    }
    
    try:
        api_base = os.environ.get("HUNYUAN_API_BASE", "https://api.hunyuan.cloud.tencent.com/v1")
        resp = requests.post(
            f"{api_base}/chat/completions",
            headers=headers,
            json=payload,
            timeout=60,
        )
        resp.raise_for_status()
        result = resp.json()
        content = result["choices"][0]["message"]["content"].strip()
        
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        copy_data = json.loads(content)
        print(f"✅ 文案生成完成")
        print(f"   标题: {copy_data['title']}")
        print(f"   描述: {copy_data['description'][:50]}...")
        print(f"   标签: {' '.join(copy_data['hashtags'])}")
        return copy_data
        
    except Exception as e:
        print(f"⚠️ AI 文案生成失败: {e}")
        # 回退：使用默认文案
        return {
            "title": f"【{character['anime']}】{character['name']}名场面 AI动漫重现！",
            "description": f"用AI重新演绎{character['anime']}中{character['name']}的经典场面，每一帧都是艺术！你最喜欢{character['name']}的哪个瞬间？评论区告诉我！",
            "hashtags": [
                f"#{character['anime']}", f"#{character['name']}",
                "#国漫", "#AI动漫", "#动漫短视频",
                "#二次元", "#国漫崛起",
            ],
        }


def publish_to_platform(
    video_path: str,
    copy_data: dict,
    platform: str,
    credentials: dict = None,
) -> dict:
    """
    发布视频到社交平台（框架接口）
    
    注意：小红书和抖音的开放 API 需要企业认证和审核。
    此函数提供标准化的发布接口，实际发布需要用户提供平台凭证。
    
    Args:
        video_path: 视频文件路径
        copy_data: 文案数据 {"title": ..., "description": ..., "hashtags": [...]}
        platform: 平台名称 ("xiaohongshu" / "douyin")
        credentials: 平台凭证 {"access_token": ..., "open_id": ...}
    
    Returns:
        发布结果 {"success": bool, "message": str, "url": str}
    """
    import requests
    
    if not credentials:
        return {
            "success": False,
            "message": f"未提供{platform}平台凭证，跳过发布。请配置 access_token 后重试。",
            "url": None,
        }
    
    title = copy_data["title"]
    description = copy_data["description"]
    hashtags = " ".join(copy_data["hashtags"])
    full_text = f"{description}\n\n{hashtags}"
    
    if platform == "xiaohongshu":
        return _publish_xiaohongshu(video_path, title, full_text, credentials)
    elif platform == "douyin":
        return _publish_douyin(video_path, title, full_text, credentials)
    else:
        return {"success": False, "message": f"不支持的平台: {platform}", "url": None}


def _publish_xiaohongshu(video_path: str, title: str, text: str, credentials: dict) -> dict:
    """
    发布到小红书
    
    小红书开放平台 API 文档: https://open.xiaohongshu.com/
    需要：企业号认证 + 开放平台应用审核 + access_token
    """
    import requests
    
    access_token = credentials.get("access_token")
    if not access_token:
        return {"success": False, "message": "缺少小红书 access_token", "url": None}
    
    print(f"📤 正在发布到小红书...")
    print(f"   标题: {title}")
    
    try:
        # 步骤1: 上传视频获取 video_id
        upload_url = "https://open.xiaohongshu.com/api/media/video/upload"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        with open(video_path, "rb") as f:
            files = {"file": (os.path.basename(video_path), f, "video/mp4")}
            resp = requests.post(upload_url, headers=headers, files=files, timeout=300)
        
        if resp.status_code != 200:
            return {"success": False, "message": f"视频上传失败: HTTP {resp.status_code} - {resp.text}", "url": None}
        
        upload_result = resp.json()
        video_id = upload_result.get("data", {}).get("video_id")
        
        # 步骤2: 创建笔记
        create_url = "https://open.xiaohongshu.com/api/note/publish"
        note_data = {
            "title": title,
            "content": text,
            "video_id": video_id,
            "type": "video",
        }
        resp = requests.post(create_url, headers=headers, json=note_data, timeout=60)
        
        if resp.status_code == 200:
            result = resp.json()
            note_id = result.get("data", {}).get("note_id", "")
            url = f"https://www.xiaohongshu.com/explore/{note_id}" if note_id else ""
            print(f"✅ 小红书发布成功！")
            return {"success": True, "message": "发布成功", "url": url}
        else:
            return {"success": False, "message": f"笔记创建失败: {resp.text}", "url": None}
            
    except Exception as e:
        return {"success": False, "message": f"小红书发布异常: {e}", "url": None}


def _publish_douyin(video_path: str, title: str, text: str, credentials: dict) -> dict:
    """
    发布到抖音
    
    抖音开放平台 API 文档: https://open.douyin.com/
    需要：开发者认证 + 应用审核 + access_token + open_id
    """
    import requests
    
    access_token = credentials.get("access_token")
    open_id = credentials.get("open_id")
    if not access_token or not open_id:
        return {"success": False, "message": "缺少抖音 access_token 或 open_id", "url": None}
    
    print(f"📤 正在发布到抖音...")
    print(f"   标题: {title}")
    
    try:
        # 步骤1: 上传视频
        upload_url = f"https://open.douyin.com/api/media/video/upload/?access_token={access_token}&open_id={open_id}"
        
        with open(video_path, "rb") as f:
            files = {"video": (os.path.basename(video_path), f, "video/mp4")}
            resp = requests.post(upload_url, files=files, timeout=300)
        
        if resp.status_code != 200:
            return {"success": False, "message": f"视频上传失败: HTTP {resp.status_code}", "url": None}
        
        upload_result = resp.json()
        video_id = upload_result.get("data", {}).get("video", {}).get("video_id")
        
        # 步骤2: 创建视频
        create_url = f"https://open.douyin.com/api/media/video/create/?access_token={access_token}&open_id={open_id}"
        create_data = {
            "video_id": video_id,
            "text": f"{title}\n{text}",
        }
        resp = requests.post(create_url, json=create_data, timeout=60)
        
        if resp.status_code == 200:
            result = resp.json()
            item_id = result.get("data", {}).get("item_id", "")
            print(f"✅ 抖音发布成功！")
            return {"success": True, "message": "发布成功", "url": f"https://www.douyin.com/video/{item_id}"}
        else:
            return {"success": False, "message": f"视频创建失败: {resp.text}", "url": None}
            
    except Exception as e:
        return {"success": False, "message": f"抖音发布异常: {e}", "url": None}


def daily_auto_generate(
    token: str,
    output_dir: str = None,
    duration: int = 30,
    resolution: str = "720p",
    publish_xiaohongshu: bool = False,
    publish_douyin: bool = False,
    xhs_credentials: dict = None,
    dy_credentials: dict = None,
) -> dict:
    """
    每日自动生成流程
    
    Args:
        token: 太湖平台 API Token
        output_dir: 输出目录
        duration: 视频时长（15-30秒）
        resolution: 分辨率
        publish_xiaohongshu: 是否发布到小红书
        publish_douyin: 是否发布到抖音
        xhs_credentials: 小红书凭证
        dy_credentials: 抖音凭证
    
    Returns:
        生成结果摘要
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if not output_dir:
        output_dir = os.path.join(os.getcwd(), "anime_videos")
    os.makedirs(output_dir, exist_ok=True)
    
    today = datetime.now().strftime("%Y%m%d")
    
    print("=" * 70)
    print(f"🌟 每日国漫短视频自动生成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # 步骤 1: 随机选取角色
    character = random_select_character()
    
    # 步骤 2: 生成分镜脚本
    clips_data = generate_storyboard(character, token, duration)
    
    # 步骤 3: 生成社交平台文案
    copy_data = generate_social_copy(character, token)
    
    # 步骤 4: 逐个生成视频片段
    gen_module = load_generate_video_module(script_dir)
    clip_files = []
    
    safe_name = character["name"].replace(" ", "_")
    
    for clip in clips_data:
        clip_num = clip["clip"]
        clip_prompt = clip["prompt"]
        clip_output = os.path.join(output_dir, f"{today}_{safe_name}_clip{clip_num:02d}.mp4")
        
        print(f"\n{'─' * 50}")
        print(f"🎬 正在生成片段 {clip_num}/{len(clips_data)}...")
        
        try:
            gen_module.generate_anime_video(
                prompt=clip_prompt,
                token=token,
                output=clip_output,
                resolution=resolution,
                optimize=False,  # 分镜已经是优化后的提示词
            )
            clip_files.append(clip_output)
        except Exception as e:
            print(f"⚠️ 片段 {clip_num} 生成失败: {e}")
            continue
    
    if not clip_files:
        print("❌ 所有片段生成失败，无法拼接视频")
        return {"success": False, "error": "所有片段生成失败"}
    
    # 步骤 5: 拼接视频
    final_output = os.path.join(output_dir, f"{today}_{safe_name}_final.mp4")
    
    if len(clip_files) > 1:
        concat_module = load_concat_module(script_dir)
        try:
            concat_module.concat_videos(clip_files, final_output, target_duration=duration)
        except Exception as e:
            print(f"⚠️ 拼接失败，使用第一个片段作为最终视频: {e}")
            import shutil
            shutil.copy2(clip_files[0], final_output)
    else:
        import shutil
        shutil.copy2(clip_files[0], final_output)
    
    # 步骤 6: 保存文案信息
    meta_path = os.path.join(output_dir, f"{today}_{safe_name}_meta.json")
    meta_data = {
        "date": today,
        "character": character["name"],
        "anime": character["anime"],
        "gender": character["gender"],
        "video_path": final_output,
        "copy": copy_data,
        "clips_count": len(clip_files),
        "duration": duration,
        "resolution": resolution,
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta_data, f, ensure_ascii=False, indent=2)
    print(f"📄 元数据已保存: {meta_path}")
    
    # 步骤 7: 发布到社交平台（如果授权）
    publish_results = {}
    
    if publish_xiaohongshu:
        result = publish_to_platform(final_output, copy_data, "xiaohongshu", xhs_credentials)
        publish_results["xiaohongshu"] = result
        if result["success"]:
            print(f"✅ 小红书发布成功: {result['url']}")
        else:
            print(f"⚠️ 小红书发布: {result['message']}")
    
    if publish_douyin:
        result = publish_to_platform(final_output, copy_data, "douyin", dy_credentials)
        publish_results["douyin"] = result
        if result["success"]:
            print(f"✅ 抖音发布成功: {result['url']}")
        else:
            print(f"⚠️ 抖音发布: {result['message']}")
    
    # 最终摘要
    print(f"\n{'=' * 70}")
    print(f"🎉 每日任务完成！")
    print(f"   角色: {character['name']}（《{character['anime']}》）")
    print(f"   视频: {final_output}")
    print(f"   标题: {copy_data['title']}")
    print(f"   标签: {' '.join(copy_data['hashtags'])}")
    if publish_results:
        for platform, result in publish_results.items():
            status = "✅ 成功" if result["success"] else f"❌ {result['message']}"
            print(f"   {platform}: {status}")
    print(f"{'=' * 70}")
    
    return {
        "success": True,
        "character": character,
        "video_path": final_output,
        "meta_path": meta_path,
        "copy": copy_data,
        "publish_results": publish_results,
    }


def main():
    parser = argparse.ArgumentParser(
        description="每日自动国漫短视频生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  %(prog)s --token YOUR_TOKEN
  %(prog)s --token YOUR_TOKEN --duration 15 --resolution 1080p
  %(prog)s --token YOUR_TOKEN --publish-xiaohongshu --xhs-token XHS_TOKEN
  %(prog)s --token YOUR_TOKEN --publish-douyin --dy-token DY_TOKEN --dy-openid DY_OPENID
        """,
    )
    
    parser.add_argument("--token", "-t", required=True, help="太湖平台 API Token")
    parser.add_argument("--output-dir", "-o", default=None, help="输出目录（默认: ./anime_videos）")
    parser.add_argument("--duration", "-d", type=int, default=30, choices=range(15, 31), metavar="15-30", help="视频时长（秒，15-30，默认30）")
    parser.add_argument("--resolution", "-r", choices=["480p", "720p", "1080p"], default="720p", help="视频分辨率")
    
    # 社交平台发布选项
    parser.add_argument("--publish-xiaohongshu", action="store_true", help="发布到小红书")
    parser.add_argument("--publish-douyin", action="store_true", help="发布到抖音")
    parser.add_argument("--xhs-token", default=None, help="小红书 access_token")
    parser.add_argument("--dy-token", default=None, help="抖音 access_token")
    parser.add_argument("--dy-openid", default=None, help="抖音 open_id")
    
    args = parser.parse_args()
    
    xhs_creds = {"access_token": args.xhs_token} if args.xhs_token else None
    dy_creds = {"access_token": args.dy_token, "open_id": args.dy_openid} if args.dy_token else None
    
    try:
        result = daily_auto_generate(
            token=args.token,
            output_dir=args.output_dir,
            duration=args.duration,
            resolution=args.resolution,
            publish_xiaohongshu=args.publish_xiaohongshu,
            publish_douyin=args.publish_douyin,
            xhs_credentials=xhs_creds,
            dy_credentials=dy_creds,
        )
        
        if result["success"]:
            print(f"\n📁 输出文件: {result['video_path']}")
            sys.exit(0)
        else:
            print(f"\n❌ 任务失败: {result.get('error', '未知错误')}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 任务失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
