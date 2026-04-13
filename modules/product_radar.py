import pandas as pd
import streamlit as st
from core.product_service import collect_products_by_keyword, discover_hot_categories
from modules.ui_helpers import render_clickable_table
from utils.db import insert_products, get_recent_products, log_event

def product_ui():
    st.subheader("상품 RADAR")

    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("#### 놓치기 쉬운 핫 카테고리")
    with c2:
        if st.button("카테고리 탐색 갱신", use_container_width=True):
            st.session_state["refresh_hot_categories"] = True

    if st.session_state.get("refresh_hot_categories", True):
        try:
            ranking, samples = discover_hot_categories(pages=1)
            st.session_state["hot_category_ranking"] = ranking
            st.session_state["hot_category_samples"] = samples
            st.session_state["refresh_hot_categories"] = False
        except Exception as e:
            st.error(f"카테고리 탐색 중 오류가 발생했습니다: {e}")

    ranking = st.session_state.get("hot_category_ranking", [])
    samples = st.session_state.get("hot_category_samples", [])

    if ranking:
        st.dataframe(pd.DataFrame(ranking), use_container_width=True, hide_index=True)

    if samples:
        st.caption("카테고리 탐색 샘플")
        render_clickable_table(pd.DataFrame(samples[:20]))

    st.divider()
    st.markdown("#### 직접 검색")
    c1, c2, c3 = st.columns([4, 1, 1])
    with c1:
        keyword = st.text_input("상품 키워드", placeholder="예: 40대 여성 티셔츠")
    with c2:
        sort = st.selectbox("정렬", ["sim", "date", "asc", "dsc"])
    with c3:
        pages = st.selectbox("수집량", [1, 2, 3], index=1)

    if st.button("네이버 검색", use_container_width=True):
        if not keyword.strip():
            st.warning("상품 키워드를 입력해 주세요.")
            return
        try:
            rows, cards = collect_products_by_keyword(keyword.strip(), pages=pages, sort=sort)
            saved = insert_products(rows)
            log_event("naver", "success", f"{keyword.strip()} / {saved}건 저장")
            st.success(f"{saved}건 저장했습니다.")
            render_clickable_table(pd.DataFrame(cards))
        except Exception as e:
            log_event("naver", "error", str(e))
            st.error(f"상품 검색 중 오류가 발생했습니다: {e}")

    st.divider()
    st.caption("최근 저장 데이터")
    rows = get_recent_products(limit=50, source="naver")
    if rows:
        df = pd.DataFrame(rows, columns=["id","source","keyword","category","name","price","mall","link","image_url","collected_at"])
        show = df.rename(columns={"keyword":"키워드","category":"카테고리","name":"상품명","price":"가격","mall":"몰","link":"링크","image_url":"이미지","collected_at":"수집일시"})
        show = show[["이미지","상품명","카테고리","가격","몰","키워드","링크","수집일시"]]
        render_clickable_table(show)
