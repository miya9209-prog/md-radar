import time
import pandas as pd
import streamlit as st
from core.keyword_service import build_keyword_rankings
from utils.db import insert_keyword_cache

def keyword_ui():
    st.subheader("키워드 RADAR")

    if "last_trend_refresh" not in st.session_state:
        st.session_state["last_trend_refresh"] = 0

    cooldown_sec = 300
    remain = cooldown_sec - (time.time() - st.session_state["last_trend_refresh"])

    if remain > 0:
        st.info(f"트렌드 새로고침은 {int(remain)}초 후 다시 가능합니다.")
    else:
        if st.button("트렌드 새로고침", use_container_width=True):
            st.session_state["last_trend_refresh"] = time.time()

            try:
                with st.spinner("트렌드 데이터 수집중입니다..."):
                    rankings = build_keyword_rankings()

                    rows = []
                    for period in ["daily", "weekly", "monthly"]:
                        for kw, score in rankings[period][:30]:
                            rows.append(("google_trends", period, kw, float(score)))

                    insert_keyword_cache(rows)

                st.success("트렌드 캐시를 갱신했습니다.")

                if rankings["failed"]:
                    st.warning(f"일부 키워드는 제한으로 제외됨 ({len(rankings['failed'])}개 묶음)")

            except Exception as e:
                st.error(f"트렌드 수집 중 오류가 발생했습니다: {e}")
