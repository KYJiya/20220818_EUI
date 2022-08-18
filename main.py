import os
import wget
import urllib3
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup


def makedirs(directory): 
    try: 
        os.makedirs(directory) 
    except OSError: 
        if not os.path.isdir(directory): 
            raise   


def open_url(data):
    url_requests = []
    for index, row in tqdm(data[data['check'] == 0].iterrows(), total=data[data['check'] == 0].shape[0]):
        http = urllib3.PoolManager()
        r = http.request(
            'GET',
            row['url'],
        )
        data['check'][index] = 1
        url_requests.append(r)

    return url_requests


def url_loop(url_requests, keyword, file):
    sub_pages = pd.DataFrame(columns = ['url', 'check'])
    for url_request in tqdm(url_requests, leave=False):
        soup = BeautifulSoup(url_request.data, 'lxml')
        for tag in tqdm(soup.find_all('a')[5:], leave=False):
            if '/' in tag.text:
                sub_pages = pd.concat([sub_pages,
                    pd.DataFrame(
                        [[url_request._request_url+tag.text, 0]], 
                        columns = ['url', 'check'],                         
                    )],
                    ignore_index=True
                )

            if keyword in tag.text:
                # wget.download(
                #     url_request._request_url+tag.text, 
                #     out=os.path.join(os.getcwd(), 'data', tag.text)
                # )
                file.write(url_request._request_url+tag.text+'\n')
        
    return sub_pages


if __name__=="__main__":    

    data = pd.DataFrame([['https://www.sidc.be/EUI/data/L1/', 0]], columns = ['url', 'check'])
    keyword = 'hrieuv174'
    index_file = os.path.join(os.getcwd(), 'data/category/index.txt')

    makedirs('data/category')

    if os.path.isfile(index_file):
        file = open(index_file, "r")
        lines = file.readlines()
        for line in tqdm(lines):
            line = line.strip()
            wget.download(
                line, 
                out=os.path.join(os.getcwd(), 'data', os.path.basename(line))
            )
    else:
        file = open(index_file, "w")
        while 0 in data['check'].values:
            url_requests = open_url(data)
            temp= url_loop(url_requests, keyword, file)
            data = pd.concat([data, temp], ignore_index=True)

    file.close()
    