"""灵案 AstRa - Streamlit 网页版（含拍照识别）"""
import time
import streamlit as st
from tarot.drawer import draw_cards, find_core_card
from tarot.interpreter import interpret_single_card, synthesize_reading
from tarot.data_loader import load_spreads, load_full_deck
from tarot.history import save_reading
from tarot.vision import recognize_cards


st.set_page_config(
    page_title="灵案 AstRa",
    page_icon="✦",
    layout="centered"
)


# === CSS（沿用莫兰迪 + 神秘卡牌）===
st.markdown("""
<style>
    html, body, [class*="st-"], button, input, textarea, select {
        font-family: 'Songti SC', 'Source Han Serif', 'Georgia', serif !important;
        color: #4A3D2F;
    }
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
    h3 {
        color: #5C4D3F !important;
        font-weight: 500;
        letter-spacing: 0.15em;
        border-bottom: 1px solid rgba(155, 138, 165, 0.25);
        padding-bottom: 8px;
        margin-top: 20px !important;
    }
    .stButton button {
        background: linear-gradient(135deg, #B5A892 0%, #9B8AA5 100%) !important;
        color: #FAF6EF !important;
        border: none !important;
        font-weight: 500 !important;
        padding: 12px 30px !important;
        border-radius: 30px !important;
        letter-spacing: 0.2em;
        transition: all 0.3s ease;
    }
    .stButton button:hover { transform: translateY(-2px); }
    .tarot-card {
        background: linear-gradient(145deg, #2D2548 0%, #1A1530 60%, #15102A 100%);
        border: 2px solid #C9A66B;
        border-radius: 12px;
        padding: 26px 14px;
        margin: 10px 0;
        text-align: center;
        min-height: 280px;
        position: relative;
    }
    .tarot-card.core { border-color: #E8C988; }
    .card-position { font-size: 0.8rem; color: #C9A66B; margin-bottom: 12px; letter-spacing: 0.25em; }
    .card-name-zh { font-size: 1.5rem; color: #E8C988; font-weight: 600; margin: 12px 0 6px 0; }
    .card-name-en { font-size: 0.7rem; color: #B5A892; font-style: italic; margin-bottom: 12px; }
    .card-orientation { font-size: 0.78rem; color: #F5E6C8; padding: 4px 14px; background: rgba(201,166,107,0.18); border-radius: 12px; display: inline-block; }
    .card-meaning { font-size: 0.85rem; color: #DDD0B0; margin-top: 14px; line-height: 1.7; font-style: italic; }
    .core-badge { display: inline-block; background: linear-gradient(120deg, #E8C988, #C9A66B); color: #2D2548; padding: 3px 14px; border-radius: 12px; font-size: 0.7rem; font-weight: 600; margin-top: 10px; }
    .interp-block { background: rgba(184,168,201,0.08); border-left: 3px solid #9B8AA5; padding: 20px 24px; margin: 14px 0; border-radius: 0 8px 8px 0; line-height: 1.9; }
    .interp-block.core { border-left-color: #C9A66B; background: rgba(201,166,107,0.08); }
    .interp-title { font-size: 1.05rem; color: #5C4D3F; font-weight: 600; margin-bottom: 12px; }
    .interp-title.core { color: #8B6F2E; }
    .summary-block { background: linear-gradient(145deg, rgba(232,201,136,0.1), rgba(184,168,201,0.06)); border: 1px solid rgba(201,166,107,0.35); border-radius: 12px; padding: 30px 28px 24px 28px; margin: 30px 0 20px 0; line-height: 1.95; position: relative; }
    hr { border: none !important; margin: 36px 0 !important; height: 1px; background: linear-gradient(90deg, transparent, rgba(155,138,165,0.35), transparent); }
    .footer { text-align: center; color: #B5A892; font-size: 0.72rem; letter-spacing: 0.4em; margin-top: 50px; font-style: italic; }
</style>
""", unsafe_allow_html=True)


