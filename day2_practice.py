def greet(name):
    return f"你好，{name}！"

# 调用函数
message = greet("Rika")
print(message)

# 多次调用
print(greet("塔罗师"))
print(greet("小红"))

import random

def draw_card(deck):
    """从牌组里抽一张牌"""
    return random.choice(deck)

# 测试
my_deck = ["The Fool", "The Magician", "The Star"]
card = draw_card(my_deck)
print(f"抽到的牌：{card}")

def draw_cards(deck, count=1):
    """从牌组里抽 N 张不重复的牌，默认抽 1 张"""
    return random.sample(deck, count)

# 测试三种调用方式
print(draw_cards(my_deck))           # 抽 1 张
print(draw_cards(my_deck, 2))        # 抽 2 张
print(draw_cards(my_deck, count=3))  # 抽 3 张（具名参数）
# 字典的常用操作
tarot_card = {
    "name": "The Fool",
    "name_zh": "愚人",
    "number": 0,
    "keywords": ["新开始", "纯真", "冒险"],
    "upright": "新的开始、纯真、自由",
    "reversed": "鲁莽、轻率"
}

# 1. 获取值
print(tarot_card["name"])              # 直接取
print(tarot_card.get("name"))          # 用 .get()（更安全）
print(tarot_card.get("不存在的key"))    # 返回 None，不报错
print(tarot_card.get("不存在", "默认值")) # 返回默认值

# 2. 添加/修改
tarot_card["element"] = "风"           # 添加新字段
tarot_card["number"] = 1               # 修改字段

# 3. 遍历字典
for key, value in tarot_card.items():
    print(f"{key}: {value}")

# 4. 检查 key 是否存在
if "name" in tarot_card:
    print("有 name 字段")

    # === 练习 5：错误处理 ===
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "❌ 不能除以 0"
    except Exception as e:
        return f"❌ 出错了：{e}"

print(safe_divide(10, 2))
print(safe_divide(10, 0))
print(safe_divide(10, "a"))

# === 练习 6：模拟 API 调用失败 ===
def fake_api_call(should_fail=False):
    try:
        if should_fail:
            raise Exception("网络超时")
        return "✅ API 返回成功"
    except Exception as e:
        return f"⚠️ API 调用失败：{e}\n请检查网络和 key"

print(fake_api_call())
print(fake_api_call(should_fail=True))