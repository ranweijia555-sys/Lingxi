# === 练习 1：写入 txt 文件 ===
with open("test.txt", "w", encoding="utf-8") as f:
    f.write("欢迎来到灵犀塔罗\n")
    f.write("这是第二行\n")

print("✅ 写入成功！")

# === 练习 2：读取 txt 文件 ===
with open("test.txt", "r", encoding="utf-8") as f:
    content = f.read()

print("📄 文件内容：")
print(content)

# === 练习 3：逐行读取 ===
print("📄 逐行打印：")
with open("test.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(f"   → {line.strip()}")

import json

# === 练习 4：把字典写成 JSON 文件 ===
card_data = {
    "name": "The Fool",
    "name_zh": "愚人",
    "number": 0,
    "upright": "新的开始、纯真、自由、冒险",
    "reversed": "鲁莽、轻率、被欺骗",
    "keywords": ["新开始", "纯真", "冒险"],
    "element": "风"
}

with open("test_card.json", "w", encoding="utf-8") as f:
    json.dump(card_data, f, ensure_ascii=False, indent=2)

print("✅ JSON 写入成功！打开 test_card.json 看看")

# === 练习 5：读取 JSON 文件 ===
with open("test_card.json", "r", encoding="utf-8") as f:
    loaded_card = json.load(f)

print(f"🃏 牌名：{loaded_card['name_zh']}")
print(f"📖 含义：{loaded_card['upright']}")
print(f"🏷️  关键词：{loaded_card['keywords']}")

# === 练习 6：字典 ↔ JSON 字符串互转 ===
# 字典 → 字符串（用于 API 传输）
json_string = json.dumps(card_data, ensure_ascii=False)
print(f"\n📝 转成字符串：{json_string[:50]}...")
print(f"   类型：{type(json_string)}")

# 字符串 → 字典
parsed = json.loads(json_string)
print(f"\n📦 转回字典，name 字段：{parsed['name']}")
print(f"   类型：{type(parsed)}")      