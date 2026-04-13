import streamlit as st
from modules.keyword_radar import keyword_ui
from modules.product_radar import product_ui
from modules.competitor_radar import competitor_ui
from modules.insight import insight_ui
from utils.db import init_db

st.set_page_config(page_title="MD 레이다", layout="wide")
init_db()

st.title("📡 MD 레이다 (MD RADAR)")

menu = st.sidebar.radio("메뉴", [
    "키워드 RADAR",
    "상품 RADAR",
    "경쟁사 RADAR",
    "MD 인사이트"
])

if menu == "키워드 RADAR":
    keyword_ui()
elif menu == "상품 RADAR":
    product_ui()
elif menu == "경쟁사 RADAR":
    competitor_ui()
elif menu == "MD 인사이트":
    insight_ui()
