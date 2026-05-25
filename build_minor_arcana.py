"""构建 56 张小阿卡纳 JSON 数据"""
import json
import os

# 花色定义
SUITS = {
    "wands": {
        "name_zh": "权杖", "name_en": "Wands",
        "element": "火", "domain": "事业、行动、热情"
    },
    "cups": {
        "name_zh": "圣杯", "name_en": "Cups",
        "element": "水", "domain": "感情、情绪、心理"
    },
    "swords": {
        "name_zh": "宝剑", "name_en": "Swords",
        "element": "风", "domain": "理智、冲突、压力"
    },
    "pentacles": {
        "name_zh": "星币", "name_en": "Pentacles",
        "element": "土", "domain": "物质、财运、身体"
    }
}

# 数字牌中文名映射
NUMBER_NAMES = {
    1: "Ace 一", 2: "二", 3: "三", 4: "四", 5: "五",
    6: "六", 7: "七", 8: "八", 9: "九", 10: "十"
}

# 宫廷牌定义
COURT_CARDS = {
    "page": {"name_zh": "侍从", "name_en": "Page"},
    "knight": {"name_zh": "骑士", "name_en": "Knight"},
    "queen": {"name_zh": "王后", "name_en": "Queen"},
    "king": {"name_zh": "国王", "name_en": "King"}
}

