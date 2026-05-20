"""塔罗占卜历史记录模块"""
import json
import os
from datetime import datetime


HISTORY_FILE = "data/history/readings.json"


def _ensure_history_file():
    """确保历史文件存在"""
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump({"readings": []}, f, ensure_ascii=False, indent=2)


def save_reading(question, spread_name, cards, core_card, single_interpretations, summary):
    """
    保存一次占卜记录
    
    cards: draw_cards 返回的列表
    single_interpretations: [{"position", "card", "interpretation"}, ...]
    summary: 整体指引文字
    """
    _ensure_history_file()
    
    # 读旧记录
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 构造新记录
    new_reading = {
        "id": len(data["readings"]) + 1,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "question": question,
        "spread": spread_name,
        "cards": [
            {
                "card": c["card"],
                "orientation": c["orientation"]
            }
            for c in cards
        ],
        "core_card": core_card["card"],
        "single_interpretations": single_interpretations,
        "summary": summary
    }
    
    # 追加 + 写回
    data["readings"].append(new_reading)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return new_reading["id"]


def load_history():
    """加载所有历史记录"""
    _ensure_history_file()
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["readings"]


def show_history_summary(limit=5):
    """打印历史摘要（最近 N 条）"""
    history = load_history()
    if not history:
        print("📭 还没有历史记录哦")
        return
    
    recent = history[-limit:][::-1]  # 最近 N 条，倒序
    print(f"📚 最近 {len(recent)} 次占卜：")
    print()
    for r in recent:
        cards_str = "、".join([c["card"].split(" ")[-1] for c in r["cards"]])
        print(f"  #{r['id']}  {r['timestamp']}")
        print(f"     问题：{r['question']}")
        print(f"     牌阵：{r['spread']}  |  抽到：{cards_str}")
        print(f"     核心牌：{r['core_card'].split(' ')[-1]}")
        print()


if __name__ == "__main__":
    show_history_summary()