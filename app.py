import streamlit as st
from modules.keyword_radar import keyword_ui
from modules.product_radar import product_ui
from modules.competitor_radar import competitor_ui
from modules.insight import insight_ui
from utils.db import init_db

st.set_page_config(page_title="MD 레이다", layout="wide")
init_db()

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2.2rem;
        padding-bottom: 2rem;
    }
    .top-nav-wrap {
        margin-top: 0.4rem;
        margin-bottom: 1.2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("# 📡 MD 레이다 (MD RADAR)")
st.caption("키워드 트렌드, 포털 상품 검색, 경쟁사 추적, GPT 인사이트를 한 화면에서 확인합니다.")

st.markdown('<div class="top-nav-wrap"></div>', unsafe_allow_html=True)

menu = st.radio(
    "메뉴",
    ["키워드 RADAR", "상품 RADAR", "경쟁사 RADAR", "MD 인사이트"],
    horizontal=True,
    label_visibility="collapsed",
)

if menu == "키워드 RADAR":
    keyword_ui()
elif menu == "상품 RADAR":
    product_ui()
elif menu == "경쟁사 RADAR":
    competitor_ui()
elif menu == "MD 인사이트":
    insight_ui()
