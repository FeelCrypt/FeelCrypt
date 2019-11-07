# -*- coding: utf-8 -*-


# -- ==user_accounts== --
import pandas as pd
def get_labeled_bitcoin_price():
    df_bitcoin_values = pd.read_csv("./csv/chart_price_bitcoin.csv")
    df_bitcoin_values = df_bitcoin_values.drop("time", 1)
    
    length = len(df_bitcoin_values)
    data = {'date': [], 
            'label': []} 

    for index in range(1,length):
        value = float(df_bitcoin_values["priceUsd"][index]) - float(df_bitcoin_values["priceUsd"][index - 1])
        data["date"].append(df_bitcoin_values["date"][index][0:10])
        data["label"].append(1 if value > 0 else 0)
    return pd.DataFrame(data)

def get_labeled_dataset(file = "scrapping_BTC_comments_sorted"):
    df_reddit = pd.read_csv(f"./csv/{file}.csv", sep=";")
    df_bictoin_price = get_labeled_bitcoin_price()
    
    data_training = {
        "text" : [],
        "label" : []
    }

    for i in range(len(df_reddit)):
        date_reddit = df_reddit["date"][i]
        for j in range(len(df_bictoin_price)):
            date_bitcoin = df_bictoin_price["date"][j]
            if date_reddit == date_bitcoin:
                data_training["text"].append(df_reddit["body"][i])
                data_training["label"].append(df_bictoin_price["label"][j])
    return pd.DataFrame(data_training)

# -- ==user_accounts== --