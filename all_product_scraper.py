import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import html
import re
import random
import sys
import threading
from queue import Queue


def req_to_address(method="GET", url="", headers=None, params=None):
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
            # print("Failed to fetch the website with url:", url)
            return -2
    except:
        # print("Error in request with url:", url)
        return -1


def create_soup_dict(tag=None, attrs=None, text=None, re_pattern=None):
    return {
        "tag": tag,
        "attrs": attrs,
        "text": text,
        "re_pattern": re_pattern,
    }


def find_id_name_url_from_element(soup, find_str, main_url, soup2=-1):
    if soup:
        link = soup["href"]
        start = link.find(find_str) + len(find_str)
        end = link.find("-")
        id = link[start:end]
        name = soup.text.strip()
        url = main_url + link
        return {"id": id, "name": name, "url": url}
    elif soup2 != -1 and soup2:
        return {"id": np.nan, "name": soup2.text.strip(), "url": np.nan}
    else:
        return np.nan


soup_div = create_soup_dict(
    tag="div",
    attrs={"class": "clearfix"},
)
soup_name = create_soup_dict(attrs={"class": "product-name"})
soup_eng_name = create_soup_dict(
    tag="div",
    attrs={"class": "product-name-englishname ltr"},
)
soup_price_broken = create_soup_dict(
    tag="span",
    attrs={"class": "price price-broken"},
)
soup_price = create_soup_dict(
    tag="span",
    attrs={"class": "price"},
)
soup_rating = create_soup_dict(
    tag="div",
    attrs={"class": "my-rating"},
    text=["data-rating", "title"],
)
soup_exists_book = create_soup_dict(tag="li", attrs={"class": "exists-book"})
soup_publisher_author = create_soup_dict(
    tag="div",
    attrs={"class": "col-xs-12 prodoct-attribute-items"},
)
soup_table = create_soup_dict(tag="table", attrs={"class": "product-table"})
soup_title = create_soup_dict(
    re_pattern=r"<div>\s*([\s\S]*?)\s*<\/div>",
)
soup_discount = create_soup_dict(
    re_pattern=r'<div style="float: left;font-size: 12px;line-height: 1.375;background-color: #fb3449;color: #fff;padding: 5px 30px 3px;-webkit-border-radius: 0 16px 16px 16px;border-radius: 0 16px 16px 16px;">(.*?)</div>',
)

# df = pd.DataFrame(columns=["id", "title", "url", "img_url"])

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

publisher_find_str = "/publisher/"
profile_find_str = "/profile/"
tag_find_str = "/tag/"
product_code = "کد محصول :"
book_code = "کد کتاب :"


def find_book_detail(df, element, title_element, url, tags, description):
    table_element = element.find(soup_table["tag"], attrs=soup_table["attrs"])
    table_element_rows = table_element.find("tbody").find_all("tr")
    columns = []
    data = []
    for row in table_element_rows:
        cols = row.find_all("td")
        cols = [col.get_text(strip=True) for col in cols]
        columns.append(cols[0])
        data.append(cols[1])

    temp_df = pd.DataFrame(data=[data], columns=columns)
    dict_df = pd.DataFrame(
        columns=["url", "translator", "publisher", "author", "tags", "description"]
    )
    dict_translator = []
    dict_publisher = np.nan
    dict_author = np.nan

    translator_elements = table_element.find_all("a")
    for translator_element in translator_elements:
        dict_translator.append(
            find_id_name_url_from_element(
                translator_element,
                profile_find_str,
                main_url,
            )
        )
    temp_df["name"] = title_element.text.strip()

    eng_name_element = element.find(soup_eng_name["tag"], soup_eng_name["attrs"])
    if eng_name_element:
        temp_df["eng_name"] = eng_name_element.text.strip()

    price_broken_element = element.find(
        soup_price_broken["tag"], soup_price_broken["attrs"]
    )
    price_element = element.find(soup_price["tag"], soup_price["attrs"])
    if price_broken_element:
        temp_df["price"] = price_broken_element.text.strip()
    elif price_element:
        temp_df["price"] = price_element.text.strip()

    temp_df["data_rating"] = element.find(soup_rating["tag"], soup_rating["attrs"])[
        soup_rating["text"][0]
    ].strip()
    temp_df["title_rating"] = element.find(soup_rating["tag"], soup_rating["attrs"])[
        soup_rating["text"][1]
    ].strip()

    exists_book_element = element.find(
        soup_exists_book["tag"], soup_exists_book["attrs"]
    )
    if exists_book_element:
        temp_df["exists"] = 1
    else:
        temp_df["exists"] = 0

    publisher_author_elements = element.find_all(
        soup_publisher_author["tag"],
        soup_publisher_author["attrs"],
    )
    if len(publisher_author_elements) > 0:
        dict_publisher = find_id_name_url_from_element(
            publisher_author_elements[0].find("a"),
            publisher_find_str,
            main_url,
            publisher_author_elements[0].find("span", attrs={"itemprop": "name"}),
        )
    if len(publisher_author_elements) > 1:
        dict_author = find_id_name_url_from_element(
            publisher_author_elements[1].find("a"),
            profile_find_str,
            main_url,
            publisher_author_elements[1].find("span", attrs={"itemprop": "name"}),
        )
    str_element = str(element)
    title_match = re.search(soup_title["re_pattern"], str_element)
    if title_match and title_match.group(1).strip() != "":
        temp_df["title"] = title_match.group(1).strip()

    discount_match = re.search(soup_discount["re_pattern"], str_element)
    if discount_match:
        temp_df["discount"] = discount_match.group(1).strip()

    dict_df.loc[len(dict_df)] = {
        "url": url,
        "translator": dict_translator,
        "publisher": dict_publisher,
        "author": dict_author,
        "tags": tags,
        "description": description,
    }
    result = pd.concat([temp_df, dict_df], axis=1)
    if df is None:
        df = result
    else:
        df = pd.concat([df, result], ignore_index=True)
    return df


