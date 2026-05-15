import json

# 塔罗体系核心知识（结构化数据）
tarot_system = {
    "version": "1.0",
    "description": "塔罗牌体系核心知识库：元素、灵数、宫廷牌、解牌公式",
    
    # === 一、四元素体系 ===
    "elements": {
        "火": {
            "name_en": "Fire",
            "keywords": ["激情", "意志力", "行动力", "热情"],
            "focus": "想不想做",
            "suit": "权杖 Wands",
            "domain": "事业、行动、热情"
        },
        "水": {
            "name_en": "Water",
            "keywords": ["情感", "人际关系", "直觉", "感受"],
            "focus": "感觉好不好",
            "suit": "圣杯 Cups",
            "domain": "感情、情绪、心理"
        },
        "风": {
            "name_en": "Air",
            "keywords": ["理智", "思想", "冲突", "判断"],
            "focus": "想得对不对",
            "suit": "宝剑 Swords",
            "domain": "理智、冲突、压力"
        },
        "土": {
            "name_en": "Earth",
            "keywords": ["物质", "金钱", "身体健康", "现实"],
            "focus": "能不能落地",
            "suit": "星币 Pentacles",
            "domain": "物质、财运、身体"
        }
    },
    
    # === 二、灵数体系（1-10）===
    "numerology_basic": {
        "1": {"meaning": "潜能、新开始、种子", "stage": "启动"},
        "2": {"meaning": "平衡、合作、选择", "stage": "二元"},
        "3": {"meaning": "创造、团队、初步成果", "stage": "产出"},
        "4": {"meaning": "稳定、停滞、基础", "stage": "结构"},
        "5": {"meaning": "挑战、冲突、改变", "stage": "动荡"},
        "6": {"meaning": "调和、分享、过渡", "stage": "秩序"},
        "7": {"meaning": "内省、评价、评估", "stage": "突围"},
        "8": {"meaning": "管理、专注、移动", "stage": "沉淀"},
        "9": {"meaning": "成熟、接近完美、总结", "stage": "巅峰"},
        "10": {"meaning": "完成、圆满、新循环开始", "stage": "终结"}
    },
    
    # === 三、灵数归元体系（1-9）===
"numerology_deep": {
    "concept": "塔罗牌中的数字都遵循 1-9 的循环，大于 9 的数字需要'归元'到 1-9",
    "reduction_rule": {
        "method": "个位 + 十位相加",
        "iteration": "若结果仍大于 9，继续相加直到 1-9"
    },
    "examples": [
        {"card": "15 恶魔", "number": 15, "calculation": "1 + 5 = 6", "reduced": 6},
        {"card": "19 太阳", "number": 19, "calculation": "1 + 9 = 10 → 1 + 0 = 1", "reduced": 1},
        {"card": "22 愚者（某些体系）", "number": 22, "calculation": "2 + 2 = 4", "reduced": 4}
    ],
    "meanings": {
        "1": "源头、启动、新阶段",
        "2": "二元、流动、寻求平衡",
        "3": "结合、产出、初步成果",
        "4": "结构、固化、建立秩序",
        "5": "动荡、冲突、打破平衡",
        "6": "秩序、回归、承担责任",
        "7": "突围、博弈、主动出击",
        "8": "沉淀、成长、由量变到质变",
        "9": "巅峰、孤独、完成使命"
    }
},
    # === 四、宫廷牌体系 ===
    "court_cards": {
        "侍从 Page": {
            "element": "风",
            "stage": "探索期",
            "keywords": ["好奇", "学习", "收集信息"]
        },
        "骑士 Knight": {
            "element": "火",
            "stage": "推进期",
            "keywords": ["行动", "执行", "快速推进"]
        },
        "王后 Queen": {
            "element": "水",
            "stage": "守护期",
            "keywords": ["滋养", "情感", "守护资源"]
        },
        "国王 King": {
            "element": "土",
            "stage": "建构期",
            "keywords": ["稳定", "权威", "构建现实"]
        }
    },
    
    # === 五、解牌公式 ===
    "interpretation_formula": {
        "core": "元素 + 灵数 = 核心能量",
        "explanation": {
            "element": "决定问题聚焦的领域和行动方式",
            "number": "决定能量的阶段和发展状态"
        },
        "examples": [
            {"card": "权杖三", "formula": "火+3", "meaning": "充满活力的团队合作，向外拓展"},
            {"card": "圣杯五", "formula": "水+5", "meaning": "情绪上的丧失或挑战"},
            {"card": "宝剑十", "formula": "风+10", "meaning": "理智上的彻底终结"},
            {"card": "星币八", "formula": "土+8", "meaning": "勤奋的积累财富和技能"}
        ]
    },
    
    # === 六、宫廷牌交叉公式 ===
    "court_combination_examples": [
        {"card": "宝剑侍从", "formula": "风+风", "meaning": "思维信息的探索者"},
        {"card": "宝剑骑士", "formula": "风+火", "meaning": "思维目标的推进者"},
        {"card": "宝剑王后", "formula": "风+水", "meaning": "思维资源的守护者"},
        {"card": "宝剑国王", "formula": "风+土", "meaning": "思维成果的建构者"}
    ]
}

# 写入 JSON 文件
with open("knowledge_base/structured/tarot_system.json", "w", encoding="utf-8") as f:
    json.dump(tarot_system, f, ensure_ascii=False, indent=2)

print("✅ 塔罗体系结构化数据导出成功")
print("📁 保存位置：knowledge_base/structured/tarot_system.json")
print(f"📊 共包含 {len(tarot_system) - 2} 个核心模块")