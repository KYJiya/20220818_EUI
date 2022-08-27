import os
import wget
import urllib3
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

def makedirs(directory): 
    try: 
        os.makedirs(directory) 
    except OSError: 
        if not os.path.isdir(directory): 
            raise   


def open_url(data, headers):
    url_requests = []
    for index, row in tqdm(data[data['check'] == 0].iterrows(), total=data[data['check'] == 0].shape[0]):
        http = urllib3.PoolManager()
        r = http.request(
            'GET',
            row['url'],
            headers=headers,
        )
        data['check'][index] = 1
        url_requests.append(r)

    return url_requests


def file_download(url, filename, headers):
    http = urllib3.PoolManager()
    r = http.request(
        'GET',
        url,
        headers=headers,
        preload_content=False,
    )

    with open(filename, 'wb') as out:
        out.write(r.read())



def url_loop(url_requests, keyword, file, headers):
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
            
            # or function
            # if any(ext in tag.text for ext in keyword):
            # and function
            if all(ext in tag.text for ext in keyword):
                # 밑의 주석을 해제하면 다운로드를 시작함
                file_download(
                    url_request._request_url+tag.text,
                    os.path.join(os.getcwd(), 'data', tag.text),
                    headers,
                )
                file.write(url_request._request_url+tag.text+'\n')
        
    return sub_pages


if __name__=="__main__":    

    id = os.environ.get('id')
    pw = os.environ.get('pw')
    headers = urllib3.make_headers(basic_auth=id+":"+pw)
    # data = pd.DataFrame([['https://www.sidc.be/EUI/data/L1/', 0]], columns = ['url', 'check'])
    data = pd.DataFrame([['https://www.sidc.be/EUI/data_internal/L1/2022', 0]], columns = ['url', 'check'])
    keyword = ['hrieuv174', 'image']
    index_file = os.path.join(os.getcwd(), 'data/category/index.txt')

    makedirs('data/category')
    
    if os.path.isfile(index_file):
        file = open(index_file, "r")
        lines = file.readlines()
        for line in tqdm(lines):
            line = line.strip()
            # 밑의 주석을 해제하면 다운로드를 시작함
            file_download(
                line,
                os.path.join(os.getcwd(), 'data', os.path.basename(line)),
                headers,
            )
    else:
        file = open(index_file, "w")
        while 0 in data['check'].values:
            url_requests = open_url(data, headers)
            temp = url_loop(url_requests, keyword, file, headers)
            data = pd.concat([data, temp], ignore_index=True)

    file.close()
    