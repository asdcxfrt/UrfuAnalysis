import concurrent.futures
from fake_useragent import UserAgent
import time
#import requests
import requests
import pandas as pd
import arrow
ua = UserAgent()
print(ua.chrome)
header = {'User-Agent':str(ua.chrome)}
Numbers=list(range(1,33+1))
MAX_THREADS = 30
rez=[]

def download_url(id):
    global rez

    MainURL=f"https://urfu.ru/api/ratings/info/27/{id}/"
    resp1 = requests.get(MainURL,headers=header)

    print(resp1)
    if ("Not Found" not in resp1.text) and resp1.text:
        url=resp1.json()["url"]
        url="https://urfu.ru/{0}".format(url)

        resp2 = requests.get(url,headers=header)
        resp2.encoding = 'utf-8'

        html=resp2.text
        if html:
            df_list = pd.read_html(html,header =0)
            df = df_list[-1]

            rez.append(df)
            print(f"End {id}")


def download_stories(IDs):
    threads = min(MAX_THREADS, len(IDs))

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(download_url, IDs)

def main(Numbers):
    t0 = time.time()
    download_stories(Numbers)
    t1 = time.time()
    print(f"{t1-t0} seconds to download {len(Numbers)} stories.")
main(Numbers)
print(rez)
result = pd.concat(rez)

Date=arrow.now().format('DD-MM-YYYY_HH-mm-ss')
result.to_csv(f'Data/dataURFU_{Date}.csv', index = False, encoding='utf-8')
