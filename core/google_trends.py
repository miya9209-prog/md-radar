from pytrends.request import TrendReq

def get_trends(keyword, timeframe="today 3-m"):
    pytrends = TrendReq(hl="ko-KR", tz=540)
    pytrends.build_payload([keyword], timeframe=timeframe)
    return pytrends.interest_over_time()

def get_interest_for_keywords(keywords, timeframe="today 1-m"):
    pytrends = TrendReq(hl="ko-KR", tz=540)
    pytrends.build_payload(keywords, timeframe=timeframe)
    return pytrends.interest_over_time()
