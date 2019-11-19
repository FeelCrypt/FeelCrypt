# -*- coding: utf-8 -*-


# -- ==user_accounts== --
import collections
from os import listdir
import pandas as pd
import os

def get_labeled_bitcoin_price():
    df_bitcoin_values = pd.read_csv("../Data/Bitcoin_Price/chart_price_BTC.csv")
    
    length = len(df_bitcoin_values)
    data = {} 

    for index in range(1,length):
        value = float(df_bitcoin_values["priceBTC"][index]) - float(df_bitcoin_values["priceBTC"][index - 1])
        data[df_bitcoin_values["dateMidnight"][index][0:10]] = 1 if value > 0 else 0
    
    return data

def get_labeled_dataset(number_of_file = 0, from_date = "2010-01-01", date_included = True, all_files = False):
    
    limit_year = 2021
    dataset = {"text" : [], "label" : [], "date" : []}
    directory = "../Data/Reddit_Data/"
    max_number_of_files_number = len(os.listdir(directory))
    
    if all_files:
        from_date = "2010-01-01"
        number_of_file = max_number_of_files_number
    
    count = 0
    
    max_number_of_files_number = len(os.listdir(directory))
    year =  int(from_date[0:4])
    month = int(from_date[5:7])
    day = int(from_date[8:10]) + (0 if date_included else 1)
    bictoin_price_dict = get_labeled_bitcoin_price()
    
    number_of_file = max_number_of_files_number if number_of_file > max_number_of_files_number else number_of_file

    while (count < number_of_file and year < limit_year and not all_files) or (all_files and count < number_of_file):
        month_string = month if month >= 10 else f"0{month}"
        day_string = day if day >= 10 else f"0{day}"
        
        date = f"{year}-{month_string}-{day_string}"
        file = f"{directory}{date}.csv"
       
        if os.path.exists(file) and date in bictoin_price_dict.keys():
            label = bictoin_price_dict[date]
            df = pd.read_csv(file, sep=";", header=None)
            
            dataset["text"].extend(list(map(lambda s : str(s), df[0])))
            dataset["label"].extend([label for i in df[0]])
            dataset["date"].extend([date for i in df[0]])
            count += 1
            
        day += 1
        if day > 31:
            day = 1
            month += 1
            
        if month > 12:
            month = 1
            year += 1
    print("Number of files loaded : ", count)
    return pd.DataFrame(dataset)

def get_prediction_stats(df_prediction):
    counter_correct_preds = collections.Counter(df_prediction["correct"])
    correct_pred = counter_correct_preds[True]
    wrong_pred = counter_correct_preds[False]
    
    print(f"""Number Correct/Wrong Guess : {correct_pred}/{wrong_pred}
              Accuracy : {(correct_pred/(correct_pred + wrong_pred)) * 100}""" )
    print("Invalid sentences count", collections.Counter(df_prediction["preds"])[-1])

# -- ==user_accounts== --