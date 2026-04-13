import streamlit as st
from core.google_trends import get_trends

def keyword_ui():
    st.header("키워드 RADAR")
    keyword = st.text_input("키워드")

    if st.button("분석"):
        data = get_trends(keyword)
        st.line_chart(data)
