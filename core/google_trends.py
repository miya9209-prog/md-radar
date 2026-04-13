from pytrends.request import TrendReq

def get_trends(keyword):
    pytrends = TrendReq(hl="ko-KR", tz=540)
    pytrends.build_payload([keyword], timeframe="today 3-m")
    return pytrends.interest_over_time()
