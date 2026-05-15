import os
import json   
import random
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# === 数据 ===
# === 从 JSON 加载塔罗数据 ===
def load_tarot_data():
    """从 JSON 文件加载塔罗牌数据"""
    with open("knowledge_base/structured/major_arcana.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # 转回字典格式（key 是牌名，方便代码查询）
    arcana_dict = {}
    for card in data["cards"]:
        arcana_dict[card["key"]] = {
            "upright": card["upright"],
            "reversed": card["reversed"],
            "number": card["number"],
            "name_zh": card["name_zh"]
        }
    return arcana_dict

# 程序启动时加载一次
MAJOR_ARCANA = load_tarot_data()


# === 函数 ===
def draw_tarot_cards(count=3):
    """随机抽 N 张塔罗牌，返回牌名和正逆位"""
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

def get_ai_interpretation(question, cards_text, core_card):
    """调 DeepSeek 生成塔罗解读"""
    prompt = f"""你是一位温柔且富有洞察力的塔罗师。

用户的问题：{question}

抽到的三张牌：
{cards_text}

核心牌（最重要）：{core_card["card"]}

请使用无牌阵解读逻辑：
1. 先重点解读核心牌的含义与对问题的指引
2. 再结合其余两张辅助牌补充信息
3. 最后给出一句核心建议
你要作为一个专业的塔罗大师，给出具体的牌面分析，语气稍微温柔，给出适当建议，避免过于绝对的预测，用中文回答，控制在 350 字以内。"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一位经验丰富的塔罗解读师，温柔而富有智慧。"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ AI 解读失败：{e}\n请检查网络和 API key。"


def main():
    """主流程"""
    print("🔮 欢迎来到灵犀塔罗")
    print()

    question = input("🌙 你想问什么问题？\n> ")
    print()

    cards = draw_tarot_cards(3)
    positions = ["牌一", "牌二", "牌三"]

    print("🔮 本次抽到的三张牌：")
    print()
    cards_text = format_cards(cards, positions)
    print(cards_text)
    print()

    print("=" * 40)
    print("🤖 AI 塔罗师正在解读中...")
    print()
    core_card = find_core_card(cards)
    interpretation = get_ai_interpretation(question, cards_text, core_card)
    print(interpretation)
    print()


if __name__ == "__main__":
    main()