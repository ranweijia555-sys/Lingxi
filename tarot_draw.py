"""灵犀塔罗 - 主程序入口（含历史记录）"""
from tarot.drawer import draw_cards, format_cards, find_core_card
from tarot.analyzer import build_analysis_report
from tarot.interpreter import interpret_single_card, synthesize_reading
from tarot.data_loader import load_spreads, load_full_deck 
from tarot.history import save_reading, show_history_summary


def choose_mode():
    """让用户选择主菜单"""
    print("✦ 欢迎来到灵案 AstRa")
    print()
    print("请选择：")
    print("  1. 开始新的占卜")
    print("  2. 查看历史记录")
    print()
    
    choice = input("> 请输入序号 (1-2): ").strip()
    return choice


def choose_spread():
    """让用户选择牌阵"""
    spreads = load_spreads()
    spread_keys = list(spreads.keys())
    
    print("📜 请选择牌阵：")
    for i, key in enumerate(spread_keys, start=1):
        spread = spreads[key]
        print(f"  {i}. {spread['name']}（{spread['card_count']} 张）- {spread['description']}")
    print()
    
    choice = input("> 请输入序号 (1-{}): ".format(len(spread_keys)))
    try:
        idx = int(choice) - 1
        return spread_keys[idx], spreads[spread_keys[idx]]
    except (ValueError, IndexError):
        print("⚠️ 输入无效，默认使用三张无牌阵")
        return "three_no_spread", spreads["three_no_spread"]


def do_reading():
    """执行一次占卜"""
    # 1. 选牌阵
    spread_key, spread = choose_spread()
    print(f"✅ 你选择了：{spread['name']}")
    print()

    # 2. 输入问题
    question = input("🌙 你想问什么问题？\n> ")
    print()

    # 3. 抽牌
    cards = draw_cards(spread["card_count"])
    positions = spread["positions"]

    # 4. 显示抽到的牌
    print("🔮 本次抽到的牌：")
    print()
    cards_text = format_cards(cards, positions)
    print(cards_text)
    print()

    # 5. 找核心牌
    core_card = find_core_card(cards, logic=spread["logic"])
    
    # 6. 准备数据
    arcana = load_full_deck()
    
    # 7. 逐张深度解读
    print("=" * 50)
    print("🃏 逐张深度解读")
    print()
    
    cards_with_interpretations = []
    for position, card_info in zip(positions, cards):
        is_core = (card_info["card"] == core_card["card"])
        card_detail = arcana[card_info["card"]]
        
        print(f"📖 {position}：{card_info['card']}" + ("（核心牌 ⭐）" if is_core else ""))
        print("-" * 40)
        interpretation = interpret_single_card(
            question, card_info, position, card_detail, is_core
        )
        print(interpretation)
        print()
        
        cards_with_interpretations.append({
            "position": position,
            "card": card_info["card"],
            "interpretation": interpretation
        })
    
    # 8. 体系化分析
    analysis_report = build_analysis_report(cards, core_card)
    
    # 9. 综合指引
    print("=" * 50)
    print("✨ 整体能量与核心指引")
    print()
    summary = synthesize_reading(question, cards_with_interpretations, analysis_report)
    print(summary)
    print()
    
    # 10. 保存到历史
    reading_id = save_reading(
        question=question,
        spread_name=spread["name"],
        cards=cards,
        core_card=core_card,
        single_interpretations=cards_with_interpretations,
        summary=summary
    )
    print("=" * 50)
    print(f"📝 已保存为占卜 #{reading_id}")
    print()


def main():
    """主流程"""
    mode = choose_mode()
    print()
    
    if mode == "1":
        do_reading()
    elif mode == "2":
        show_history_summary(limit=5)
    else:
        print("⚠️ 输入无效，再见 👋")


if __name__ == "__main__":
    main()