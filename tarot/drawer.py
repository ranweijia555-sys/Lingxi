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


def find_core_card(cards):
    """无牌阵逻辑：编号最小的大卡为核心牌"""
    arcana_order = list(MAJOR_ARCANA.keys())
    core = min(cards, key=lambda c: arcana_order.index(c["card"]))
    return core


if __name__ == "__main__":
    cards = draw_cards(3)
    print(format_cards(cards, ["牌一", "牌二", "牌三"]))
    print(f"\n核心牌：{find_core_card(cards)['card']}")