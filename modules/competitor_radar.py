import pandas as pd
import streamlit as st
from core.competitor_crawlers import run_all_crawlers
from utils.db import insert_products, log_event

def competitor_ui():
    st.header("경쟁사 RADAR")
    st.caption("현재 포함: 조아맘, 캔마트")

    if st.button("경쟁사 수집 실행", use_container_width=True):
        try:
            items = run_all_crawlers()
            rows = []
            view = []
            for item in items:
                rows.append((item["site"], "competitor", item["name"], item["price"], item["site"], item["link"]))
                view.append({
                    "사이트": item["site"],
                    "상품명": item["name"],
                    "가격": item["price"],
                    "링크": item["link"],
                })
            insert_products(rows)
            log_event("competitor", "success", f"{len(rows)}건 저장")
            if view:
                st.success(f"{len(view)}건 수집했습니다.")
                st.dataframe(pd.DataFrame(view), use_container_width=True)
            else:
                st.info("수집된 상품이 없습니다.")
        except Exception as e:
            log_event("competitor", "error", str(e))
            st.error(f"경쟁사 수집 중 오류가 발생했습니다: {e}")
