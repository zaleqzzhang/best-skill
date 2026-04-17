#!/usr/bin/env python3
"""
gen_travel_image.py - 根据行程描述生成手绘风旅游攻略插画

用法：
  python3 gen_travel_image.py \
    --day "Day1" \
    --date "4月29日" \
    --city "武汉" \
    --spots "黄鹤楼,长江轮渡,巴公房子" \
    --foods "热干面,鲜鱼糊汤粉,蛋酒" \
    --theme "古迹+美食+夜游" \
    --output "./output.png"

输出：提示词 JSON（供 image_gen 工具使用）
"""

import argparse
import json
import sys


PROMPT_TEMPLATE = """Highly detailed hand-drawn watercolor travel journal page, Chinese xiaohongshu diary style. \
Kraft paper notebook texture background. \
Title badge: "{day} {date} {city}游记 🗺️" in cute brush style with small star and heart decorations.

Main illustrated scenes ({theme}):
{scene_block}

Food section with cute illustrated dishes:
{food_block}

DECORATIVE ELEMENTS scattered throughout: compass rose, cherry blossom petals, star sparkles, \
tiny camera icon, chopsticks doodle, heart shapes, small flower doodles, washi tape strips, \
polaroid photo frames with handwritten captions.

COLOR PALETTE: warm cream paper background, soft watercolors — coral red, sage green, golden yellow, \
sky blue, warm brown ink outlines. Each element has visible watercolor brush strokes and pen ink detail.
Style: professional travel journal illustration, cozy xiaohongshu aesthetic, HIGH DETAIL quality."""


def build_scene_block(spots: list[str]) -> str:
    lines = []
    for i, spot in enumerate(spots, 1):
        lines.append(f"{i}. Detailed watercolor illustration of 【{spot}】 with atmospheric lighting and local flavor")
    return "\n".join(lines)


def build_food_block(foods: list[str]) -> str:
    lines = []
    for food in foods:
        lines.append(f"- 【{food}】: steaming, appetizing, with handwritten label and cute price tag")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='生成旅游手绘插画提示词')
    parser.add_argument('--day',    required=True, help='天数，如 Day1')
    parser.add_argument('--date',   required=True, help='日期，如 4月29日')
    parser.add_argument('--city',   required=True, help='城市，如 武汉')
    parser.add_argument('--spots',  required=True, help='景点列表，逗号分隔')
    parser.add_argument('--foods',  required=True, help='美食列表，逗号分隔')
    parser.add_argument('--theme',  default='景点+美食',  help='主题描述')
    parser.add_argument('--output', default=None,  help='输出 JSON 文件路径（默认打印到标准输出）')
    args = parser.parse_args()

    spots = [s.strip() for s in args.spots.split(',') if s.strip()]
    foods = [f.strip() for f in args.foods.split(',') if f.strip()]

    prompt = PROMPT_TEMPLATE.format(
        day=args.day,
        date=args.date,
        city=args.city,
        theme=args.theme,
        scene_block=build_scene_block(spots),
        food_block=build_food_block(foods),
    )

    result = {
        "prompt": prompt,
        "quality": "high",
        "size": "1024x1536",
        "style": "natural",
        "suggested_filename": f"{args.city}_{args.day}_手绘攻略.png"
    }

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"✅ 提示词已保存到：{args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
