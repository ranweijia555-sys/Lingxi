"""灵犀塔罗 - 主程序入口（升级版：融合元素+灵数体系）"""
from tarot.drawer import draw_cards, format_cards, find_core_card
from tarot.analyzer import build_analysis_report
from tarot.interpreter import get_interpretation


def main():
    """主流程"""
    print("🔮 欢迎来到灵犀塔罗")
    print()

    question = input("🌙 你想问什么问题？\n> ")
    print()

    # 1. 抽牌
    cards = draw_cards(3)
    positions = ["牌一", "牌二", "牌三"]

    # 2. 显示抽到的牌
    print("🔮 本次抽到的三张牌：")
    print()
    cards_text = format_cards(cards, positions)
    print(cards_text)
    print()

    # 3. 找出核心牌
    core_card = find_core_card(cards)

    # 4. 生成体系化分析报告（新增！）
    print("=" * 50)
    print("📊 体系化分析")
    print()
    analysis_report = build_analysis_report(cards, core_card)
    print(analysis_report)
    print()

    # 5. AI 综合解读
    print("=" * 50)
    print("🤖 AI 塔罗师正在深度解读中...")
    print()
    interpretation = get_interpretation(question, cards_text, core_card, analysis_report)
    print(interpretation)
    print()


if __name__ == "__main__":
    main()
    