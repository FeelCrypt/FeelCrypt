# get bitcoin price in csv format

import requests
import json
import csv
import pandas as pd
import time as t
import urllib.request
from datetime import date

def get_csv_crypto_prices(currency="BTC"):
    currentTimeStamp = int(t.time())
    url=f'https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=USD&allData=true'
    btc_json = requests.get(url).json()
    btc_json_data = btc_json['Data']['Data']
    for i in range(len(btc_json_data)):
        del btc_json_data[i]['open']
        del btc_json_data[i]['high']
        del btc_json_data[i]['low']
        del btc_json_data[i]['conversionSymbol']
        del btc_json_data[i]['conversionType']
        del btc_json_data[i]['volumefrom']
        del btc_json_data[i]['volumeto']
    df_btc = pd.DataFrame.from_dict(btc_json_data)
    dates = []
    for i in range(len(btc_json_data)):
        dates.append(date.fromtimestamp(btc_json_data[i]['time']))
    df_btc['dateMidnight'] = dates
    del df_btc['time']
    df_btc = df_btc.rename(columns={"close":"priceBTC"})
    df_btc.to_csv(f'chart_price_{currency}.csv',index=False)