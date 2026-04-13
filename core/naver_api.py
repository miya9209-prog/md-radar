import requests
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

def search_naver_shopping(query):
    url = "https://openapi.naver.com/v1/search/shop.json"

    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET
    }

    params = {
        "query": query,
        "display": 20
    }

    res = requests.get(url, headers=headers, params=params)
    return res.json()
