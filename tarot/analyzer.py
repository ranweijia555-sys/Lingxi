"""塔罗体系化分析模块 - 基于元素和灵数"""
from collections import Counter
from tarot.data_loader import load_major_arcana, get_tarot_system, reduce_number


MAJOR_ARCANA = load_major_arcana()


def analyze_elements(cards):
    """分析三张牌的元素分布"""
    elements = []
    for card_info in cards:
        card = card_info["card"]
        element = MAJOR_ARCANA[card].get("element", "未知")
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
        number = MAJOR_ARCANA[card]["number"]
        reduced = reduce_number(number) if number > 0 else 0
        
        meaning = numerology_meanings.get(str(reduced), "特殊牌（愚者）")
        
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
    
    # 每张牌的元素+占星详细信息
    cards_detail_lines = []
    for card_info in cards:
        card = card_info["card"]
        info = MAJOR_ARCANA[card]
        orientation = "正位" if card_info["orientation"] == "upright" else "逆位"
        cards_detail_lines.append(
            f"- {card}（{orientation}）：元素={info.get('element', '?')}，"
            f"占星={info.get('planet', '?')}，编号={info['number']}"
        )
    cards_detail = "\n".join(cards_detail_lines)
    
    # 核心牌的详细信息
    core_info = MAJOR_ARCANA[core_card["card"]]
    core_number = core_info["number"]
    core_reduced = reduce_number(core_number) if core_number > 0 else 0
    
    report = f"""【三张牌的元素与占星】
{cards_detail}

【元素分布】
- 元素占比：{element_analysis['distribution']}
- 主导元素：{element_analysis['dominant_element']}（{element_analysis['domain']}）
- 关注核心：{element_analysis['focus']}

【灵数分析】"""
    
    for item in numerology_analysis:
        report += f"\n- {item['card']}：编号 {item['number']} → 归元 {item['reduced']} → {item['meaning']}"
    
    report += f"""

【核心牌深度信息】
- 牌名：{core_card['card']}
- 元素：{core_info.get('element', '未知')}
- 占星对应：{core_info.get('planet', '未知')}
- 编号：{core_number} → 归元为 {core_reduced}
- 正/逆位：{'正位' if core_card['orientation'] == 'upright' else '逆位'}"""
    
    return report


if __name__ == "__main__":
    # 测试一下
    from tarot.drawer import draw_cards, find_core_card
    
    cards = draw_cards(3)
    core = find_core_card(cards)
    report = build_analysis_report(cards, core)
    print(report)