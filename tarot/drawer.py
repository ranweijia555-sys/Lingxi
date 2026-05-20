"""塔罗抽牌模块"""
import random
from tarot.data_loader import load_major_arcana


# 模块加载时把数据准备好
MAJOR_ARCANA = load_major_arcana()


def draw_cards(count=3):
    """随机抽 N 张塔罗牌"""
    card_names = list(MAJOR_ARCANA.keys())
    selected = random.sample(card_names, count)
    result = []
    for card_name in selected:
        result.append({
            "card": card_name,
            "orientation": random.choice(["upright", "reversed"])
        })
    return result


def format_cards(cards, positions):
    """把抽到的牌格式化成易读文字"""
    lines = []
    for position, card_info in zip(positions, cards):
        card = card_info["card"]
        orientation = card_info["orientation"]
        orientation_zh = "正位" if orientation == "upright" else "逆位"
        meaning = MAJOR_ARCANA[card][orientation]
        lines.append(f"{position}: {card} ({orientation_zh})\n      含义：{meaning}")
    return "\n".join(lines)


def find_core_card(cards, logic="no_spread"):
    """
    根据牌阵逻辑找出核心牌
    
    - single: 只有一张，就是它
    - no_spread: 编号最小的为核心
    - timeline: "现在"位置（中间）的为核心
    """
    if len(cards) == 1:
        return cards[0]
    
    if logic == "timeline":
        # 时间线牌阵：中间的牌（现在）是核心
        return cards[len(cards) // 2]
    
    # 默认无牌阵逻辑：编号最小为核心
    arcana_order = list(MAJOR_ARCANA.keys())
    core = min(cards, key=lambda c: arcana_order.index(c["card"]))
    return core