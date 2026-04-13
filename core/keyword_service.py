import time
from core.catalog import TREND_SEED_KEYWORDS
from core.google_trends import get_interest_for_keywords

def safe_get_interest(chunk, timeframe="today 3-m", retries=3):
    last_error = None
    for attempt in range(retries):
        try:
            return get_interest_for_keywords(chunk, timeframe=timeframe)
        except Exception as e:
            last_error = e
            if "429" in str(e):
                wait_time = 8 * (attempt + 1)
                time.sleep(wait_time)
            else:
                raise
    raise RuntimeError(f"Google Trends 재시도 실패: {last_error}")

def build_keyword_rankings():
    seeds = TREND_SEED_KEYWORDS[:]
    chunk_size = 3
    daily_scores = {}
    weekly_scores = {}
    monthly_scores = {}
    failed_chunks = []

    for i in range(0, len(seeds), chunk_size):
        chunk = seeds[i:i + chunk_size]
        try:
            df = safe_get_interest(chunk, timeframe="today 3-m")
            if df.empty:
                continue
            for kw in chunk:
                if kw not in df.columns:
                    continue
                series = df[kw].fillna(0)
                daily_scores[kw] = float(series.tail(7).mean())
                weekly_scores[kw] = float(series.tail(28).mean())
                monthly_scores[kw] = float(series.mean())
        except Exception as e:
            failed_chunks.append((chunk, str(e)))
            continue

    return {
        "daily": sorted(daily_scores.items(), key=lambda x: x[1], reverse=True),
        "weekly": sorted(weekly_scores.items(), key=lambda x: x[1], reverse=True),
        "monthly": sorted(monthly_scores.items(), key=lambda x: x[1], reverse=True),
        "failed": failed_chunks,
    }
