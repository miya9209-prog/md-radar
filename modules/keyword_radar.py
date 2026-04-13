import streamlit as st
from core.google_trends import get_trends

def keyword_ui():
    st.header("키워드 RADAR")
    keyword = st.text_input("키워드 입력", placeholder="예: 40대 가디건")

    if st.button("키워드 분석", use_container_width=True):
        if not keyword.strip():
            st.warning("키워드를 입력해 주세요.")
            return
        try:
            data = get_trends(keyword.strip())
            if data.empty:
                st.info("표시할 트렌드 데이터가 없습니다.")
            else:
                st.line_chart(data[[keyword.strip()]])
                st.dataframe(data.reset_index(), use_container_width=True)
        except Exception as e:
            st.error(f"키워드 분석 중 오류가 발생했습니다: {e}")
