import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import pandas as pd
import numpy as np
import geopandas as gpd
import json
import tqdm
import datetime
import time

# read lat_lon.csv
lat_lon = pd.read_csv(r'C:\Users\WeilunShi\OneDrive - CGIAR\Desktop\Food Crisis and Insecurity\lat_lon.csv')

def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session



# create a new df to store the data
result = pd.DataFrame(columns=['date', 'lat', 'lon', 'precipitation_sum', 'precipitation_sum_sd'])

# loop through each lat and lon
for i in tqdm.tqdm(range(len(lat_lon))):
    # request the data from the API
    url = 'https://archive-api.open-meteo.com/v1/archive?latitude=' + str(lat_lon['lat_round'][i]) + '&longitude=' + str(lat_lon['lon_round'][i]) + '&start_date=2017-01-01&end_date=2022-12-31&models=era5&daily=precipitation_sum&timezone=America%2FNew_York'
    try:
        response = requests_retry_session().get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
    data = response.json()
    # create a new df to store the data
    df = pd.DataFrame(columns=['date', 'lat', 'lon', 'precipitation_sum'])
    # extract time and temperature_2m_mean from the json file
    df['date'] = data['daily']['time']
    df['precipitation_sum'] = data['daily']['precipitation_sum']
    df['lat'] = lat_lon['lat'][i]
    df['lon'] = lat_lon['lon'][i]
    # convert date to datetime
    df['date'] = pd.to_datetime(df['date'])
    # calculate montely average and sd
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['month_year'] = df['month'].astype(str) + '-' + df['year'].astype(str)
    df['month_year'] = pd.to_datetime(df['month_year'])
    df['month_year'] = df['month_year'].dt.strftime('%Y-%m')
    df = df.groupby(['month_year', 'lat', 'lon']).agg({'precipitation_sum': ['mean', 'std']}).reset_index()
    df.columns = ['month_year', 'lat', 'lon', 'precipitation_sum', 'precipitation_sum_sd']
    # rename month_year to date
    df = df.rename(columns={'month_year': 'date'})
    # concat the data
    result = pd.concat([result, df], axis=0)
    # sleep for 1 second
    time.sleep(1)

# save the data
result.to_csv(r'C:\Users\WeilunShi\OneDrive - CGIAR\Desktop\Food Crisis and Insecurity\precipitation_sum.csv', index=False)
