from core.naver_api import search_many
from core.transforms import clean_html, guess_category
from core.competitor_sources import COMPETITOR_ALIASES, DEFAULT_KEYWORDS

def _match_alias(mall_name, selected_malls):
    mall_name = (mall_name or "").strip().lower()
    matched = None
    for mall in selected_malls:
        aliases = COMPETITOR_ALIASES.get(mall, [mall])
        for alias in aliases:
            if alias.lower() in mall_name:
                return mall
    return matched

def collect_by_keyword(keyword, selected_malls, pages=2, sort="sim"):
    raw_items = search_many(keyword, pages=pages, display=50, sort=sort)
    rows, cards, seen = [], [], set()
    for item in raw_items:
        mall_name = item.get("mallName", "")
        matched_mall = _match_alias(mall_name, selected_malls)
        if not matched_mall:
            continue
        name = clean_html(item.get("title", ""))
        price = item.get("lprice", "")
        link = item.get("link", "")
        image_url = item.get("image", "")
        category = guess_category(name, keyword)
        dedupe = (matched_mall, name, price, link)
        if dedupe in seen:
            continue
        seen.add(dedupe)
        rows.append(("competitor_naver", keyword, category, name, price, matched_mall, link, image_url))
        cards.append({
            "몰": matched_mall,
            "카테고리": category,
            "상품명": name,
            "가격": price,
            "키워드": keyword,
            "링크": link,
            "이미지": image_url,
        })
    return rows, cards

def collect_all_mode(selected_malls, pages=1, sort="sim"):
    merged_rows, merged_cards = [], []
    seen = set()
    for keyword in DEFAULT_KEYWORDS:
        rows, cards = collect_by_keyword(keyword, selected_malls, pages=pages, sort=sort)
        for row, card in zip(rows, cards):
            dedupe = (row[5], row[3], row[4], row[6])
            if dedupe in seen:
                continue
            seen.add(dedupe)
            merged_rows.append(row)
            merged_cards.append(card)
    return merged_rows, merged_cards
