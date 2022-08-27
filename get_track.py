import urllib3
import pandas as pd
from datetime import datetime, timedelta
import json
import os

# https://solarorbiter.esac.esa.int/where/
url = "https://solarorbiter.esac.esa.int/where/assets/scenarios/solar_solar_cruise.json"


if __name__=="__main__":
    # data = pd.DataFrame(columns=['Date', 'positions'])
    filename = os.path.join(os.getcwd(), 'data', 'ToSun.csv')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }
    http = urllib3.PoolManager()
    r = http.request(
        'GET',
        url,
        headers=headers,
    )
    data = json.loads(r.data)
    df = pd.DataFrame(data["spacecraft"]["positions"], columns=['x','y','z'])
    df['ToSun'] = (df['x']**2 + df['y']**2 + df['z']**2)**(0.5)
    day = datetime(2020,2,10)
    date_list = [day + timedelta(days=x) for x in range(3400)]
    df2 = pd.DataFrame(date_list, columns=['Date'])
    df = pd.concat([df2, df], axis=1)
    df.to_csv(os.path.join(os.getcwd(), 'data', 'ToSun.csv'), index=False)
    print(df)


        # 위성 위치
        # data["spacecraft"]["positions"]
        # 시작 날짜
        # data["spacecraft"]["startutc"]
        # '2020-02-10T05:03:00Z'