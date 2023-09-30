import requests
from bs4 import BeautifulSoup as bf
import pandas as pd
import concurrent.futures

def fetch_data(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'Accept-Language': 'fa-IR,fa;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        page = requests.get(url, headers=headers)
        soup = bf(page.content, 'html.parser')
        name = soup.find('h1', attrs={'class': 'text-center'}).text.strip() if soup.find('h1', attrs={'class': 'text-center'}) else "null"
        Information = soup.find('h5').text.strip() if soup.find('h5') else "No Information"
        print(name)
        return {'name': name, 'Information': Information, 'URL': url}
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        return {'name': "null", 'Information': "No Information", 'URL': url}

if __name__ == '__main__':
    df = pd.read_excel(pd.ExcelFile('D:\python\data_q\pro1\profile.xlsx'), 'profile')
    p = list(df["urls"])

    df_result = pd.DataFrame({'name': [], 'Information': [], 'URL': []})
    number = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:  # Adjust max_workers as needed
        results = list(executor.map(fetch_data, p))

    df_result = df_result.append(results, ignore_index=True)
    df_result.to_csv('profile.csv', index=False)
