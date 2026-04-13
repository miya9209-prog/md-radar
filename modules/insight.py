import streamlit as st
from core.gpt_insight import generate_insight
from utils.db import get_db_location_text

def insight_ui():
    st.header("MD 인사이트")
    st.caption(f"DB 저장 위치: {get_db_location_text()}")

    if st.button("GPT 분석 실행", use_container_width=True):
        try:
            result = generate_insight()
            st.write(result)
        except Exception as e:
            st.error(f"GPT 분석 중 오류가 발생했습니다: {e}")
