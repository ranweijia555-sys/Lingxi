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
            "planet": card.get("planet", "未知"),
            "suit": "major"  # 标记花色类型
        }
    return arcana_dict


def load_minor_arcana():
    """从 JSON 文件加载 56 张小阿卡纳牌数据"""
    with open("knowledge_base/structured/minor_arcana.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    arcana_dict = {}
    for card in data["cards"]:
        arcana_dict[card["key"]] = {
            "upright": card["upright"],
            "reversed": card["reversed"],
            "number": card.get("number"),  # 宫廷牌为 None
            "name_zh": card["name_zh"],
            "element": card.get("element", "未知"),
            "minor_suit": card.get("minor_suit"),
            "is_court": card.get("is_court", False),
            "court_role": card.get("court_role"),
            "court_element": card.get("court_element"),
            "domain": card.get("domain"),
            "suit": "minor"
        }
    return arcana_dict


def load_full_deck():
    """加载完整 78 张塔罗牌（大+小）"""
    major = load_major_arcana()
    minor = load_minor_arcana()
    full = {**major, **minor}  # 字典合并
    return full


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

def load_spreads():
    """加载牌阵定义"""
    with open("knowledge_base/structured/spreads.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["spreads"]

def get_spread(spread_key):
    """根据 key 获取单个牌阵定义"""
    spreads = load_spreads()
    return spreads.get(spread_key)