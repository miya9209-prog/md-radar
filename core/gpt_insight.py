import os
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
from utils.db import get_conn

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_insight():
    conn = get_conn()
    df = pd.read_sql("SELECT name FROM products LIMIT 50", conn)
    text_data = "\n".join(df["name"].tolist())

    prompt = f"""
아래 상품 데이터를 분석해서
키워드, 트렌드, 상품기획 방향을 정리해줘:

{text_data}
"""

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content
