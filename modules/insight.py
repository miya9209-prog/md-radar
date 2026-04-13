import pandas as pd
import streamlit as st
from core.gpt_insight import generate_insight
from utils.db import get_db_path_text, get_summary_stats

def insight_ui():
    st.subheader("MD 인사이트")
    st.caption(f"DB 저장 위치: {get_db_path_text()}")

    stats = get_summary_stats()
    c1, c2 = st.columns(2)
    with c1:
        st.metric("전체 저장 건수", stats["total"])
    with c2:
        st.metric("수집 소스 수", len(stats["by_source"]))

    if stats["by_source"]:
        st.write("소스별 수집 현황")
        st.dataframe(pd.DataFrame(stats["by_source"], columns=["source", "count"]), use_container_width=True)

    if stats["by_mall"]:
        st.write("몰별 상위 현황")
        st.dataframe(pd.DataFrame(stats["by_mall"], columns=["mall", "count"]), use_container_width=True)

    if st.button("GPT 분석 실행", use_container_width=True):
        try:
            result = generate_insight()
            st.write(result)
        except Exception as e:
            st.error(f"GPT 분석 중 오류가 발생했습니다: {e}")
