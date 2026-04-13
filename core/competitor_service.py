from core.naver_api import search_many
from core.transforms import clean_html, guess_category
from core.competitor_sources import DEFAULT_KEYWORDS

def _query_for_mall(mall, keyword, pages=2, sort="sim"):
    query = f"{mall} {keyword}"
    items = search_many(query, pages=pages, display=50, sort=sort)
    rows = []
    cards = []
    seen = set()

    for item in items:
        name = clean_html(item.get("title", ""))
        price = item.get("lprice", "")
        link = item.get("link", "")
        image_url = item.get("image", "")
        category = guess_category(name, keyword)
        dedupe = (mall, name, price, link)
        if dedupe in seen:
            continue
        seen.add(dedupe)
        rows.append(("competitor_naver", keyword, category, name, price, mall, link, image_url))
        cards.append({
            "이미지": image_url,
            "몰": mall,
            "상품명": name,
            "카테고리": category,
            "가격": price,
            "키워드": keyword,
            "링크": link,
        })
    return rows, cards

def collect_by_keyword(keyword, selected_malls, pages=2, sort="sim"):
    merged_rows = []
    merged_cards = []
    for mall in selected_malls:
        rows, cards = _query_for_mall(mall=mall, keyword=keyword, pages=pages, sort=sort)
        merged_rows.extend(rows)
        merged_cards.extend(cards)
    return merged_rows, merged_cards

def collect_all_mode(selected_malls, pages=1, sort="sim"):
    merged_rows = []
    merged_cards = []
    for keyword in DEFAULT_KEYWORDS:
        rows, cards = collect_by_keyword(keyword=keyword, selected_malls=selected_malls, pages=pages, sort=sort)
        merged_rows.extend(rows)
        merged_cards.extend(cards)
    return merged_rows, merged_cards
