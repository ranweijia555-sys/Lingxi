"""塔罗体系化分析模块 - 基于元素和灵数（升级版：支持 78 张全牌）"""
from collections import Counter
from tarot.data_loader import load_full_deck, get_tarot_system, reduce_number
from tarot.llm_client import get_text_client, TEXT_MODEL


FULL_DECK = load_full_deck()
# 兼容旧代码：保留 MAJOR_ARCANA 别名指向完整牌组
MAJOR_ARCANA = FULL_DECK

ALL_ELEMENTS = ["火", "水", "风", "土"]
_ELEMENT_ORDER = {element: index for index, element in enumerate(ALL_ELEMENTS)}

ELEMENT_PAIR_RELATIONSHIPS = {
    ("火", "风"): (
        "激发型",
        "火给风以方向，风给火以扩散；行动与思路互相点燃，适合快速启动但需防冲动决策。",
    ),
    ("火", "水"): (
        "拉扯型",
        "行动冲动与情感需求互相牵制，容易在「想做」和「感受是否对」之间反复摇摆。",
    ),
    ("火", "土"): (
        "落地型",
        "热情需要现实结构承载；议题焦点在如何把想法变成可执行、可衡量的步骤。",
    ),
    ("风", "水"): (
        "反思型",
        "理智审视情感，适合厘清感受背后的逻辑、动机与未被说出的需求。",
    ),
    ("风", "土"): (
        "策略型",
        "分析配合务实，适合先评估利弊、再制定计划，避免空想或蛮干。",
    ),
    ("水", "土"): (
        "滋养型",
        "情感与物质互相支撑；关系、资源与日常结构可以同步巩固。",
    ),
}

MISSING_ELEMENT_IMPLICATION = {
    "火": "缺火：行动启动不足，容易停留在想而未做、等而未动。",
    "水": "缺水：情感与直觉被回避，关系或内在感受未被正视。",
    "风": "缺风：视角与判断不足，可能看不清选项、逻辑链或沟通切口。",
    "土": "缺土：落地与资源不足，计划缺少现实锚点与可持续结构。",
}

_TRAJECTORY_DESCRIPTIONS = {
    "递进型": "归元数字整体走高，议题从起点向更高阶段推进，阻力主要在「是否愿意升级」。",
    "回归型": "归元数字回到起点附近或形成闭环，说明旧议题未完结，需要收尾或二次确认。",
    "拱形型": "中间牌归元数字最高，过程存在明显高潮或压力峰值，前后两牌是铺垫与回落。",
    "凹型": "中间牌归元数字最低，过程经历低谷或停滞，前后两牌提供进入与走出路径。",
    "混合型": "归元数字无单一清晰模式，说明多股力量并行，需按牌序逐段解读而非套用单一轨迹。",
}


def _normalize_element_pair(element_a, element_b):
    return tuple(sorted((element_a, element_b), key=_ELEMENT_ORDER.get))


def _describe_pair_relationship(element_a, element_b):
    key = _normalize_element_pair(element_a, element_b)
    relation = ELEMENT_PAIR_RELATIONSHIPS.get(key)
    if not relation:
        return None
    label, description = relation
    return f"{element_a}×{element_b}（{label}）：{description}"


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
        "focus": element_info.get("focus", ""),
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
                "meaning": f"宫廷牌（{card_data.get('court_role', '?')}）— 非数字牌，重在角色能量",
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
            "meaning": meaning,
        })
    return results


