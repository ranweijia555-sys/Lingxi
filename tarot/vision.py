"""塔罗牌拍照识别模块（GPT-4o Vision）"""
import base64
import json
from tarot.llm_client import get_vision_client, VISION_MODEL
from tarot.data_loader import load_full_deck


# 加载完整牌组，用于校验识别结果
FULL_DECK = load_full_deck()


def _encode_image(image_bytes):
    """把图片字节转成 base64"""
    return base64.b64encode(image_bytes).decode("utf-8")


def _build_card_list_hint():
    """生成所有合法牌名的提示，帮助 GPT 输出标准牌名"""
    names = list(FULL_DECK.keys())
    return "、".join(names)


def recognize_cards(image_bytes, expected_count=None):
    """
    识别图中的塔罗牌
    
    参数：
      image_bytes: 图片的二进制内容
      expected_count: 期望识别的牌数（来自用户选的牌阵），None 表示自动判断
    
    返回：
      {
        "success": True/False,
        "cards": [{"card": "...", "orientation": "upright/reversed", "confidence": 0.9}, ...],
        "raw": "GPT 原始回复",
        "error": "错误信息（如果失败）"
      }
    """
    client = get_vision_client()
    base64_image = _encode_image(image_bytes)
    
    count_hint = ""
    if expected_count:
        count_hint = f"图中应该有 {expected_count} 张牌，请识别出全部 {expected_count} 张。"
    
    prompt = f"""你是一位塔罗牌识别专家。请识别这张图片中的塔罗牌。

{count_hint}

要求：
1. 按从左到右、从上到下的顺序识别每一张牌
2. 判断每张牌是正位（upright）还是逆位（reversed）—— 注意牌面图案是否上下颠倒
3. 牌名必须从以下标准牌名中选择最匹配的一个：
{_build_card_list_hint()}

4. 给出识别置信度 confidence（0-1 之间的小数）

只返回 JSON，不要任何其他文字，格式如下：
{{
  "cards": [
    {{"card": "标准牌名", "orientation": "upright", "confidence": 0.95}},
    {{"card": "标准牌名", "orientation": "reversed", "confidence": 0.88}}
  ]
}}"""

    try:
        response = client.chat.completions.create(
            model=VISION_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )
        
        raw = response.choices[0].message.content
        
        # 解析 JSON（GPT 有时会用 ```json 包裹，要清理）
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:]
        cleaned = cleaned.strip()
        
        parsed = json.loads(cleaned)
        cards = parsed.get("cards", [])
        
        # 校验每张牌名是否在合法牌组里
        validated = []
        for c in cards:
            card_name = c.get("card", "")
            # 精确匹配
            if card_name in FULL_DECK:
                validated.append({
                    "card": card_name,
                    "orientation": c.get("orientation", "upright"),
                    "confidence": c.get("confidence", 0.5),
                    "valid": True
                })
            else:
                # 模糊匹配：找名字包含关系的
                match = None
                for key in FULL_DECK:
                    if card_name in key or key in card_name:
                        match = key
                        break
                validated.append({
                    "card": match if match else card_name,
                    "orientation": c.get("orientation", "upright"),
                    "confidence": c.get("confidence", 0.5) if match else 0.3,
                    "valid": match is not None
                })
        
        return {
            "success": True,
            "cards": validated,
            "raw": raw,
            "error": None
        }
        
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "cards": [],
            "raw": raw if 'raw' in dir() else "",
            "error": f"无法解析识别结果：{e}"
        }
    except Exception as e:
        return {
            "success": False,
            "cards": [],
            "raw": "",
            "error": f"识别失败：{e}"
        }


if __name__ == "__main__":
    # 测试：读取一张本地图片识别
    import sys
    if len(sys.argv) < 2:
        print("用法：python3 -m tarot.vision <图片路径>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    
    print("🔍 正在识别...")
    result = recognize_cards(image_bytes)
    
    if result["success"]:
        print(f"✅ 识别到 {len(result['cards'])} 张牌：")
        for c in result["cards"]:
            orientation_zh = "正位" if c["orientation"] == "upright" else "逆位"
            valid_mark = "✓" if c["valid"] else "⚠️ 牌名存疑"
            print(f"  {valid_mark} {c['card']} ({orientation_zh}) - 置信度 {c['confidence']}")
    else:
        print(f"❌ {result['error']}")