"""塔罗数据加载模块"""
import json


def load_major_arcana():
    """从 JSON 文件加载 22 张大阿卡纳牌数据"""
    with open("knowledge_base/structured/major_arcana.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    arcana_dict = {}
    for card in data["cards"]:
        arcana_dict[card["key"]] = {
            "upright": card["upright"],
            "reversed": card["reversed"],
            "number": card["number"],
            "name_zh": card["name_zh"],
            "element": card.get("element", "未知"),
            "planet": card.get("planet", "未知")
        }
    return arcana_dict


def load_tarot_system():
    """加载塔罗体系知识（元素、灵数、解牌公式等）"""
    with open("knowledge_base/structured/tarot_system.json", "r", encoding="utf-8") as f:
        return json.load(f)


# 调试用：直接运行这个文件可以验证加载是否成功
if __name__ == "__main__":
    arcana = load_major_arcana()
    print(f"✅ 加载了 {len(arcana)} 张大阿卡纳牌")
    print(f"   示例 - 愚人：{arcana['The Fool 愚人']}")

    system = load_tarot_system()
    print(f"✅ 加载了塔罗体系，包含 {len(system) - 2} 个模块")
    # 模块级缓存，避免重复加载
_TAROT_SYSTEM = None


def get_tarot_system():
    """单例方式获取塔罗体系，避免重复读 JSON"""
    global _TAROT_SYSTEM
    if _TAROT_SYSTEM is None:
        _TAROT_SYSTEM = load_tarot_system()
    return _TAROT_SYSTEM


def reduce_number(n):
    """灵数归元：把任意数字降到 1-9"""
    if n == 0:
        return 0  # 愚者特殊处理
    while n > 9:
        n = sum(int(digit) for digit in str(n))
    return n