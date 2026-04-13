# MD 인사이트

## Streamlit Secrets
```toml
OPENAI_API_KEY = "한줄 전체키"
NAVER_CLIENT_ID = "..."
NAVER_CLIENT_SECRET = "..."
```

## 실행
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 구조
- 키워드 RADAR: 일간/주간/월간 트렌드 요약 + 직접 검색
- 상품 RADAR: 핫 카테고리 + 썸네일 + 상품 검색
- 경쟁사 RADAR: 키워드 방식 / 전체 탐색 방식
- MD 인사이트: DB 기반 GPT 분석
- 매출형 상품기획: GPT 기반 상품기획서 생성
