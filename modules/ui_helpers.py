import pandas as pd
import streamlit as st

def render_clickable_table(df, link_col="링크"):
    config = {}
    if link_col in df.columns:
        config[link_col] = st.column_config.LinkColumn(
            "바로가기",
            help="클릭하면 상품 페이지로 이동합니다.",
            display_text="열기",
        )
    if "이미지" in df.columns:
        config["이미지"] = st.column_config.ImageColumn("썸네일", help="상품 썸네일")
    st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        disabled=True,
        column_config=config,
    )
