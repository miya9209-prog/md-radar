import streamlit as st
from modules.keyword_radar import keyword_ui
from modules.product_radar import product_ui
from modules.competitor_radar import competitor_ui
from modules.insight import insight_ui
from utils.db import init_db

st.set_page_config(page_title="MD 레이다", layout="wide")
init_db()

st.markdown("""
<style>
.block-container {padding-top: 2.1rem; padding-bottom: 2rem;}
div[data-baseweb="tab-list"] {gap: 0.25rem;}
</style>
""", unsafe_allow_html=True)

st.markdown("# 📡 MD 레이다 (MD RADAR)")
st.caption("키워드 트렌드, 포털 상품 검색, 경쟁사 추적, GPT 인사이트를 한 화면에서 확인합니다.")

tab1, tab2, tab3, tab4 = st.tabs(["키워드 RADAR", "상품 RADAR", "경쟁사 RADAR", "MD 인사이트"])

with tab1:
    keyword_ui()
with tab2:
    product_ui()
with tab3:
    competitor_ui()
with tab4:
    insight_ui()