# 56 张小牌的正/逆位含义（标准 Rider-Waite 体系）
MINOR_MEANINGS = {
    # === 权杖组 (火 - 行动、激情、意志) ===
    "wands_1": {"upright": "灵感、新机会、成长冲动", "reversed": "延迟、缺乏方向、灵感受阻"},
    "wands_2": {"upright": "规划、未来选择、个人力量", "reversed": "恐惧未知、缺乏计划、自我怀疑"},
    "wands_3": {"upright": "远见、扩展、机会到来", "reversed": "障碍、延迟、缺乏远见"},
    "wands_4": {"upright": "庆祝、家、稳定的成就", "reversed": "不和谐、家庭紧张、临时性"},
    "wands_5": {"upright": "冲突、竞争、分歧", "reversed": "避免冲突、内部紧张、和解"},
    "wands_6": {"upright": "胜利、公众认可、自信", "reversed": "失败、缺乏认可、自我怀疑"},
    "wands_7": {"upright": "坚持、防御、立场", "reversed": "屈服、压力过大、放弃"},
    "wands_8": {"upright": "快速行动、消息到来、势能", "reversed": "延迟、混乱、错失时机"},
    "wands_9": {"upright": "韧性、坚持到底、防备", "reversed": "偏执、防御过度、疲惫"},
    "wands_10": {"upright": "负担、责任过重、压力", "reversed": "释放负担、寻求帮助、减负"},
    "wands_page": {"upright": "探索新方向、热情、好奇", "reversed": "缺乏方向、虎头蛇尾、不成熟"},
    "wands_knight": {"upright": "行动、激情、冲动前行", "reversed": "鲁莽、急躁、缺乏耐心"},
    "wands_queen": {"upright": "自信、热情、个人魅力", "reversed": "嫉妒、不安全感、控制欲"},
    "wands_king": {"upright": "远见、领导力、果敢决策", "reversed": "专制、急躁、滥用权力"},

    # === 圣杯组 (水 - 情感、关系、直觉) ===
    "cups_1": {"upright": "新感情、情感丰盛、心灵滋养", "reversed": "情感堵塞、压抑、空虚"},
    "cups_2": {"upright": "伙伴、和谐、相互吸引", "reversed": "失衡、分离、误解"},
    "cups_3": {"upright": "庆祝、友谊、社交喜悦", "reversed": "过度沉溺、八卦、群体疏离"},
    "cups_4": {"upright": "不满、冷漠、错失机会", "reversed": "重新参与、觉醒、新视角"},
    "cups_5": {"upright": "失落、悲伤、专注于损失", "reversed": "接受、原谅、向前看"},
    "cups_6": {"upright": "怀旧、童年、纯真", "reversed": "困在过去、长大、放下回忆"},
    "cups_7": {"upright": "选择、幻想、机会迷茫", "reversed": "清晰、做出决定、看清现实"},
    "cups_8": {"upright": "离开、寻找意义、放下", "reversed": "害怕改变、停滞、留恋"},
    "cups_9": {"upright": "满足、愿望成真、情感丰盛", "reversed": "不满足、表面快乐、贪心"},
    "cups_10": {"upright": "圆满、家庭幸福、情感和谐", "reversed": "家庭不和、关系破裂、表面和睦"},
    "cups_page": {"upright": "直觉信息、好奇、敏感", "reversed": "情绪化、不成熟、过度敏感"},
    "cups_knight": {"upright": "浪漫、追求、理想主义", "reversed": "善变、不现实、情绪化"},
    "cups_queen": {"upright": "同情、直觉、滋养他人", "reversed": "情感失衡、依赖、过度付出"},
    "cups_king": {"upright": "情感平衡、智慧、外交", "reversed": "情感操纵、冷漠、压抑"},

    # === 宝剑组 (风 - 思想、冲突、决断) ===
    "swords_1": {"upright": "清晰、突破、新想法", "reversed": "困惑、思维阻塞、错误判断"},
    "swords_2": {"upright": "抉择、僵局、暂时平衡", "reversed": "做出决定、释放压力"},
    "swords_3": {"upright": "心碎、悲痛、背叛之痛", "reversed": "疗愈、释放伤痛、原谅"},
    "swords_4": {"upright": "休息、反思、恢复元气", "reversed": "倦怠、不安、强迫休息"},
    "swords_5": {"upright": "冲突、失败、不光彩的胜利", "reversed": "和解、原谅、放下争执"},
    "swords_6": {"upright": "过渡、放手、前行", "reversed": "困住、阻力、不愿前进"},
    "swords_7": {"upright": "策略、独行、隐藏意图", "reversed": "坦白、被发现、寻求帮助"},
    "swords_8": {"upright": "受困、自我设限、恐惧", "reversed": "释放、看清自己的力量"},
    "swords_9": {"upright": "焦虑、噩梦、担忧", "reversed": "内心平静、希望、走出焦虑"},
    "swords_10": {"upright": "痛苦的结束、谷底", "reversed": "复苏、新开始、最坏的过去了"},
    "swords_page": {"upright": "好奇、新想法、警觉观察", "reversed": "八卦、急躁、片面思考"},
    "swords_knight": {"upright": "果断、冲动追求真相", "reversed": "鲁莽、攻击性、缺乏耐心"},
    "swords_queen": {"upright": "理性、独立、清醒智慧", "reversed": "冷漠、刻薄、过度批判"},
    "swords_king": {"upright": "权威、清晰、客观判断", "reversed": "专制、操纵、滥用智力"},

    # === 星币组 (土 - 物质、工作、身体) ===
    "pentacles_1": {"upright": "新机会、繁荣、丰盛种子", "reversed": "错失机会、贪婪、规划不足"},
    "pentacles_2": {"upright": "平衡、灵活、多任务管理", "reversed": "失衡、混乱、应付不来"},
    "pentacles_3": {"upright": "团队合作、技能展示、规划", "reversed": "缺乏团队、敷衍、技能不足"},
    "pentacles_4": {"upright": "节制、控制、安全感", "reversed": "物质主义、贪婪、紧握不放"},
    "pentacles_5": {"upright": "贫困、担忧、被排斥感", "reversed": "恢复、改善、走出困境"},
    "pentacles_6": {"upright": "给予、分享、公平交换", "reversed": "不公、自私、不平等关系"},
    "pentacles_7": {"upright": "评估、耐心、长远投资", "reversed": "缺乏回报、不耐烦、放弃太早"},
    "pentacles_8": {"upright": "学习、精进、专注磨练", "reversed": "缺乏专注、敷衍、技艺停滞"},
    "pentacles_9": {"upright": "富足、独立、享受成果", "reversed": "物质过度、孤独、空虚"},
    "pentacles_10": {"upright": "财富、家族传承、长期保障", "reversed": "财务危机、家族争议、不稳定"},
    "pentacles_page": {"upright": "学习、新机会、专注培养", "reversed": "缺乏目标、拖延、不切实际"},
    "pentacles_knight": {"upright": "稳定、勤奋、可靠推进", "reversed": "停滞、过于谨慎、缺乏热情"},
    "pentacles_queen": {"upright": "务实、滋养、丰盛母性", "reversed": "物质失衡、忽视自我、过度劳碌"},
    "pentacles_king": {"upright": "成功、可靠、物质保障", "reversed": "物质执着、固执、忽视精神"}
}

