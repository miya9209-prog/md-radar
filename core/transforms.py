import re

TAG_RE = re.compile(r"<[^>]+>")

def clean_html(text):
    if not isinstance(text, str):
        return text
    return TAG_RE.sub("", text)

def guess_category(name, keyword=""):
    src = f"{name} {keyword}".lower()
    mapping = {
        "가디건": ["가디건"],
        "블라우스": ["블라우스"],
        "티셔츠": ["티셔츠", "티셔츠", "반팔", "긴팔", "맨투맨", "후드"],
        "슬랙스": ["슬랙스", "팬츠", "바지"],
        "원피스": ["원피스"],
        "자켓": ["자켓", "재킷", "야상"],
        "니트": ["니트", "스웨터"],
        "셔츠": ["셔츠"],
    }
    for cat, words in mapping.items():
        if any(w in src for w in words):
            return cat
    return ""

def price_to_int(value):
    try:
        return int(str(value).replace(",", "").replace("원", "").strip())
    except Exception:
        return None
