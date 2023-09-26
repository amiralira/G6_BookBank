from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def categorize_type(url):
    if 'tag' in url:
        return 'book'
    elif 'blog' in url:
        return 'blog'
    elif 'profile' in url:
        return 'profile'
    elif 'publisher' in url:
        return 'publisher'
    else:
        return 'other'
    
def find_names(url):
    n=url.split("/")[4].find('-')
    if "blog"  in url:
        return url.split("/")[4]
    return url.split("/")[4][n+1:]
    

with open('iranketab.ir_sitemap.xml', 'r') as f:
    data = f.read()
Bs_data = BeautifulSoup(data, "xml")
b_unique = list(Bs_data.find_all('loc'))
print(len(b_unique))


df=pd.DataFrame({'urls':b_unique})
df['urls'] = df['urls'].apply(lambda x: x.text)

df['type'] = df['urls'].apply(categorize_type)
df['names'] = df['urls'].apply(find_names)
type_counts = df['type'].value_counts()
print(type_counts) 
dfdub=df[df['names'].duplicated()]
df.to_excel('urls_name.xlsx', sheet_name='urls_name')
dfdub.to_excel('duplicated.xlsx', sheet_name='duplicated')