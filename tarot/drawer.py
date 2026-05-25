"""塔罗抽牌模块（78 张完整版）"""
import random
from tarot.data_loader import load_full_deck


# 模块加载时把完整 78 张牌准备好
FULL_DECK = load_full_deck()


def draw_cards(count=3):
    """从 78 张牌里随机抽 N 张"""
    card_names = list(FULL_DECK.keys())
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
        meaning = FULL_DECK[card][orientation]
        lines.append(f"{position}: {card} ({orientation_zh})\n      含义：{meaning}")
    return "\n".join(lines)


def find_core_card(cards, logic="no_spread"):
    """
    完整核心牌规则（升级版）
    
    无牌阵逻辑（no_spread）：
    - 0 张大卡：取中间位置的牌
    - 1 张大卡：那张大卡就是核心
    - 2 张大卡：取编号靠前（小）者
    - 3 张大卡：取中间编号者
    
    时间线逻辑（timeline）：固定取中间位置（现在）
    单张逻辑（single）：就是那一张
    """
    if len(cards) == 1:
        return cards[0]
    
    if logic == "timeline":
        return cards[len(cards) // 2]
    
    # === no_spread 完整规则 ===
    # 找出大卡
    majors = [c for c in cards if FULL_DECK[c["card"]]["suit"] == "major"]
    major_count = len(majors)
    
    if major_count == 0:
        # 全小卡：取中间位置
        return cards[len(cards) // 2]
    
    if major_count == 1:
        # 1 张大卡：那张就是核心
        return majors[0]
    
    if major_count == 2:
        # 2 张大卡：取编号靠前者
        return min(majors, key=lambda c: FULL_DECK[c["card"]]["number"])
    
    if major_count == 3:
        # 3 张大卡：取中间编号者
        sorted_by_num = sorted(majors, key=lambda c: FULL_DECK[c["card"]]["number"])
        return sorted_by_num[1]  # 中间那个
    
    # 兜底（4+ 张大卡，未来扩展时用）
    return min(majors, key=lambda c: FULL_DECK[c["card"]]["number"])


if __name__ == "__main__":
    # 跑几次测试一下
    for i in range(3):
        print(f"\n--- 第 {i+1} 次测试 ---")
        cards = draw_cards(3)
        for c in cards:
            suit_label = "大" if FULL_DECK[c["card"]]["suit"] == "major" else "小"
            print(f"  [{suit_label}] {c['card']} ({c['orientation']})")
        core = find_core_card(cards)
        print(f"  → 核心牌：{core['card']}")
        