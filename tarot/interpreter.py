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

RESPONSIBLE_AI_GUIDELINES_EN = """
Treat tarot as a reflective tool, never as certainty or professional advice. Do not predict death,
disaster, illness, or guaranteed outcomes. For medical, mental-health, legal, financial, relationship,
or other major decisions, keep firm boundaries and encourage appropriate professional or trusted
support. Avoid restrictive body, diet, calorie, or exercise targets. Be warm and thoughtful without
pet names, fear-based language, or exaggerated claims.
"""

VAGUE_LANGUAGE_BAN = """
禁止使用以下空转词汇及同类表达：
能量流动、元素分布、内在笃定、云开见月、温柔过渡、能量在平衡、像一条河流、
牌灵、聚合能量、水元素为主、火风水、温柔地过渡、重新相信、跟随直觉中的笃定。
"""

"""塔罗 AI 解读模块（多步链式版：单卡深读 + 整体汇总）"""
from tarot.analyzer import build_analysis_report
from tarot.llm_client import get_text_client, TEXT_MODEL

client = get_text_client()


def _call_llm(system_prompt, user_prompt):
    """统一的 LLM 调用接口"""
    try:
        response = client.chat.completions.create(
            model=TEXT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ AI 解读失败：{e}"


def interpret_single_card(question, card_info, position, card_detail, is_core, language="zh"):
    """
    解读单张牌

    card_info: {"card": "...", "orientation": "..."}
    position: "牌一" / "过去" / "今日指引" 等
    card_detail: 包含 element, planet, number, upright, reversed 等
    is_core: 是否为核心牌
    """
    orientation_zh = "正位" if card_info["orientation"] == "upright" else "逆位"
    orientation_en = "upright" if card_info["orientation"] == "upright" else "reversed"
    meaning = card_detail["upright"] if card_info["orientation"] == "upright" else card_detail["reversed"]

    role_label = "（核心牌 ⭐）" if is_core else ""

    if language == "en":
        user_prompt = f"""The user's question: {question}

Card to interpret:
- Position: {position}{" (core card)" if is_core else ""}
- Card: {card_info['card']} ({orientation_en})
- Element: {card_detail.get('element', '?')}
- Astrological correspondence: {card_detail.get('planet', '?')}
- Number: {card_detail.get('number', '?')}
- Traditional meaning: {meaning}

Write a focused interpretation of 90–130 words. Connect the card directly to the question, weave in
elemental or astrological details only when useful, and provide grounded reflection rather than a
fixed prediction. Return one natural paragraph in English without a heading."""
        system_prompt = (
            "You are a thoughtful, grounded tarot reader who uses elemental and astrological symbolism.\n\n"
            + RESPONSIBLE_AI_GUIDELINES_EN
        )
        return _call_llm(system_prompt, user_prompt)

    user_prompt = f"""用户的问题：{question}

需要解读的牌：
- 位置：{position} {role_label}
- 牌名：{card_info['card']}（{orientation_zh}）
- 元素：{card_detail.get('element', '?')}
- 占星对应：{card_detail.get('planet', '?')}
- 编号：{card_detail.get('number', '?')}
- 权威依据 —— 必须严格遵循：{meaning}

请给出这张牌在此问题下的解读，要求：
1. 控制在 100-150 字，一段话，无标题
2. 必须包含三项，自然融入叙述中：
   - 具体场景：这张牌在用户问题中对应什么现实情境
   - 可辨认信号：用户可观察到的具体现象（如「某段对话反复出现」「某项计划迟迟未启动」）
   - 可执行动作：一个今天或本周内可完成的小步骤
3. 元素/占星信息只在能解释上述三项时使用，禁止硬塞
4. 紧扣用户问题，禁止泛泛而谈
5. 用中文

{VAGUE_LANGUAGE_BAN}"""

    system_prompt = (
        "你是一位落地型塔罗师，擅长把牌义翻译成具体情境与可执行建议。"
        "准确应用体系，而不是产出优美文字。\n\n"
        + RESPONSIBLE_AI_GUIDELINES
    )
    return _call_llm(system_prompt, user_prompt)


def synthesize_reading(question, cards_with_interpretations, cards, core_card, language="zh"):
    """
    综合解读 — 在三张牌的单独解读基础上，给出整体能量与建议

    cards_with_interpretations: [{"position": ..., "card": ..., "interpretation": ...}, ...]
    """
    analysis_report = build_analysis_report(cards, core_card, question=question)

    cards_summary = "\n\n".join([
        f"【{item['position']}】{item['card']}\n{item['interpretation']}"
        for item in cards_with_interpretations
    ])

    if language == "en":
        user_prompt = f"""The user's question: {question}

The individual card interpretations are complete:
{cards_summary}

Systemic analysis reference:
{analysis_report}

Synthesize the reading in no more than 170 words. Describe the movement across the cards, state the
central insight clearly, and finish with one specific, realistic next step. Keep the tone warm,
grounded, and non-deterministic. Return one flowing paragraph in English without a heading."""
        system_prompt = (
            "You synthesize multi-card tarot readings into clear, practical reflection.\n\n"
            + RESPONSIBLE_AI_GUIDELINES_EN
        )
        return _call_llm(system_prompt, user_prompt)

    user_prompt = f"""用户的问题：{question}

各张牌的单独解读：
{cards_summary}

体系化分析（含元素张力、灵数轨迹、核心判断）：
{analysis_report}

请先内部完成推理（不要输出推理过程），再输出综合指引。

输出必须包含以下四项，自然融入 200 字以内的一段中文，不要加小标题或编号：
1. 叙事顺序：按牌阵位置说明事情如何展开（从第一张到最后一张各推进一步）
2. 核心判断：一句话讲清这次占卜最关键的结论（直接引用体系化核心判断中的逻辑）
3. 具体动作：一个本周内可执行、可验证的步骤
4. 可辨认的信号：一句「如果接下来你注意到 X，说明这条线在兑现」格式的观察点

要求：
- 禁止描述「能量流动」「元素分布」等抽象过程，改用因果链和具体事件语言
- 语气清晰、有边界，不要称呼「亲爱的」
- 用中文

{VAGUE_LANGUAGE_BAN}"""

    system_prompt = (
        "你是一位落地型塔罗师，擅长把体系化分析翻译成具体判断与行动建议。"
        "准确应用体系，而不是产出优美文字。\n\n"
        + RESPONSIBLE_AI_GUIDELINES
    )
    return _call_llm(system_prompt, user_prompt)
