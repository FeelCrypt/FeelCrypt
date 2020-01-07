# Get bitcoin price

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
    urllib.request.urlretrieve(url, 'btc.json')
    f = open('btc.json')
    data = pd.read_json(f)
    btc_csv = data.to_csv('btc.csv')
    df = pd.read_csv('btc.csv')
    df = clean_csv(df)
    btc_data = df['Data']
    btc_list = pd.Series(btc_data.iloc[0])
    btc_list = btc_list[0]
    btc_list = btc_list.replace("\'","\"")
    btc_res = json.loads(btc_list)
    btc_res = pd.DataFrame(btc_res)
    del btc_res['open']
    del btc_res['high']
    del btc_res['low']
    del btc_res['conversionSymbol']
    del btc_res['conversionType']
    del btc_res['volumefrom']
    del btc_res['volumeto']
    dates = []
    for time in btc_res['time']:
        dates.append(date.fromtimestamp(time))
    btc_res['date'] = dates
    del btc_res['time']
    btc_res = btc_res.rename(columns={"close":"priceBTC","date":"dateMidnight"})
    btc_res.to_csv(f'chart_price_{currency}.csv',index=False)
	
def clean_csv(df):
    del df['Unnamed: 0']
    del df['Message']
    del df['Type']
    del df['RateLimit']
    del df['HasWarning']
    df = df.drop([0, 2, 3])
    return df