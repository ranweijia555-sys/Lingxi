"""塔罗体系化分析模块 - 基于元素和灵数（升级版：支持 78 张全牌）"""
from collections import Counter
from tarot.data_loader import load_full_deck, get_tarot_system, reduce_number


FULL_DECK = load_full_deck()
# 兼容旧代码：保留 MAJOR_ARCANA 别名指向完整牌组
MAJOR_ARCANA = FULL_DECK


def analyze_elements(cards):
    """分析三张牌的元素分布"""
    elements = []
    for card_info in cards:
        card = card_info["card"]
        element = FULL_DECK[card].get("element", "未知")
        elements.append(element)
    
    counter = Counter(elements)
    dominant = counter.most_common(1)[0]  # 最多的元素
    
    system = get_tarot_system()
    element_info = system["elements"].get(dominant[0], {})
    
    return {
        "distribution": dict(counter),
        "dominant_element": dominant[0],
        "dominant_count": dominant[1],
        "domain": element_info.get("domain", ""),
        "focus": element_info.get("focus", "")
    }


def analyze_numerology(cards):
    """分析三张牌的灵数（归元后）"""
    system = get_tarot_system()
    numerology_meanings = system["numerology_deep"]["meanings"]
    
    results = []
    for card_info in cards:
        card = card_info["card"]
        card_data = FULL_DECK[card]
        number = card_data.get("number")
        
        if number is None:
            # 宫廷牌没有数字
            results.append({
                "card": card,
                "number": None,
                "reduced": None,
                "meaning": f"宫廷牌（{card_data.get('court_role', '?')}）— 非数字牌，重在角色能量"
            })
            continue
        
        reduced = reduce_number(number) if number > 0 else 0
        
        if reduced == 0:
            meaning = "特殊牌（愚者）— 0 代表无限可能与起点之前的纯粹"
        else:
            meaning = numerology_meanings.get(str(reduced), "?")
        
        results.append({
            "card": card,
            "number": number,
            "reduced": reduced,
            "meaning": meaning
        })
    return results


def build_analysis_report(cards, core_card):
    """生成完整的体系化分析报告（喂给 AI 用）"""
    element_analysis = analyze_elements(cards)
    numerology_analysis = analyze_numerology(cards)
    
    # 每张牌的详细信息（按牌型显示）
    cards_detail_lines = []
    for card_info in cards:
        card = card_info["card"]
        info = FULL_DECK[card]
        orientation = "正位" if card_info["orientation"] == "upright" else "逆位"
        
        if info.get("is_court"):
            # 宫廷牌
            cards_detail_lines.append(
                f"- {card}（{orientation}）：花色={info.get('minor_suit', '?')}（{info.get('element', '?')}），"
                f"角色={info.get('court_role', '?')}（{info.get('court_element', '?')}）"
            )
        elif info.get("suit") == "minor":
            # 小阿卡纳数字牌
            cards_detail_lines.append(
                f"- {card}（{orientation}）：花色={info.get('minor_suit', '?')}（{info.get('element', '?')}），"
                f"编号={info.get('number', '?')}"
            )
        else:
            # 大阿卡纳
            cards_detail_lines.append(
                f"- {card}（{orientation}）：元素={info.get('element', '?')}，"
                f"占星={info.get('planet', '?')}，编号={info.get('number', '?')}"
            )
    
    cards_detail = "\n".join(cards_detail_lines)
    
    # 核心牌的详细信息
    core_info = FULL_DECK[core_card["card"]]
    core_number = core_info.get("number")
    if core_number is None:
        core_reduced = None  # 宫廷牌
    else:
        core_reduced = reduce_number(core_number) if core_number > 0 else 0
    
    # 报告开头（三张牌 + 元素分布 + 灵数）
    report = f"""【三张牌的元素与占星】
{cards_detail}

【元素分布】
- 元素占比：{element_analysis['distribution']}
- 主导元素：{element_analysis['dominant_element']}（{element_analysis['domain']}）
- 关注核心：{element_analysis['focus']}

【灵数分析】"""
    
    for item in numerology_analysis:
        if item["number"] is None:
            report += f"\n- {item['card']}：{item['meaning']}"
        else:
            report += f"\n- {item['card']}：编号 {item['number']} → 归元 {item['reduced']} → {item['meaning']}"
    
    # 核心牌深度信息（按牌型分情况）
    orientation_zh = '正位' if core_card['orientation'] == 'upright' else '逆位'
    
    if core_info.get("is_court"):
        # 宫廷牌
        report += f"""

【核心牌深度信息】
- 牌名：{core_card['card']}
- 类型：宫廷牌（{core_info.get('court_role', '?')}）
- 花色：{core_info.get('minor_suit', '?')}（{core_info.get('element', '?')} 元素）
- 角色元素：{core_info.get('court_element', '?')}
- 正/逆位：{orientation_zh}"""
    elif core_info.get("suit") == "minor":
        # 小阿卡纳数字牌
        report += f"""

【核心牌深度信息】
- 牌名：{core_card['card']}
- 类型：小阿卡纳数字牌
- 花色：{core_info.get('minor_suit', '?')}（{core_info.get('element', '?')} 元素）
- 编号：{core_number} → 归元为 {core_reduced}
- 正/逆位：{orientation_zh}"""
    else:
        # 大阿卡纳
        report += f"""

【核心牌深度信息】
- 牌名：{core_card['card']}
- 类型：大阿卡纳
- 元素：{core_info.get('element', '未知')}
- 占星对应：{core_info.get('planet', '未知')}
- 编号：{core_number} → 归元为 {core_reduced}
- 正/逆位：{orientation_zh}"""
    
    return report


if __name__ == "__main__":
    from tarot.drawer import draw_cards, find_core_card
    
    cards = draw_cards(3)
    core = find_core_card(cards)
    report = build_analysis_report(cards, core)
    print(report)