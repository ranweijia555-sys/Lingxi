"""LLM 客户端工厂 — 统一管理 DeepSeek（文字）和 OpenAI（视觉）"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def _get_key(env_name, secret_name):
    """优先本地 .env，fallback 到 Streamlit Secrets"""
    key = os.getenv(env_name)
    if key:
        return key
    try:
        import streamlit as st
        return st.secrets[secret_name]
    except Exception:
        return None


def get_text_client():
    """文字解读用 DeepSeek（便宜）"""
    return OpenAI(
        api_key=_get_key("DEEPSEEK_API_KEY", "DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com"
    )


def get_vision_client():
    """视觉识别用 OpenAI（精度高）"""
    return OpenAI(
        api_key=_get_key("OPENAI_API_KEY", "OPENAI_API_KEY")
    )


# 模型名常量（方便统一管理 / 未来切换）
TEXT_MODEL = "deepseek-chat"
VISION_MODEL = "gpt-4o"
