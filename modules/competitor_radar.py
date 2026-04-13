import streamlit as st
from core.competitor_crawlers import run_all_crawlers
import pandas as pd

def competitor_ui():
    st.header("경쟁사 RADAR")

    if st.button("수집"):
        data = run_all_crawlers()
        df = pd.DataFrame(data)
        st.dataframe(df)
