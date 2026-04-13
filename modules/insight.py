import streamlit as st
from core.gpt_insight import generate_insight

def insight_ui():
    st.header("MD 인사이트")

    if st.button("분석 실행"):
        result = generate_insight()
        st.write(result)
