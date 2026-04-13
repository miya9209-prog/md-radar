import streamlit as st
from core.naver_api import search_naver_shopping
import pandas as pd

def product_ui():
    st.header("상품 RADAR")
    keyword = st.text_input("상품 키워드")

    if st.button("검색"):
        result = search_naver_shopping(keyword)
        df = pd.DataFrame(result.get("items", []))
        st.dataframe(df)
