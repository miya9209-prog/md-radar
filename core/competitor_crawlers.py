
import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0"}

sites = [
    ("조아맘", "https://www.joamom.co.kr/product/list.html?cate_no=24"),
    ("캔마트", "https://canmart.co.kr/product/list.html?cate_no=28"),
]

def crawl_site(name, url):
    res = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")

    items = []
    for p in soup.select(".prdList li"):
        try:
            name_text = p.select_one(".name").text.strip()
            price = p.select_one(".price").text.strip()
            link = p.select_one("a")["href"]

            items.append({
                "site": name,
                "name": name_text,
                "price": price,
                "link": link
            })
        except:
            continue

    return items

def run_all_crawlers():
    data = []
    for name, url in sites:
        try:
            data += crawl_site(name, url)
        except:
            continue
    return data