def add_err_df(df, code, url):
    df.loc[len(df)] = {
        "err_code": code,
        "url": url,
    }
    return df


def crawl_url(url):
    global final_df
    global err_df
    global cnt_completed
    global cnt_err
    global cnt_product

    df = None
    html_content = req_to_address(
        method="GET",
        url=url,
        headers=headers,
    )
    if html_content == -1:
        with cnt_err_lock:
            cnt_err += 1
        with err_df_lock:
            add_err_df(err_df, -1, url)
    elif html_content == -2:
        with cnt_err_lock:
            cnt_err += 1
        with err_df_lock:
            add_err_df(err_df, -2, url)
    else:
        soup = BeautifulSoup(html_content, "html.parser")

        description_element = soup.find("div", attrs={"class": "product-description"})
        description = np.nan
        if description_element:
            description = description_element.text.strip()

        tag_elements = soup.find("div", attrs={"class": "product-tags"}).find_all("a")
        tags = []
        for tag_element in tag_elements:
            tags.append(
                find_id_name_url_from_element(
                    tag_element,
                    tag_find_str,
                    main_url,
                )
            )

        elements = soup.find_all(soup_div["tag"], attrs=soup_div["attrs"])
        for element in elements:
            title_element = element.find(attrs=soup_name["attrs"])
            if title_element:
                try:
                    df = find_book_detail(
                        df, element, title_element, url, tags, description
                    )
                    with cnt_product_lock:
                        cnt_product += 1
                except:
                    print("\n[-3] Error in find element with url:", url)
                    with err_df_lock:
                        add_err_df(err_df, -3, url)
                    # raise
        code_col = ""
        if product_code in df.columns:
            code_col = product_code
        elif book_code in df.columns:
            code_col = book_code
        try:
            df.drop_duplicates(subset=code_col, keep="first", inplace=True)
            with cnt_product_lock:
                cnt_product -= 1
        except:
            print("\n[-4] ", url)
            with err_df_lock:
                add_err_df(err_df, -4, url)

        with final_df_lock:
            final_df = pd.concat([final_df, df], ignore_index=True)
        with cnt_completed_lock:
            cnt_completed += 1

    headers["User-Agent"] = random.choice(user_agents)
    progress_completed = f"{cnt_completed} / {len(urls)} requests were completed."
    progress_err = f"{cnt_err} request errors!"
    sys.stdout.write("\r" + progress_completed + "\t" + progress_err)
    sys.stdout.flush()


def crawl_batch_url(batch_urls):
    for url in batch_urls:
        crawl_url(url)


def split_list_into_batches(lst, batch_size):
    for i in range(0, len(lst), batch_size):
        yield lst[i : i + batch_size]


def read_file(f_name, err=-1):
    try:
        return pd.read_csv(f_name, encoding="utf-8-sig")
    except:
        print("err", f_name)
        if err != -1:
            return pd.DataFrame(columns=["err_code", "url"])
        return None


final_df_lock = threading.Lock()
err_df_lock = threading.Lock()
cnt_completed_lock = threading.Lock()
cnt_err_lock = threading.Lock()
cnt_product_lock = threading.Lock()

file_name = "all_product_details(p0).csv"
err_file_name = "err_url.csv"

final_df = read_file(file_name)
err_df = read_file(err_file_name, 1)
cnt_completed = 0
cnt_err = 0
cnt_product = 0

df_urls = pd.read_csv("URL_address_books.csv")
# df_urls = pd.read_csv("err_url.csv")
urls = df_urls["url"][0:10000]

url_batches = list(split_list_into_batches(urls, 500))
threads = []
for batch in url_batches:
    thread = threading.Thread(target=crawl_batch_url, args=(batch,))
    threads.append(thread)
    thread.start()
for thread in threads:
    thread.join()

# with ThreadPoolExecutor(max_workers=20) as executor:
#     executor.map(crawl_url, urls)

final_df.to_csv(file_name, index=False, encoding="utf-8-sig")
err_df.to_csv(err_file_name, index=False, encoding="utf-8-sig")

print(f"\n{cnt_product} Done!")