# 宫廷牌的本体元素（人物属性，不同于花色元素）
COURT_ELEMENT = {
    "page": "风", "knight": "火", "queen": "水", "king": "土"
}


def build_cards():
    """生成 56 张小阿卡纳数据"""
    cards = []
    
    for suit_key, suit_info in SUITS.items():
        # 1. 数字牌 1-10
        for num in range(1, 11):
            meaning_key = f"{suit_key}_{num}"
            number_label = NUMBER_NAMES[num]
            
            key = f"{suit_info['name_en']} {number_label} {suit_info['name_zh']}{number_label}"
            
            cards.append({
                "key": key,
                "name_en": f"{number_label} of {suit_info['name_en']}",
                "name_zh": f"{suit_info['name_zh']}{number_label}",
                "suit": "minor",
                "minor_suit": suit_info["name_zh"],
                "minor_suit_en": suit_info["name_en"],
                "number": num,
                "element": suit_info["element"],
                "is_court": False,
                "domain": suit_info["domain"],
                "upright": MINOR_MEANINGS[meaning_key]["upright"],
                "reversed": MINOR_MEANINGS[meaning_key]["reversed"]
            })
        
        # 2. 宫廷牌
        for court_key, court_info in COURT_CARDS.items():
            meaning_key = f"{suit_key}_{court_key}"
            
            key = f"{court_info['name_en']} of {suit_info['name_en']} {suit_info['name_zh']}{court_info['name_zh']}"
            
            cards.append({
                "key": key,
                "name_en": f"{court_info['name_en']} of {suit_info['name_en']}",
                "name_zh": f"{suit_info['name_zh']}{court_info['name_zh']}",
                "suit": "minor",
                "minor_suit": suit_info["name_zh"],
                "minor_suit_en": suit_info["name_en"],
                "number": None,
                "court_role": court_info["name_zh"],
                "court_role_en": court_info["name_en"],
                "element": suit_info["element"],
                "court_element": COURT_ELEMENT[court_key],
                "is_court": True,
                "domain": suit_info["domain"],
                "upright": MINOR_MEANINGS[meaning_key]["upright"],
                "reversed": MINOR_MEANINGS[meaning_key]["reversed"]
            })
    
    return cards


def main():
    cards = build_cards()
    
    output = {
        "version": "1.0",
        "type": "minor_arcana",
        "count": len(cards),
        "cards": cards
    }
    
    os.makedirs("knowledge_base/structured", exist_ok=True)
    output_path = "knowledge_base/structured/minor_arcana.json"
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    # 输出统计
    print(f"✅ 成功导出 {len(cards)} 张小阿卡纳牌")
    print(f"📁 保存位置：{output_path}")
    print()
    
    suit_counts = {}
    court_count = 0
    for c in cards:
        suit_counts[c["minor_suit"]] = suit_counts.get(c["minor_suit"], 0) + 1
        if c["is_court"]:
            court_count += 1
    
    print("📊 统计：")
    for suit, count in suit_counts.items():
        print(f"   {suit}：{count} 张")
    print(f"   宫廷牌总数：{court_count} 张")


if __name__ == "__main__":
    main()