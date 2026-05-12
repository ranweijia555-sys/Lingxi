import random

# 22张大阿卡纳牌（先用这些，后面再加56张小阿卡纳）
major_arcana = {

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
        "upright": "待补充",
        "reversed": "待补充"
    },
    "The Emperor 皇帝": {
        "upright": "待补充",
        "reversed": "待补充"
    },
    "The Hierophant 教皇": {
        "upright": "待补充",
        "reversed": "待补充"
    },
    "The Lovers 恋人": {
        "upright": "待补充",
        "reversed": "待补充"
    },
    "The Chariot 战车": {
        "upright": "待补充",
        "reversed": "待补充"
    },
    "Strength 力量": {
        "upright": "待补充",
        "reversed": "待补充"
    },
    "The Hermit 隐者": {
        "upright": "待补充",
        "reversed": "待补充"
    },
    "Wheel of Fortune 命运之轮": {
        "upright": "待补充",
        "reversed": "待补充"
    },
    "Justice 正义": {
        "upright": "待补充",
        "reversed": "待补充"
    },
    "The Hanged Man 倒吊人": {
        "upright": "待补充",
        "reversed": "待补充"
    },
    "Death 死神": {
        "upright": "待补充",
        "reversed": "待补充"
    },
    "Temperance 节制": {
        "upright": "待补充",
        "reversed": "待补充"
    },
    "The Devil 恶魔": {
        "upright": "待补充",
        "reversed": "待补充"
    },
    "The Tower 塔": {
        "upright": "待补充",
        "reversed": "待补充"
    },
    "The Star 星星": {
        "upright": "待补充",
        "reversed": "待补充"
    },
    "The Moon 月亮": {
        "upright": "待补充",
        "reversed": "待补充"
    },
    "The Sun 太阳": {
        "upright": "待补充",
        "reversed": "待补充"
    },
    "Judgement 审判": {
        "upright": "待补充",
        "reversed": "待补充"
    },
    "The World 世界": {
        "upright": "待补充",
        "reversed": "待补充"
    }
}
# 让用户输入问题
question = input("🌙 你想问什么问题？\n> ")

print()
print(f"📜 你的问题：{question}")
print()

# 抽三张
card_names = list(major_arcana.keys())
cards = random.sample(card_names, 3)
positions = ["过去", "现在", "未来"]

print("🔮 三张牌阵（过去 / 现在 / 未来）：")
print()

for position, card in zip(positions, cards):
    orientation = random.choice(["upright", "reversed"])
    meaning = major_arcana[card][orientation]
    
    orientation_zh = "正位" if orientation == "upright" else "逆位"
    
    print(f"   {position}: {card} ({orientation_zh})")
    print(f"      含义：{meaning}")
    print()