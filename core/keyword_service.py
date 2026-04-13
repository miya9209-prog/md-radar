import pandas as pd
from core.catalog import TREND_SEED_KEYWORDS
from core.google_trends import get_interest_for_keywords

def build_keyword_rankings():
    seeds = TREND_SEED_KEYWORDS[:]
    chunk_size = 5
    daily_scores = {}
    weekly_scores = {}
    monthly_scores = {}

    for i in range(0, len(seeds), chunk_size):
        chunk = seeds[i:i+chunk_size]
        try:
            df = get_interest_for_keywords(chunk, timeframe="today 3-m")
            if df.empty:
                continue
            for kw in chunk:
                series = df[kw].fillna(0)
                daily_scores[kw] = float(series.tail(7).mean())
                weekly_scores[kw] = float(series.tail(28).mean())
                monthly_scores[kw] = float(series.mean())
        except Exception:
            continue

    daily = sorted(daily_scores.items(), key=lambda x: x[1], reverse=True)
    weekly = sorted(weekly_scores.items(), key=lambda x: x[1], reverse=True)
    monthly = sorted(monthly_scores.items(), key=lambda x: x[1], reverse=True)
    return {"daily": daily, "weekly": weekly, "monthly": monthly}
