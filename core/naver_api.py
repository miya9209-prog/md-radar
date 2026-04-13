import requests
import streamlit as st

BASE_URL = "https://openapi.naver.com/v1/search/shop.json"

def search_naver_shopping(query, display=50, start=1, sort="sim"):
    headers = {
        "X-Naver-Client-Id": st.secrets["NAVER_CLIENT_ID"],
        "X-Naver-Client-Secret": st.secrets["NAVER_CLIENT_SECRET"],
    }
    params = {
        "query": query,
        "display": max(1, min(int(display), 100)),
        "start": max(1, min(int(start), 1000)),
        "sort": sort,
    }
    res = requests.get(BASE_URL, headers=headers, params=params, timeout=20)
    res.raise_for_status()
    return res.json()

def search_many(query, pages=2, display=50, sort="sim"):
    items = []
    for page in range(pages):
        start = page * display + 1
        data = search_naver_shopping(query=query, display=display, start=start, sort=sort)
        batch = data.get("items", [])
        if not batch:
            break
        items.extend(batch)
        if len(batch) < display:
            break
    return items
