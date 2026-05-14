import os
import random
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# === 数据 ===
MAJOR_ARCANA = {
    "The Fool 愚人": {
        "upright": "新的开始、纯真、自由、冒险",
        "reversed": "鲁莽、轻率、被欺骗"
    },
    "The Magician 魔术师": {
        "upright": "意志力、创造、行动、技能",
        "reversed": "操纵、缺乏自信、未发挥潜能"
    },
    "The High Priestess 女祭司": {
        "upright": "直觉、潜意识、神秘、内在智慧",
        "reversed": "压抑、忽视直觉、表面化"
    },
    "The Empress 女皇": {
        "upright": "丰盛、母性、创造力、自然",
        "reversed": "依赖、创意阻塞、忽视自我"
    },
    "The Emperor 皇帝": {
        "upright": "权威、稳定、领导力、纪律",
        "reversed": "专制、缺乏灵活、控制欲强"
    },
    "The Hierophant 教皇": {
        "upright": "传统、信仰、教育、遵循规则",
        "reversed": "挑战传统、个人信念、叛逆"
    },
    "The Lovers 恋人": {
        "upright": "爱、和谐、选择、价值观一致",
        "reversed": "失衡、价值观冲突、错误选择"
    },
    "The Chariot 战车": {
        "upright": "意志力、胜利、控制、决心",
        "reversed": "失控、方向不明、攻击性"
    },
    "Strength 力量": {
        "upright": "内在力量、勇气、耐心、同情",
        "reversed": "自我怀疑、软弱、缺乏自信"
    },
    "The Hermit 隐者": {
        "upright": "内省、独处、寻找真相、智慧",
        "reversed": "孤立、逃避、拒绝帮助"
    },
    "Wheel of Fortune 命运之轮": {
        "upright": "命运、转机、循环、好运",
        "reversed": "厄运、阻力、打破循环"
    },
    "Justice 正义": {
        "upright": "公正、真相、因果、诚实",
        "reversed": "不公平、逃避责任、不诚实"
    },
    "The Hanged Man 倒吊人": {
        "upright": "暂停、放手、新视角、等待",
        "reversed": "拖延、抵抗、无谓牺牲"
    },
    "Death 死神": {
        "upright": "转变、结束与开始、蜕变",
        "reversed": "抗拒改变、停滞、无法前进"
    },
    "Temperance 节制": {
        "upright": "平衡、耐心、适度、融合",
        "reversed": "失衡、过度、缺乏长远眼光"
    },
    "The Devil 恶魔": {
        "upright": "束缚、物质主义、上瘾、阴暗面",
        "reversed": "解放、挣脱束缚、重获自由"
    },
    "The Tower 塔": {
        "upright": "突变、混乱、启示、打破幻象",
        "reversed": "避免灾难、延迟崩溃、恐惧改变"
    },
    "The Star 星星": {
        "upright": "希望、信念、更新、平静",
        "reversed": "绝望、失去信念、缺乏灵感"
    },
    "The Moon 月亮": {
        "upright": "幻觉、恐惧、潜意识、不确定",
        "reversed": "释放恐惧、真相揭露、清晰"
    },
    "The Sun 太阳": {
        "upright": "成功、喜悦、活力、积极",
        "reversed": "暂时受阻、过度乐观、延迟成功"
    },
    "Judgement 审判": {
        "upright": "觉醒、重生、内在呼唤、宽恕",
        "reversed": "自我怀疑、拒绝成长、内疚"
    },
    "The World 世界": {
        "upright": "完成、整合、成就、旅程终点",
        "reversed": "未完成、缺乏收尾、拖延"
    }
}


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