"""Streamlit 入门 demo"""
import streamlit as st

# 标题
st.title("🔮 灵犀塔罗 - 入门 Demo")

# 文字
st.write("欢迎来到我的第一个 Streamlit 网页")

# 输入框
name = st.text_input("你叫什么名字？")
if name:
    st.success(f"你好，{name}！")

# 按钮
if st.button("点我抽一张牌"):
    import random
    cards = ["愚人 🤡", "魔术师 ✨", "女祭司 🌙", "太阳 ☀️"]
    st.info(f"你抽到了：**{random.choice(cards)}**")

# 选择框
spread = st.selectbox(
    "你想用哪种牌阵？",
    ["单张指引", "三张无牌阵", "三张时间线"]
)
st.write(f"你选了：{spread}")

# 多列布局
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("已占卜次数", "12")
with col2:
    st.metric("最爱牌阵", "三张无牌阵")
with col3:
    st.metric("今日运势", "🌟")
    