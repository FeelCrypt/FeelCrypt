import collections
from os import listdir
import pandas as pd
import os
import moment

values_prct = [-2, -5, 5, 2]

def get_multi_class_label():
    df_bitcoin_values = pd.read_csv("./chart_price_BTC.csv")
    
    length = len(df_bitcoin_values)
    data = {} 
    
    for index in range(1,length):
        price_today = float(df_bitcoin_values["priceBTC"][index])
        price_yesterday = float(df_bitcoin_values["priceBTC"][index - 1])
        prct = ((price_today - price_yesterday) / price_yesterday) * 100
        
        label = 1
        
        if values_prct[0]  < prct :
            label = 1
        if values_prct[0]  < prct and prct <= values_prct[1]:
            label = 2
        if values_prct[1] < prct and prct <=  values_prct[2]: 
            label = 3
        if  values_prct[2] < prct and prct <= values_prct[3]:
            label = 4
        if  values_prct[3] < prct :
            label = 5
        
        data[df_bitcoin_values["dateMidnight"][index - 1][0:10]] = label
    
    return data

def get_labeled_bitcoin_price():
    df_bitcoin_values = pd.read_csv("./chart_price_BTC.csv")

    length = len(df_bitcoin_values)
    data = {} 

    for index in range(1,length):
        value = float(df_bitcoin_values["priceBTC"][index]) - float(df_bitcoin_values["priceBTC"][index - 1])
        data[df_bitcoin_values["dateMidnight"][index - 1][0:10]] = 1 if value > 0 else 0
    
    return data

def get_text_labeled_dataset(from_date, to_date, binary = True):
    
    dataset = {"text" : [], "label" : []}
    directory = "../../Data/Reddit_Data/btc/comments/"
    
    bictoin_price_dict = get_labeled_bitcoin_price() if binary else get_multi_class_label()
   
    current_date = moment.date(from_date)


    from_date = moment.date(from_date)
    to_date = moment.date(to_date)

    while (current_date < to_date):
        date = current_date.format('YYYY-MM-DD')
        file = f"{directory}{date}.csv"
       
        if os.path.exists(file) and date in bictoin_price_dict.keys():
            label = bictoin_price_dict[date]
            df = pd.read_csv(file, sep=";")
            df["body"] = [str(x) for x in df["body"]]
               
            dataset["text"].extend(df["body"])
            dataset["label"].extend([label for i in df["body"]])
          
        current_date.add(day=1)
        
    return pd.DataFrame(dataset)

def get_date_labeled_dataset(from_date, to_date, binary = True):
    dataset = {"label" : [], "year" : [], "month" : [], "day" : [], "label_m1" : [], "label_m2" : []}
    
    bictoin_price_dict = get_labeled_bitcoin_price() if binary else get_multi_class_label()
    current_date = moment.date(from_date)
    
    label_m1 = bictoin_price_dict[moment.date(from_date).add(day=-1).format("YYYY-MM-DD")]
    label_m2 = bictoin_price_dict[moment.date(from_date).add(day=-2).format("YYYY-MM-DD")]

    from_date = moment.date(from_date)
    to_date = moment.date(to_date)

    while (current_date < to_date):
        
        date = current_date.format('YYYY-MM-DD')
       
        label = bictoin_price_dict[date]
            
        dataset["label"].append(label)
        dataset["year"] = int(str(date)[0:4])
        dataset["month"] = int(str(date)[5:7])
        dataset["day"] = int(str(date)[8:10])
        dataset["label_m2"].append(label_m2)
        dataset["label_m1"].append(label_m1)
    
        label_m2 = label_m1
        label_m1 = label
        current_date.add(day=1)
        
    return pd.DataFrame(dataset)

def read_today_data(threads):
    dataset = {"text" : []}
    
    date_now =  moment.now().format("YYYY-MM-DD")
    for thread in threads:
        file = f"./{thread}/comments/{date_now}.csv"
        if os.path.exists(file):
            df = pd.read_csv(file, sep=";")
            df["body"] = [str(x) for x in df["body"]]
            dataset["text"].extend(df["body"])
    return pd.DataFrame(dataset)