def analyze_element_tension(distribution):
    """根据元素分布返回元素张力描述"""
    present = [element for element in ALL_ELEMENTS if distribution.get(element, 0) > 0]
    missing = [element for element in ALL_ELEMENTS if distribution.get(element, 0) == 0]
    lines = []

    if not present:
        return "未识别到有效元素分布。"

    if len(present) == 1:
        element = present[0]
        count = distribution[element]
        system = get_tarot_system()
        element_info = system["elements"].get(element, {})
        lines.append(
            f"单一元素主导（{element}×{count}）：能量高度集中，议题几乎完全落在"
            f"{element_info.get('domain', '该元素领域')}，{element_info.get('focus', '需关注其单一视角带来的盲区')}。"
        )
    elif len(present) == 2:
        relation = _describe_pair_relationship(present[0], present[1])
        if relation:
            lines.append(f"双元素组合：{relation}")
        counts = "、".join(f"{element}×{distribution[element]}" for element in present)
        lines.append(f"当前占比：{counts}。")
    else:
        counts = "、".join(f"{element}×{distribution[element]}" for element in present)
        lines.append(f"多元素并存（{counts}）：议题跨多个层面，需按牌序观察元素如何依次作用。")
        pair_lines = []
        for index in range(len(present)):
            for inner in range(index + 1, len(present)):
                relation = _describe_pair_relationship(present[index], present[inner])
                if relation:
                    pair_lines.append(relation)
        if pair_lines:
            lines.append("主要元素互动：" + "；".join(pair_lines[:3]) + "。")

    if missing:
        lines.append("缺失元素提示：" + " ".join(MISSING_ELEMENT_IMPLICATION[element] for element in missing))

    return "\n".join(lines)


def _classify_numeric_trajectory(reduced_values):
    if len(reduced_values) < 2:
        return None

    if len(reduced_values) == 2:
        first, second = reduced_values
        if second > first:
            return "递进型"
        if second < first:
            return "回归型"
        return "混合型"

    if all(reduced_values[index] <= reduced_values[index + 1] for index in range(len(reduced_values) - 1)):
        return "递进型"
    if all(reduced_values[index] >= reduced_values[index + 1] for index in range(len(reduced_values) - 1)):
        return "回归型"

    first, last = reduced_values[0], reduced_values[-1]
    middle_values = reduced_values[1:-1]
    peak = max(reduced_values)
    valley = min(reduced_values)

    if middle_values and peak in middle_values and peak > first and peak > last:
        return "拱形型"
    if middle_values and valley in middle_values and valley < first and valley < last:
        return "凹型"
    if abs(first - last) <= 1 and peak - valley >= 2:
        return "回归型"
    return "混合型"


def analyze_numerology_trajectory(numerology_analysis):
    """分析归元数字的变化轨迹"""
    numeric_entries = [item for item in numerology_analysis if item["reduced"] is not None]
    court_cards = [item["card"] for item in numerology_analysis if item["reduced"] is None]
    lines = []

    if not numeric_entries:
        if court_cards:
            return (
                "本牌阵均为宫廷牌，无归元数字轨迹；解读重心在角色能量（"
                + "、".join(court_cards)
                + "）如何依次登场，而非数字升降。"
            )
        return "无可用归元数字，无法判断灵数轨迹。"

    sequence = " → ".join(
        f"{item['card']}({item['reduced']})" for item in numeric_entries
    )
    reduced_values = [item["reduced"] for item in numeric_entries]
    pattern = _classify_numeric_trajectory(reduced_values)
    lines.append(f"归元序列：{sequence}")
    if pattern:
        lines.append(f"轨迹模式：{pattern} — {_TRAJECTORY_DESCRIPTIONS[pattern]}")
    else:
        lines.append("轨迹模式：单牌归元，无跨牌升降可比，解读重心在该数字本身的阶段含义。")

    if court_cards:
        lines.append(
            "宫廷牌介入："
            + "、".join(court_cards)
            + " 不参与数字升降，代表「人物/态度/角色」插入过程，可能打断或改写数字轨迹。"
        )

    return "\n".join(lines)


