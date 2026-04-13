import streamlit as st
from openai import OpenAI
from utils.db import get_product_names

def generate_insight():
    names = get_product_names(limit=50)
    if not names:
        return "먼저 상품 RADAR나 경쟁사 RADAR에서 데이터를 수집해 주세요."

    text_data = "\n".join(names)
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    prompt = f'''
아래는 최근 수집된 상품명 목록입니다.

{text_data}

다음 형식으로 한국어로 정리해 주세요.
1. 핵심 키워드 5개
2. 반복되는 스타일/소재/핏 특징
3. 가격 전략에 대한 추정 포인트
4. 다음 상품기획 추천 5가지

너무 장황하지 않게, 실무 MD가 바로 볼 수 있게 정리해 주세요.
'''

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return res.choices[0].message.content
