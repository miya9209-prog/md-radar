# MD 레이다

## Streamlit Secrets 예시
```toml
OPENAI_API_KEY = "sk-..."
NAVER_CLIENT_ID = "..."
NAVER_CLIENT_SECRET = "..."
```

## 실행
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 참고
- Streamlit Cloud에서 소스 디렉터리는 쓰기 제한이 있을 수 있어 DB는 사용자 홈의 `.md_radar_data` 아래에 저장됩니다.
- 경쟁사 크롤러는 현재 2개 샘플 구조입니다.
