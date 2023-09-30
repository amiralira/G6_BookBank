import requests
import random
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

data = []


def crawler(url):
    url_data = {}

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    ]
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": "en-US,en;q=0.9,fa;q=0.8",
    }

    response = requests.get(url, headers=headers)
    print("status code is: ", response.status_code)
    soup = BeautifulSoup(response.text, "html.parser")
    persian_title = soup.select_one('.product-name strong').text
    english_title = soup.select_one('div div .product-name-englishname').text
    try:
        discount = soup.select_one('.col-md-7 li:nth-child(1) div').text
    except:
        discount = 'null'
    price_despite_of_discount = soup.find('span', attrs={'class': 'price price-special'}).text

    try:
        price_without_discount = soup.find('span', attrs={'class': 'price price-broken'}).text
    except:
        price_without_discount = price_despite_of_discount
    try:
        publisher = soup.find_all('span', attrs={'class': 'prodoct-attribute-item'})[1].text
    except:
        publisher = 'null'

    try:
        publisher_link1 = soup.find('a', href=lambda href: href and href.startswith('/publisher'))['href']
        publisher_link = 'https://www.iranketab.ir' + publisher_link1
    except:
        publisher_link = "null"

    writers_div = soup.find('div', attrs={'class': 'col-xs-12 prodoct-attribute-items'})
    writers = writers_div.find_all('a', class_='prodoct-attribute-item')

    try:
        deliver_from = soup.select_one('.label-info').text.strip()
    except:
        deliver_from = 'null'
    try:
        description = soup.select_one('.product-description').text.strip()
    except:
        description = 'null'
    try:
        author_description = soup.select_one('.col-xs-9').text.strip()
    except:
        author_description = 'null'
    try:
        tags = soup.select('.product-tags-item')
        tags_list = [tag.text.strip() for tag in tags]
    except:
        tags_list = ['null']
    table = soup.find('table', class_='product-table')
    for row in table.find_all('tr'):
        row_data = [cell.text.strip() for cell in row.find_all('td')]
        if len(row_data) == 2: 
            url_data[row_data[0]] = row_data[1]

    data.append(url_data)
    return {
        'Persian Title': persian_title,
        'English Title': english_title,
        'Discount': discount,
        'Price Without Discount': price_without_discount,
        'Price Despite of Discount': price_despite_of_discount,
        'Publisher link': publisher_link,
        'Publisher': publisher,
        'Description': description,
        'Author Description': author_description,
        'Tags': tags_list,
        'URL': url,  
    }



books_url = pd.read_csv('/Users/amirosein/Desktop/untitled folder/URL_address_books.csv')
urls = books_url['url'].tolist()


total_count = len(urls)

with ThreadPoolExecutor(max_workers=20) as executor:
    results = executor.map(crawler, urls)

df = pd.DataFrame(results)
df1 = pd.DataFrame(data)

print(df)
print(df1)
