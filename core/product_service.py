from collections import Counter
from core.catalog import CATEGORY_KEYWORDS
from core.naver_api import search_many
from core.transforms import clean_html, guess_category

def collect_products_by_keyword(keyword, pages=2, sort="sim"):
    items = search_many(keyword, pages=pages, display=50, sort=sort)
    rows = []
    cards = []
    for item in items:
        name = clean_html(item.get("title", ""))
        price = item.get("lprice", "")
        mall = item.get("mallName", "")
        link = item.get("link", "")
        image_url = item.get("image", "")
        category = guess_category(name, keyword)
        rows.append(("naver", keyword, category, name, price, mall, link, image_url))
        cards.append({
            "카테고리": category,
            "상품명": name,
            "가격": price,
            "몰": mall,
            "링크": link,
            "이미지": image_url,
        })
    return rows, cards

def discover_hot_categories(pages=1):
    counter = Counter()
    samples = []
    for category, keywords in CATEGORY_KEYWORDS.items():
        try:
            items = search_many(keywords[0], pages=pages, display=30, sort="sim")
        except Exception:
            items = []
        count = 0
        for item in items[:20]:
            name = clean_html(item.get("title", ""))
            price = item.get("lprice", "")
            mall = item.get("mallName", "")
            link = item.get("link", "")
            image_url = item.get("image", "")
            counter[category] += 1
            count += 1
            if len(samples) < 40:
                samples.append({
                    "카테고리": category,
                    "상품명": name,
                    "가격": price,
                    "몰": mall,
                    "링크": link,
                    "이미지": image_url,
                })
        if count == 0:
            counter[category] += 0
    ranking = [{"카테고리": k, "노출건수": v} for k, v in counter.most_common()]
    return ranking, samples
