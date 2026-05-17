"""塔罗 AI 解读模块（升级版：融合元素+灵数体系）"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


def get_interpretation(question, cards_text, core_card, analysis_report):
    """
    生成融合元素+灵数体系的塔罗解读
    
    新增参数 analysis_report：来自 analyzer.build_analysis_report
    """
    prompt =f"""你是一位精通元素与灵数体系的资深塔罗师。

【用户的问题】
{question}

【抽到的三张牌】
{cards_text}

【你内部的分析依据（不要在回答中分段罗列，作为思考素材使用）】
{analysis_report}

---

请基于以上信息，给用户一段**流畅、温柔、有叙事感**的塔罗解读。

要求：
1. **像在和朋友说话**，不要使用 markdown 标题或分段小标题
2. 用一段（或最多两段）连贯的文字完成解读
3. 解读时**自然融入**元素和灵数的洞察（例如"火元素的能量在这里提醒你..."），但不要刻意分点列出
4. 核心牌是叙事的主线，辅助牌是补充的注脚
5. 结尾给一句话的核心建议
6. 总长度控制在 250-350 字
7. 用中文回答"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一位精通塔罗、元素学与灵数学的专业占卜师，解读时融合多重体系，给出有依据的洞察。"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ AI 解读失败：{e}\n请检查网络和 API key。"