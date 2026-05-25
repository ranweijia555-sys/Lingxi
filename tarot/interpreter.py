# 全局负责任 AI 守则 - 所有 prompt 共用
RESPONSIBLE_AI_GUIDELINES = """
在解读时，请遵守以下负责任的边界：

1. 涉及体重、身材、饮食、运动等身体健康话题时：
   - 不做"能不能减到 X 公斤"这种绝对判断
   - 不给具体的卡路里、运动量、饮食限制数字
   - 强调身体的多元美与自我接纳，避免强化"瘦才好"的预设
   - 鼓励温和、可持续的生活方式，而非苛刻的目标
   - 如察觉问题背后有过度节食或身材焦虑倾向，温柔地提醒"可以与信任的人或专业人士聊聊"

2. 涉及医疗、用药、严重心理困扰时：
   - 不给医疗建议
   - 温柔地引导寻求专业帮助

3. 涉及重大决策（投资、婚姻、辞职、移民等）时：
   - 强调塔罗是反思工具，不是决策依据
   - 鼓励多角度思考和咨询相关专业人士

4. 任何时候：
   - 不预测灾难、死亡、严重负面事件
   - 保持温暖、有边界、不夸大

5. 语言风格要求：
   - 不要使用"亲爱的"、"宝贝"、"姐妹"等称呼语开头
   - 直接进入解读内容，自然如朋友间的对话
   - 多用第二人称"你"，少用"亲"、"小可爱"等亲昵词
   - 整体语气保持温柔、知性、有边界感，避免过度亲密
"""

"""塔罗 AI 解读模块（多步链式版：单卡深读 + 整体汇总）"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# 兼容本地 .env 和 Streamlit Cloud Secrets
def get_api_key():
    """优先用 Streamlit Secrets，本地 fallback 到 .env"""
    key = os.getenv("DEEPSEEK_API_KEY")
    if key:
        return key
    # Streamlit Cloud 场景
    try:
        import streamlit as st
        return st.secrets["DEEPSEEK_API_KEY"]
    except Exception:
        return None


client = OpenAI(
    api_key=get_api_key(),
    base_url="https://api.deepseek.com"
)

def _call_llm(system_prompt, user_prompt):
    """统一的 LLM 调用接口"""
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ AI 解读失败：{e}"


def interpret_single_card(question, card_info, position, card_detail, is_core):
    """
    解读单张牌
    
    card_info: {"card": "...", "orientation": "..."}
    position: "牌一" / "过去" / "今日指引" 等
    card_detail: 包含 element, planet, number, upright, reversed 等
    is_core: 是否为核心牌
    """
    orientation_zh = "正位" if card_info["orientation"] == "upright" else "逆位"
    meaning = card_detail["upright"] if card_info["orientation"] == "upright" else card_detail["reversed"]
    
    role_label = "（核心牌 ⭐）" if is_core else ""
    
    user_prompt = f"""用户的问题：{question}

需要解读的牌：
- 位置：{position} {role_label}
- 牌名：{card_info['card']}（{orientation_zh}）
- 元素：{card_detail.get('element', '?')}
- 占星对应：{card_detail.get('planet', '?')}
- 编号：{card_detail.get('number', '?')}
- 传统含义：{meaning}

请给出这张牌的解读，要求：
1. 控制在 100-150 字
2. 自然融入元素和占星信息（不要硬塞）
3. 紧扣用户问题，不要泛泛而谈
4. 语气亲和有洞察，不要称呼亲爱的
5. 不需要标题或编号，直接一段话
6. 用中文"""
    
    # 第一个（interpret_single_card 里）
    system_prompt = "你是一位温柔且专业的塔罗师，擅长用元素和占星视角解读单张牌。\n\n" + RESPONSIBLE_AI_GUIDELINES
    return _call_llm(system_prompt, user_prompt)


def synthesize_reading(question, cards_with_interpretations, analysis_report):
    """
    综合解读 — 在三张牌的单独解读基础上，给出整体能量与建议
    
    cards_with_interpretations: [{"position": ..., "card": ..., "interpretation": ...}, ...]
    """
    cards_summary = "\n\n".join([
        f"【{item['position']}】{item['card']}\n{item['interpretation']}"
        for item in cards_with_interpretations
    ])
    
    user_prompt = f"""用户的问题：{question}

你已经解读完了每张牌：
{cards_summary}

体系化分析参考：
{analysis_report}

现在请给一段【整体能量与核心指引】，要求：
1. 综合三张牌的能量流动（用元素分布和灵数变化说明）
2. 点明这次占卜的核心信息（一句话能讲清）
3. 给一个具体的、可执行的核心建议
4. 控制在 200 字以内
5. 语气温柔但有力量
6. 直接输出一段流畅文字，不要再分段或加小标题
7. 用中文"""
    
    system_prompt = "你是一位精通元素学与灵数学的资深塔罗师，擅长把多张牌的能量整合为有力的整体洞察。"
    return _call_llm(system_prompt, user_prompt)