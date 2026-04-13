import re
import pandas as pd
import streamlit as st
from core.naver_api import search_many
from utils.db import insert_products, get_recent_products, log_event

TAG_RE = re.compile(r"<[^>]+>")

def _clean_html(text):
    if not isinstance(text, str):
        return text
    return TAG_RE.sub("", text)

def _render_clickable_table(df):
    st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        disabled=True,
        column_config={
            "링크": st.column_config.LinkColumn(
                "바로가기",
                help="클릭하면 상품 페이지로 이동합니다.",
                display_text="열기",
            )
        },
    )

def product_ui():
    st.subheader("상품 RADAR")
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
            items = search_many(keyword.strip(), pages=pages, display=100, sort=sort)
            rows = []
            view = []
            for item in items:
                name = _clean_html(item.get("title", ""))
                price = item.get("lprice", "")
                mall = item.get("mallName", "")
                link = item.get("link", "")
                rows.append(("naver", keyword.strip(), name, price, mall, link))
                view.append({"상품명": name, "가격": price, "몰": mall, "링크": link})
            saved = insert_products(rows)
            log_event("naver", "success", f"{keyword.strip()} / {saved}건 저장")
            st.success(f"{saved}건 저장했습니다.")
            _render_clickable_table(pd.DataFrame(view))
        except Exception as e:
            log_event("naver", "error", str(e))
            st.error(f"상품 검색 중 오류가 발생했습니다: {e}")

    st.divider()
    st.caption("최근 저장 데이터")
    rows = get_recent_products(limit=50, source="naver")
    if rows:
        df = pd.DataFrame(rows, columns=["id", "source", "keyword", "name", "price", "mall", "link", "collected_at"])
        show = df.rename(columns={"name": "상품명", "price": "가격", "mall": "몰", "link": "링크", "keyword": "키워드", "collected_at": "수집일시"})
        show = show[["상품명", "가격", "몰", "키워드", "링크", "수집일시"]]
        _render_clickable_table(show)
