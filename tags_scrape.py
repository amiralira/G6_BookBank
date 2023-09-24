# this code fetches all the tag names in english and persian with their id and  saves them into a csv file

import requests
import random
from bs4 import BeautifulSoup
import pandas as pd

# fake user agents list
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; Redmi Note 9 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36'
]

# fetching the data
url = "https://www.iranketab.ir/tag/284-browse-books-by-subject"
response = requests.get(url, headers={'User-Agent': random.choice(user_agents), 'Accept-Language': 'en-US,en;q=0.5'})
print('status code: ', response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
l = soup.find_all('a', class_='product-tags-item ParentTag')
tag_name_persian = []
tag_name_english = []
tag_id = []
tag_num = []
for tag in l:
    tag_name_persian.append(tag.text.strip().split('\n')[0].strip(' \r'))
    tag_num.append(tag.text.strip().split('\n')[1].strip(' \r')[1:-7])
    tag_name_english.append(tag['href'][5:].split('-')[1])
    tag_id.append(tag['href'][5:].split('-')[0])
print(tag_name_persian[1])
print(tag_num[1])
print(tag_name_english[1])
print(tag_id[1])
print(len(tag_name_persian))
print(len(tag_num))
print(len(tag_name_english))
print(len(tag_id))

tag_dict = {
    'tag_id': tag_id,
    'tag_name_english': tag_name_english,
    'tag_name_persian': tag_name_persian,
    'tag_num': tag_num
}
tags_df = pd.DataFrame(tag_dict)
tags_df.to_csv('tags.csv', encoding='utf-8-sig')