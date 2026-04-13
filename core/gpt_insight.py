import streamlit as st
from openai import OpenAI
from utils.db import get_names_for_insight, get_summary_stats

def generate_insight():
    names = get_names_for_insight(limit=120)
    if not names:
        return "먼저 상품 RADAR 또는 경쟁사 RADAR에서 데이터를 수집해 주세요."

    stats = get_summary_stats()
    by_source = "\n".join([f"- {src}: {cnt}건" for src, cnt in stats["by_source"][:10]])
    by_mall = "\n".join([f"- {mall}: {cnt}건" for mall, cnt in stats["by_mall"][:15]])

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    prompt = f'''
아래는 최근 수집된 패션 상품 데이터입니다.

[전체 수집 개수]
{stats["total"]}건

[소스별 개수]
{by_source}

[몰별 개수]
{by_mall}

[최근 상품명]
{"\n".join(names)}

위 데이터를 바탕으로 한국어로 아래 형식에 맞춰 정리해 주세요.

1. 핵심 키워드 7개
2. 반복되는 스타일/핏/소재 특징
3. 가격대 해석
4. 경쟁사/포털 관점에서 지금 강한 포인트
5. 다음 상품기획 제안 7개
6. 상세페이지/광고카피에 바로 쓸 표현 10개

실무 MD가 바로 회의 자료에 붙여넣을 수 있게, 군더더기 없이 구체적으로 작성해 주세요.
'''
    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return res.choices[0].message.content
