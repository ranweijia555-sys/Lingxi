"""灵案 AstRa - 莫兰迪 + 神秘卡牌版"""
import time
import streamlit as st
from tarot.drawer import draw_cards, find_core_card
from tarot.analyzer import build_analysis_report
from tarot.interpreter import interpret_single_card, synthesize_reading
from tarot.data_loader import load_spreads, load_full_deck
from tarot.history import save_reading


st.set_page_config(
    page_title="灵案 AstRa",
    page_icon="✦",
    layout="centered"
)


# === CSS：莫兰迪柔光底 + 深色神秘卡牌 ===
st.markdown("""
<style>
    /* 字体 */
    html, body, [class*="st-"], button, input, textarea, select {
        font-family: 'Songti SC', 'Source Han Serif', 'Georgia', serif !important;
        color: #4A3D2F;
    }
    
    /* 主标题：金紫渐变 */
    .lingxi-title {
        text-align: center;
        font-size: 2.6rem;
        background: linear-gradient(120deg, #9B8AA5 30%, #C9A66B 70%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600;
        letter-spacing: 0.2em;
        margin: 30px 0 8px 0;
    }
    
    .lingxi-subtitle {
        text-align: center;
        color: #7A6B5C;
        font-size: 0.9rem;
        letter-spacing: 0.25em;
        margin-bottom: 36px;
        font-style: italic;
    }
    
    /* 小标题 */
    h3 {
        color: #5C4D3F !important;
        font-weight: 500;
        letter-spacing: 0.15em;
        border-bottom: 1px solid rgba(155, 138, 165, 0.25);
        padding-bottom: 8px;
        margin-top: 20px !important;
    }
    
    /* 输入框 / 下拉 */
    .stTextArea textarea, .stSelectbox div[data-baseweb] {
        background-color: #FAF6EF !important;
        border: 1px solid #D4C9B5 !important;
        border-radius: 8px !important;
        color: #4A3D2F !important;
    }
    
    /* 提示框 */
    .stAlert {
        background: rgba(184, 168, 201, 0.15) !important;
        border-left: 3px solid #9B8AA5 !important;
    }
    
    /* 按钮 */
    .stButton button {
        background: linear-gradient(135deg, #B5A892 0%, #9B8AA5 100%) !important;
        color: #FAF6EF !important;
        border: none !important;
        font-weight: 500 !important;
        padding: 12px 30px !important;
        border-radius: 30px !important;
        letter-spacing: 0.2em;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(74, 61, 47, 0.15);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(74, 61, 47, 0.25);
    }
    
    /* === 深色神秘塔罗卡牌 === */
    .tarot-card {
        background: 
            radial-gradient(circle at 30% 20%, rgba(201, 166, 107, 0.18), transparent 55%),
            linear-gradient(145deg, #2D2548 0%, #1A1530 60%, #15102A 100%);
        border: 2px solid #C9A66B;
        border-radius: 12px;
        padding: 26px 14px;
        margin: 10px 0;
        position: relative;
        text-align: center;
        box-shadow: 
            0 4px 20px rgba(74, 61, 47, 0.2),
            inset 0 0 30px rgba(201, 166, 107, 0.08);
        transition: all 0.4s ease;
        min-height: 280px;
    }
    
    .tarot-card:hover {
        transform: translateY(-4px);
        box-shadow: 
            0 8px 30px rgba(74, 61, 47, 0.3),
            inset 0 0 40px rgba(201, 166, 107, 0.18);
    }
    
    .tarot-card.core {
        border-color: #E8C988;
        box-shadow: 
            0 4px 25px rgba(232, 201, 136, 0.35),
            inset 0 0 40px rgba(232, 201, 136, 0.15);
    }
    
    /* 卡牌四角装饰星 */
    .tarot-card::before {
        content: "✦";
        position: absolute;
        top: 10px;
        left: 14px;
        color: rgba(201, 166, 107, 0.55);
        font-size: 0.9rem;
    }
    .tarot-card::after {
        content: "✦";
        position: absolute;
        bottom: 10px;
        right: 14px;
        color: rgba(201, 166, 107, 0.55);
        font-size: 0.9rem;
    }
    
    .card-position {
        font-size: 0.8rem;
        color: #C9A66B;
        margin-bottom: 12px;
        letter-spacing: 0.25em;
    }
    
    .card-name-zh {
        font-size: 1.5rem;
        color: #E8C988;
        font-weight: 600;
        margin: 12px 0 6px 0;
        letter-spacing: 0.12em;
    }
    
    .card-name-en {
        font-size: 0.7rem;
        color: #B5A892;
        font-style: italic;
        margin-bottom: 12px;
        letter-spacing: 0.05em;
    }
    
    .card-orientation {
        font-size: 0.78rem;
        color: #F5E6C8;
        margin: 6px 0;
        padding: 4px 14px;
        background: rgba(201, 166, 107, 0.18);
        border: 1px solid rgba(201, 166, 107, 0.35);
        border-radius: 12px;
        display: inline-block;
        letter-spacing: 0.15em;
    }
    
    .card-meaning {
        font-size: 0.85rem;
        color: #DDD0B0;
        margin-top: 14px;
        line-height: 1.7;
        font-style: italic;
        padding: 0 4px;
    }
    
    .core-badge {
        display: inline-block;
        background: linear-gradient(120deg, #E8C988, #C9A66B);
        color: #2D2548;
        padding: 3px 14px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-top: 10px;
        letter-spacing: 0.2em;
    }
    
    /* === 单卡解读区（替换 expander，避免 bug） === */
    .interp-block {
        background: rgba(184, 168, 201, 0.08);
        border-left: 3px solid #9B8AA5;
        padding: 20px 24px;
        margin: 14px 0;
        border-radius: 0 8px 8px 0;
        line-height: 1.9;
        color: #4A3D2F;
        font-size: 0.95rem;
    }
    
    .interp-block.core {
        border-left-color: #C9A66B;
        background: rgba(201, 166, 107, 0.08);
    }
    
    .interp-title {
        font-size: 1.05rem;
        color: #5C4D3F;
        font-weight: 600;
        margin-bottom: 12px;
        letter-spacing: 0.1em;
    }
    
    .interp-title.core {
        color: #8B6F2E;
    }
    
    /* 整体指引 */
    .summary-block {
        background: linear-gradient(145deg, rgba(232, 201, 136, 0.1), rgba(184, 168, 201, 0.06));
        border: 1px solid rgba(201, 166, 107, 0.35);
        border-radius: 12px;
        padding: 30px 28px 24px 28px;
        margin: 30px 0 20px 0;
        line-height: 1.95;
        color: #4A3D2F;
        position: relative;
        font-size: 0.97rem;
    }
    
    .summary-block::before {
        content: "✦  整 体 指 引  ✦";
        position: absolute;
        top: -11px;
        left: 50%;
        transform: translateX(-50%);
        background: #F2EDE4;
        padding: 0 16px;
        font-size: 0.75rem;
        color: #C9A66B;
        letter-spacing: 0.3em;
    }
    
    /* 分隔线 */
    hr {
        border: none !important;
        margin: 36px 0 !important;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(155, 138, 165, 0.35), transparent);
    }
    
    /* 页脚 */
    .footer {
        text-align: center;
        color: #B5A892;
        font-size: 0.72rem;
        letter-spacing: 0.4em;
        margin-top: 50px;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)


# === Session State ===
if "reading_done" not in st.session_state:
    st.session_state.reading_done = False
if "cards" not in st.session_state:
    st.session_state.cards = None


# === 标题 ===
st.markdown('<div class="lingxi-title">⊹ 灵 案  A s t R a ⊹</div>', unsafe_allow_html=True)
st.markdown('<div class="lingxi-subtitle">— 西 方 占 星 · 塔 罗 · 东 方 命 理 —</div>', unsafe_allow_html=True)


# === 输入区 ===
spreads = load_spreads()
spread_options = {s["name"]: key for key, s in spreads.items()}

selected_name = st.selectbox("📜  选择牌阵", list(spread_options.keys()))
selected_key = spread_options[selected_name]
selected_spread = spreads[selected_key]

st.info(f"💡 {selected_spread['description']}")

question = st.text_area(
    "🌙  你想问什么？",
    placeholder="例如：我下半年的事业会有什么变化？",
    height=80
)


# === 开始占卜按钮 ===
if st.button("✦  开 始 占 卜  ✦", type="primary", use_container_width=True):
    if not question.strip():
        st.warning("请先输入你的问题")
    else:
        with st.spinner("🌀 牌灵正在为你聚合能量..."):
            time.sleep(1.2)
            cards = draw_cards(selected_spread["card_count"])
        st.session_state.cards = cards
        st.session_state.spread = selected_spread
        st.session_state.question = question
        st.session_state.reading_done = True
        st.rerun()


# === 显示抽牌结果 ===
if st.session_state.reading_done and st.session_state.cards:
    cards = st.session_state.cards
    spread = st.session_state.spread
    question = st.session_state.question
    
    st.markdown("---")
    st.markdown("### 🌑  抽 到 的 牌")
    
    core_card = find_core_card(cards, logic=spread["logic"])
    arcana = load_full_deck()
    
    cols = st.columns(len(cards))
    for col, position, card_info in zip(cols, spread["positions"], cards):
        with col:
            is_core = (card_info["card"] == core_card["card"])
            card_data = arcana[card_info["card"]]
            orientation_zh = "正位 ⬆" if card_info["orientation"] == "upright" else "逆位 ⬇"
            meaning = card_data[card_info["orientation"]]
            
            card_class = "tarot-card core" if is_core else "tarot-card"
            core_badge = '<div class="core-badge">⊹ 核 心 牌 ⊹</div>' if is_core else ''
            
            st.markdown(f"""
            <div class="{card_class}">
                <div class="card-position">— {position} —</div>
                <div class="card-name-zh">{card_data['name_zh']}</div>
                <div class="card-name-en">{card_info['card']}</div>
                <div class="card-orientation">{orientation_zh}</div>
                <div class="card-meaning">{meaning}</div>
                {core_badge}
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.3)
    
    # === 逐张深度解读（弃用 expander，直接铺开）===
    st.markdown("---")
    st.markdown("### ✦  逐 张 深 度 解 读")
    
    cards_with_interpretations = []
    
    for position, card_info in zip(spread["positions"], cards):
        is_core = (card_info["card"] == core_card["card"])
        card_detail = arcana[card_info["card"]]
        
        block_class = "interp-block core" if is_core else "interp-block"
        title_class = "interp-title core" if is_core else "interp-title"
        core_marker = "  ⊹" if is_core else ""
        
        with st.spinner(f"🌙 塔罗师为「{position}」沉思..."):
            interpretation = interpret_single_card(
                question, card_info, position, card_detail, is_core
            )
        
        st.markdown(f"""
        <div class="{block_class}">
            <div class="{title_class}">{position}　·　{card_info['card']}{core_marker}</div>
            {interpretation}
        </div>
        """, unsafe_allow_html=True)
        
        cards_with_interpretations.append({
            "position": position,
            "card": card_info["card"],
            "interpretation": interpretation
        })
    
    # === 整体指引 ===
    st.markdown("---")
    
    analysis_report = build_analysis_report(cards, core_card)
    
    with st.spinner("🪄 综合所有牌的能量..."):
        summary = synthesize_reading(question, cards_with_interpretations, analysis_report)
    
    st.markdown(f"""
    <div class="summary-block">
    {summary}
    </div>
    """, unsafe_allow_html=True)
    
    # === 保存历史 ===
    reading_id = save_reading(
        question=question,
        spread_name=spread["name"],
        cards=cards,
        core_card=core_card,
        single_interpretations=cards_with_interpretations,
        summary=summary
    )
    st.caption(f"📜 已保存为占卜 #{reading_id}")
    
    if st.button("⊹  再 来 一 次  ⊹", use_container_width=True):
        st.session_state.reading_done = False
        st.session_state.cards = None
        st.rerun()


# === 页脚 ===
st.markdown(
    '<div class="footer">⊹  A S T  R A  ·  灵 案  ⊹</div>',
    unsafe_allow_html=True
)