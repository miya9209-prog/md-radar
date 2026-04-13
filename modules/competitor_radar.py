import pandas as pd
import streamlit as st
from core.competitor_sources import COMPETITOR_MALLS, DEFAULT_KEYWORDS
from core.competitor_radar_service import collect_competitors_from_naver
from utils.db import insert_products, get_recent_products, log_event

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

def competitor_ui():
    st.subheader("경쟁사 RADAR")
    st.caption("경쟁사 직접 크롤링 대신, 네이버쇼핑 노출 결과에서 경쟁사 몰명을 필터링하는 방식으로 수집합니다.")

    c1, c2 = st.columns([3, 2])
    with c1:
        keyword = st.text_input("경쟁사 추적 키워드", placeholder="예: 여성 가디건")
    with c2:
        sort = st.selectbox("정렬 방식", ["sim", "date", "asc", "dsc"], key="comp_sort")

    selected = st.multiselect(
        "추적할 경쟁사 몰",
        COMPETITOR_MALLS,
        default=["조아맘", "캔마트", "퍼플리아", "그레이시크"],
    )

    c3, c4 = st.columns([1, 1])
    with c3:
        pages = st.selectbox("검색 페이지 수", [1, 2, 3], index=1, key="comp_pages")
    with c4:
        quick = st.selectbox("빠른 키워드", ["직접 입력"] + DEFAULT_KEYWORDS)

    if quick != "직접 입력" and not keyword:
        keyword = quick

    if st.button("경쟁사 수집 실행", use_container_width=True):
        if not keyword.strip():
            st.warning("키워드를 입력해 주세요.")
            return
        if not selected:
            st.warning("경쟁사 몰을 최소 1개 이상 선택해 주세요.")
            return
        try:
            items = collect_competitors_from_naver(
                keyword=keyword.strip(),
                selected_malls=selected,
                pages=pages,
                sort=sort,
            )
            rows = []
            view = []
            for item in items:
                rows.append(("competitor_naver", item["keyword"], item["name"], item["price"], item["site"], item["link"]))
                view.append({
                    "몰": item["site"],
                    "상품명": item["name"],
                    "가격": item["price"],
                    "키워드": item["keyword"],
                    "링크": item["link"],
                })
            saved = insert_products(rows)
            log_event("competitor_naver", "success", f"{keyword.strip()} / {saved}건 저장")
            if saved:
                st.success(f"{saved}건 저장했습니다.")
                _render_clickable_table(pd.DataFrame(view))
            else:
                st.info("해당 키워드에서 선택한 경쟁사 결과를 찾지 못했습니다.")
        except Exception as e:
            log_event("competitor_naver", "error", str(e))
            st.error(f"경쟁사 수집 중 오류가 발생했습니다: {e}")

    st.divider()
    st.caption("최근 저장 데이터")
    rows = get_recent_products(limit=100, source="competitor_naver")
    if rows:
        df = pd.DataFrame(rows, columns=["id", "source", "keyword", "name", "price", "mall", "link", "collected_at"])
        show = df.rename(columns={"name": "상품명", "price": "가격", "mall": "몰", "link": "링크", "keyword": "키워드", "collected_at": "수집일시"})
        show = show[["몰", "상품명", "가격", "키워드", "링크", "수집일시"]]
        _render_clickable_table(show)
