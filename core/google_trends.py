from pytrends.request import TrendReq

pytrends = TrendReq()

def get_trends(keyword):
    pytrends.build_payload([keyword], timeframe='today 3-m')
    return pytrends.interest_over_time()