# === Session State ===
for key in ["reading_done", "cards", "recognized_cards", "mode"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "reading_done" else False


# === 标题 ===
st.markdown('<div class="lingxi-title">⊹ 灵 案  A s t R a ⊹</div>', unsafe_allow_html=True)
st.markdown('<div class="lingxi-subtitle">— 西 方 占 星 · 塔 罗 · 东 方 命 理 —</div>', unsafe_allow_html=True)


spreads = load_spreads()
spread_options = {s["name"]: key for key, s in spreads.items()}
arcana = load_full_deck()


# === 模式选择 ===
mode = st.radio(
    "选择方式",
    ["🎴 系统为我抽牌", "📷 我拍照识别自己抽的牌"],
    horizontal=True
)


# === 牌阵选择（两种模式都要）===
selected_name = st.selectbox("📜 选择牌阵", list(spread_options.keys()))
selected_key = spread_options[selected_name]
selected_spread = spreads[selected_key]
st.info(f"💡 {selected_spread['description']}")


# === 拍照识别模式 ===
recognized = None
if mode == "📷 我拍照识别自己抽的牌":
    uploaded = st.file_uploader(
        "📷 上传你抽的牌的照片（清晰平铺最佳）",
        type=["jpg", "jpeg", "png"]
    )
    
    if uploaded:
        st.image(uploaded, caption="你上传的照片", width=400)
        
        if st.button("🔍 识别这些牌"):
            with st.spinner("👁️ AI 正在识别牌面..."):
                image_bytes = uploaded.getvalue()
                result = recognize_cards(image_bytes, expected_count=selected_spread["card_count"])
            
            if result["success"] and result["cards"]:
                st.session_state.recognized_cards = result["cards"]
                st.success(f"✅ 识别到 {len(result['cards'])} 张牌，请在下方确认或修正")
            else:
                st.error(f"❌ {result.get('error', '识别失败，请换一张更清晰的照片，或改用系统抽牌')}")
    
    # 显示识别结果 + 让用户修正
    if st.session_state.recognized_cards:
        st.markdown("### ✍️ 确认 / 修正识别结果")
        all_card_names = list(arcana.keys())
        
        corrected = []
        for i, c in enumerate(st.session_state.recognized_cards):
            col1, col2 = st.columns([3, 1])
            with col1:
                default_idx = all_card_names.index(c["card"]) if c["card"] in all_card_names else 0
                chosen = st.selectbox(
                    f"第 {i+1} 张" + ("  ⚠️置信度低" if c["confidence"] < 0.7 else ""),
                    all_card_names,
                    index=default_idx,
                    key=f"card_{i}"
                )
            with col2:
                ori = st.selectbox(
                    "方向",
                    ["upright", "reversed"],
                    index=0 if c["orientation"] == "upright" else 1,
                    format_func=lambda x: "正位" if x == "upright" else "逆位",
                    key=f"ori_{i}"
                )
            corrected.append({"card": chosen, "orientation": ori})
        
        recognized = corrected


# === 问题输入 ===
question = st.text_area("🌙 你想问什么？", placeholder="例如：我下半年的事业会有什么变化？", height=80)


# === 开始占卜 ===
button_label = "✦ 开 始 解 读 ✦" if mode == "📷 我拍照识别自己抽的牌" else "✦ 开 始 占 卜 ✦"

if st.button(button_label, type="primary", use_container_width=True):
    if not question.strip():
        st.warning("请先输入你的问题")
    elif mode == "📷 我拍照识别自己抽的牌" and not recognized:
        st.warning("请先上传照片并识别牌面")
    else:
        if mode == "📷 我拍照识别自己抽的牌":
            cards = recognized
        else:
            with st.spinner("🌀 牌灵正在聚合能量..."):
                time.sleep(1)
                cards = draw_cards(selected_spread["card_count"])
        
        st.session_state.cards = cards
        st.session_state.spread = selected_spread
        st.session_state.question = question
        st.session_state.reading_done = True
        st.rerun()


# === 显示结果 ===
if st.session_state.reading_done and st.session_state.cards:
    cards = st.session_state.cards
    spread = st.session_state.spread
    question = st.session_state.question
    
    st.markdown("---")
    st.markdown("### 🌑 你的牌")
    
    core_card = find_core_card(cards, logic=spread["logic"])
    
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
    
    st.markdown("---")
    st.markdown("### ✦ 逐 张 深 度 解 读")
    
    cards_with_interpretations = []
    for position, card_info in zip(spread["positions"], cards):
        is_core = (card_info["card"] == core_card["card"])
        card_detail = arcana[card_info["card"]]
        block_class = "interp-block core" if is_core else "interp-block"
        title_class = "interp-title core" if is_core else "interp-title"
        core_marker = "  ⊹" if is_core else ""
        with st.spinner(f"🌙 塔罗师为「{position}」沉思..."):
            interpretation = interpret_single_card(question, card_info, position, card_detail, is_core)
        st.markdown(f"""
        <div class="{block_class}">
            <div class="{title_class}">{position}　·　{card_info['card']}{core_marker}</div>
            {interpretation}
        </div>
        """, unsafe_allow_html=True)
        cards_with_interpretations.append({"position": position, "card": card_info["card"], "interpretation": interpretation})
    
    st.markdown("---")
    with st.spinner("🪄 综合所有牌的能量..."):
        summary = synthesize_reading(question, cards_with_interpretations, cards, core_card)
    st.markdown(f'<div class="summary-block">{summary}</div>', unsafe_allow_html=True)
    
    reading_id = save_reading(
        question=question, spread_name=spread["name"], cards=cards,
        core_card=core_card, single_interpretations=cards_with_interpretations, summary=summary
    )
    st.caption(f"📜 已保存为占卜 #{reading_id}")
    
    if st.button("⊹ 再 来 一 次 ⊹", use_container_width=True):
        for key in ["reading_done", "cards", "recognized_cards"]:
            st.session_state[key] = None if key != "reading_done" else False
        st.rerun()


st.markdown('<div class="footer">⊹  A S T  R A  ·  灵 案  ⊹</div>', unsafe_allow_html=True)