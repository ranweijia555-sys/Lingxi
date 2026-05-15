def reduce_number(n):
    """灵数归元：把任意数字降到 1-9"""
    while n > 9:
        n = sum(int(digit) for digit in str(n))
    return n


# 测试
test_cards = [
    (15, "恶魔"),
    (19, "太阳"),
    (22, "愚者"),
    (10, "命运之轮"),
    (78, "如果有78号牌")
]

for num, name in test_cards:
    reduced = reduce_number(num)
    print(f"{num} 号牌「{name}」→ 归元为 {reduced}")