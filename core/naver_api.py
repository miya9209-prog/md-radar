import requests
import streamlit as st

def search_naver_shopping(query, display=20, sort="sim"):
    url = "https://openapi.naver.com/v1/search/shop.json"
    headers = {
        "X-Naver-Client-Id": st.secrets["NAVER_CLIENT_ID"],
        "X-Naver-Client-Secret": st.secrets["NAVER_CLIENT_SECRET"],
    }
    params = {
        "query": query,
        "display": display,
        "sort": sort,
    }
    res = requests.get(url, headers=headers, params=params, timeout=20)
    res.raise_for_status()
    return res.json()