def generate_core_insight(question, cards_detail, element_analysis, tension, trajectory, cards, core_card):
    """基于体系化数据推导四条结构化判断"""
    orientation_zh = "正位" if core_card["orientation"] == "upright" else "逆位"
    cards_overview = "；".join(
        f"{item['card']}({'正' if item['orientation'] == 'upright' else '逆'})"
        for item in cards
    )

    system_prompt = """你是塔罗体系分析引擎，只做基于给定数据的逻辑推理。
禁止情感表达、诗意渲染、安慰性话术或空泛象征。
输出必须严格包含以下四项，每项单独一行，格式固定：
①中心动力：
②关键转折点：
③事件因果链：
④最需要把握的一件事："""

    user_prompt = f"""用户问题：{question}

牌阵概览：{cards_overview}

牌面详情：
{cards_detail}

元素分布：{element_analysis['distribution']}
主导元素：{element_analysis['dominant_element']}（{element_analysis['domain']}）
元素关注：{element_analysis['focus']}

【元素张力】
{tension}

【灵数轨迹】
{trajectory}

核心牌：{core_card['card']}（{orientation_zh}）

请仅依据以上数据推导四项结构化判断，每项必须指向具体问题情境，不得使用「能量流动」「内在笃定」等空转词汇。"""

    try:
        client = get_text_client()
        response = client.chat.completions.create(
            model=TEXT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        return f"⚠️ 核心判断生成失败：{exc}"


def build_analysis_report(cards, core_card, question=None):
    """生成完整的体系化分析报告（喂给 AI 用）"""
    element_analysis = analyze_elements(cards)
    numerology_analysis = analyze_numerology(cards)
    element_tension = analyze_element_tension(element_analysis["distribution"])
    numerology_trajectory = analyze_numerology_trajectory(numerology_analysis)

    # 每张牌的详细信息（按牌型显示）
    cards_detail_lines = []
    for card_info in cards:
        card = card_info["card"]
        info = FULL_DECK[card]
        orientation = "正位" if card_info["orientation"] == "upright" else "逆位"

        if info.get("is_court"):
            cards_detail_lines.append(
                f"- {card}（{orientation}）：花色={info.get('minor_suit', '?')}（{info.get('element', '?')}），"
                f"角色={info.get('court_role', '?')}（{info.get('court_element', '?')}）"
            )
        elif info.get("suit") == "minor":
            cards_detail_lines.append(
                f"- {card}（{orientation}）：花色={info.get('minor_suit', '?')}（{info.get('element', '?')}），"
                f"编号={info.get('number', '?')}"
            )
        else:
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
    orientation_zh = "正位" if core_card["orientation"] == "upright" else "逆位"

    if core_info.get("is_court"):
        report += f"""

【核心牌深度信息】
- 牌名：{core_card['card']}
- 类型：宫廷牌（{core_info.get('court_role', '?')}）
- 花色：{core_info.get('minor_suit', '?')}（{core_info.get('element', '?')} 元素）
- 角色元素：{core_info.get('court_element', '?')}
- 正/逆位：{orientation_zh}"""
    elif core_info.get("suit") == "minor":
        report += f"""

【核心牌深度信息】
- 牌名：{core_card['card']}
- 类型：小阿卡纳数字牌
- 花色：{core_info.get('minor_suit', '?')}（{core_info.get('element', '?')} 元素）
- 编号：{core_number} → 归元为 {core_reduced}
- 正/逆位：{orientation_zh}"""
    else:
        report += f"""

【核心牌深度信息】
- 牌名：{core_card['card']}
- 类型：大阿卡纳
- 元素：{core_info.get('element', '未知')}
- 占星对应：{core_info.get('planet', '未知')}
- 编号：{core_number} → 归元为 {core_reduced}
- 正/逆位：{orientation_zh}"""

    report += f"""

【元素张力】
{element_tension}

【灵数轨迹】
{numerology_trajectory}"""

    if question:
        core_insight = generate_core_insight(
            question=question,
            cards_detail=cards_detail,
            element_analysis=element_analysis,
            tension=element_tension,
            trajectory=numerology_trajectory,
            cards=cards,
            core_card=core_card,
        )
        report += f"""

【体系化核心判断】
{core_insight}"""

    return report


if __name__ == "__main__":
    from tarot.drawer import draw_cards, find_core_card

    cards = draw_cards(3)
    core = find_core_card(cards)
    report = build_analysis_report(cards, core, question="测试问题")
    print(report)
