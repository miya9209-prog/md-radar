import re
import pandas as pd
import streamlit as st
from core.naver_api import search_naver_shopping
from utils.db import insert_products, get_recent_products, log_event

TAG_RE = re.compile(r"<[^>]+>")

def _clean_html(text):
    if not isinstance(text, str):
        return text
    return TAG_RE.sub("", text)

def product_ui():
    st.header("상품 RADAR")
    col1, col2 = st.columns([4,1])
    with col1:
        keyword = st.text_input("상품 키워드", placeholder="예: 여성 가디건")
    with col2:
        sort = st.selectbox("정렬", ["sim", "date", "asc", "dsc"])

    if st.button("네이버 검색", use_container_width=True):
        if not keyword.strip():
            st.warning("상품 키워드를 입력해 주세요.")
            return
        try:
            result = search_naver_shopping(keyword.strip(), display=20, sort=sort)
            items = result.get("items", [])
            rows = []
            cleaned = []
            for item in items:
                name = _clean_html(item.get("title", ""))
                price = item.get("lprice", "")
                mall = item.get("mallName", "")
                link = item.get("link", "")
                rows.append(("naver", keyword.strip(), name, price, mall, link))
                cleaned.append({
                    "상품명": name,
                    "가격": price,
                    "몰": mall,
                    "링크": link
                })
            insert_products(rows)
            log_event("naver", "success", f"{keyword.strip()} / {len(rows)}건 저장")
            if cleaned:
                st.dataframe(pd.DataFrame(cleaned), use_container_width=True)
            else:
                st.info("검색 결과가 없습니다.")
        except Exception as e:
            log_event("naver", "error", str(e))
            st.error(f"상품 검색 중 오류가 발생했습니다: {e}")

    st.divider()
    st.subheader("최근 저장 데이터")
    rows = get_recent_products(limit=50)
    if rows:
        df = pd.DataFrame(rows, columns=["id","source","keyword","name","price","mall","link","collected_at"])
        st.dataframe(df, use_container_width=True)
    else:
        st.caption("아직 저장된 상품이 없습니다.")
