import requests
import pandas as pd
from bs4 import BeautifulSoup
import html
import re
import random
import sys

def req_to_address(method, url, headers, params):
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
        )
        if response.status_code == 200:
            return response.content
        else:
            print("Failed to fetch the website with url:", url)
            return None
    except:
        print("Error in get request with url:", url)


def create_dict(tag="", attrs="", text="", re_pattern=""):
    return {
        "tag": tag,
        "attrs": attrs,
        "text": text,
        "re_pattern": re_pattern,
    }


div_each_item = create_dict(
    tag="div",
    attrs={"class": "panel panel-default panel-horizontal product-item change-icon"},
)

title_url_each_book = create_dict(
    tag="h4",
    attrs={"class": "product-name-title"},
)

img_url_each_book = create_dict(
    tag="a",
    attrs={"class": "product-item-link"},
)

df = pd.DataFrame(columns=["id", "title", "url", "img_url"])

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
]
headers = {
    "User-Agent": random.choice(user_agents),
    "Accept-Language": "en-US,en;q=0.9,fa;q=0.8",
}

main_url = "https://www.iranketab.ir"
# category1_url = "tag/103-fiction"
book_url = "/book?"
# page = "?Page="
maximum_number_books = 1000
page_number = 1
sum_items = 0

while True:
    query_params = {
        "pagenumber": str(page_number),
        "pagesize": str(maximum_number_books),
        "sortOrder": "date_asc",
        # "tagid": "103",
    }
    html_content = req_to_address(
        method="GET",
        url=main_url + book_url,
        headers=headers,
        params=query_params,
    )
    soup = BeautifulSoup(html_content, "html.parser")
    elements = soup.find_all(div_each_item["tag"], attrs=div_each_item["attrs"])

    cnt = 0
    for element in elements:
        img_url = element.find(
            img_url_each_book["tag"],
            attrs=img_url_each_book["attrs"],
        ).find("img")["data-src"]

        title_url = element.find(
            title_url_each_book["tag"],
            attrs=title_url_each_book["attrs"],
        ).find("a")
        if title_url:
            link = title_url["href"]
            start = link.find("/book/") + len("/book/")
            end = link.find("-")
            df.loc[len(df)] = {
                "id": link[start:end],
                "title": title_url.text.strip(),
                "url": main_url + link,
                "img_url": img_url,
            }
            cnt += 1
    sum_items += cnt
    progress = f"pagenumber {page_number} done. [{sum_items} url]"
    sys.stdout.write("\r" + progress)
    sys.stdout.flush()  
    if cnt != maximum_number_books:
        print("\nDone!")
        break
    page_number += 1
    headers["User-Agent"] = random.choice(user_agents)

df.to_csv("URL_address_books.csv", index=False, encoding="utf-8-sig")