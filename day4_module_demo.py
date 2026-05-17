"""day4 模块练习 - 提供塔罗工具函数"""
import random


def shuffle_cards(deck):
    """洗牌函数"""
    shuffled = deck.copy()
    random.shuffle(shuffled)
    return shuffled


def pick_one(deck):
    """随机选一张"""
    return random.choice(deck)


# 让别人 import 这个模块时，下面的代码不会自动执行
if __name__ == "__main__":
    test_deck = ["A", "B", "C", "D"]
    print(shuffle_cards(test_deck))
    print(pick_one(test_deck))