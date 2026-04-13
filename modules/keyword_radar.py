import pandas as pd
import streamlit as st
from core.google_trends import get_trends
from core.keyword_service import build_keyword_rankings
from utils.db import insert_keyword_cache, get_recent_keywords, log_event

def _show_rank_table(rows):
    if not rows:
        st.info("아직 데이터가 없습니다. '트렌드 새로고침'을 눌러주세요.")
        return
    df = pd.DataFrame(rows, columns=["id", "source", "period", "keyword", "score", "collected_at"])
    df = df[["keyword", "score"]].sort_values("score", ascending=False)
    st.dataframe(df, use_container_width=True, hide_index=True)

def keyword_ui():
    st.subheader("키워드 RADAR")
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown("#### 오늘/주간/월간 트렌드 요약")
    with c2:
        if st.button("트렌드 새로고침", use_container_width=True):
            try:
                with st.spinner("트렌드 데이터 수집중입니다..."):
                    rankings = build_keyword_rankings()
                    rows = []
                    for period, values in rankings.items():
                        for kw, score in values[:30]:
                            rows.append(("google_trends", period, kw, float(score)))
                    insert_keyword_cache(rows)
                    log_event("google_trends", "success", f"{len(rows)}건 저장")
                st.success("트렌드 캐시를 갱신했습니다.")
            except Exception as e:
                log_event("google_trends", "error", str(e))
                st.error(f"트렌드 수집 중 오류가 발생했습니다: {e}")

    daily = get_recent_keywords(limit=20, source="google_trends", period="daily")
    weekly = get_recent_keywords(limit=20, source="google_trends", period="weekly")
    monthly = get_recent_keywords(limit=20, source="google_trends", period="monthly")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**일간 상위 키워드**")
        _show_rank_table(daily)
    with c2:
        st.markdown("**주간 상위 키워드**")
        _show_rank_table(weekly)
    with c3:
        st.markdown("**월간 상위 키워드**")
        _show_rank_table(monthly)

    st.divider()
    st.markdown("#### 직접 검색")
    keyword = st.text_input("키워드 입력", placeholder="예: 40대 여성 가디건")
    if st.button("키워드 분석", use_container_width=True):
        if not keyword.strip():
            st.warning("키워드를 입력해 주세요.")
            return
        try:
            with st.spinner("키워드 분석중입니다..."):
                df = get_trends(keyword.strip(), timeframe="today 3-m")
            if df.empty or keyword.strip() not in df.columns:
                st.warning("표시할 트렌드 데이터가 없습니다. 다른 키워드를 시도해 보세요.")
            else:
                st.line_chart(df[[keyword.strip()]])
                st.dataframe(df.reset_index(), use_container_width=True)
        except Exception as e:
            st.error(f"키워드 분석 중 오류가 발생했습니다: {e}")
