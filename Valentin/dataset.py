# -*- coding: utf-8 -*-


# -- ==user_accounts== --
import collections
from os import listdir
import pandas as pd
import os
import moment

values_prct = [-0.02,-0.005, 0.005, 0.02]

def get_multi_class_label(values):
    df_bitcoin_values = pd.read_csv("../Data/Bitcoin_Price/chart_price_BTC.csv")
    
    length = len(df_bitcoin_values)
    data = {} 
    
    #(prix aujourdui - prix hier / prix hier) * 100
    for index in range(1,length):
        price_today = float(df_bitcoin_values["priceBTC"][index])
        price_yesterday = float(df_bitcoin_values["priceBTC"][index - 1])
        prct = ((price_today - price_yesterday) / price_yesterday) * 100
        
        label = 1
        
        if values[0]  < prct :
            label = 1
        if values[0]  < prct and prct <= values[1]:
            label = 2
        if values[1] < prct and prct <=  values[2]: 
            label = 3
        if  values[2] < prct and prct <= values[3]:
            label = 4
        if  values[3] < prct :
            label = 5
        
        data[df_bitcoin_values["dateMidnight"][index - 1][0:10]] = label
    
    return data

def get_labeled_bitcoin_price():
    df_bitcoin_values = pd.read_csv("../Data/Bitcoin_Price/chart_price_BTC.csv")

    length = len(df_bitcoin_values)
    data = {} 

    for index in range(1,length):
        value = float(df_bitcoin_values["priceBTC"][index]) - float(df_bitcoin_values["priceBTC"][index - 1])
        label = 1
        data[df_bitcoin_values["dateMidnight"][index - 1][0:10]] = 1 if value > 0 else 0
    
    return data
    
def put_on_label_dataset(df, date_col, binary = True, values = values_prct):
    bictoin_price_dict = get_labeled_bitcoin_price() if binary else get_multi_class_label(values)
    df["label"] = [bictoin_price_dict[date] for date in df[date_col]]
    return df

def get_labeled_dataset(number_of_file = 0, from_date = "2010-01-01", date_included = True, all_files = False, group_by_date = False, binary = True, values = values_prct):
    
    limit_year = moment.now().add(years=1).year
    dataset = {"text" : [], "label" : [], "date" : [], "score" : [], "nb_replies" : [], "stickied" : [], "label_m1" : [], "label_m2" : []}
    directory = "../Data/Reddit_Data/btc/comments/"
    
    max_number_of_files_number = len(os.listdir(directory))
    
    if all_files:
        from_date = moment.date("2010-01-01")
        number_of_file = max_number_of_files_number
    
    count = 0
    number_of_file += 2
    max_number_of_files_number = len(os.listdir(directory))
    
    current_date = moment.date(from_date)
    if not date_included:
        current_date.add(day=1)
    
    
    bictoin_price_dict = get_labeled_bitcoin_price() if binary else get_multi_class_label(values)
   
    
    label_m1 = -1
    label_m2 = -1
    number_of_file = max_number_of_files_number if number_of_file > max_number_of_files_number else number_of_file

    while (count < number_of_file and current_date.year < limit_year and not all_files) or (all_files and count < number_of_file and current_date.year < limit_year):
        
        date = current_date.format('YYYY-MM-DD')
        file = f"{directory}{date}.csv"
       
        if os.path.exists(file) and date in bictoin_price_dict.keys():
            label = bictoin_price_dict[date]
            df = pd.read_csv(file, sep=";")
            df["body"] = [str(x) for x in df["body"]]
            if count == 0:
                label_m2 = label
            elif count == 1:
                label_m1 = label
            else :
                if group_by_date:
                    dataset["text"].append(" ".join(df["body"]))
                    dataset["label"].append(label)
                    dataset["date"].append(date)
                    dataset["score"].append(None)
                    dataset["nb_replies"].append(None)
                    dataset["stickied"].append(None)
                    dataset["label_m2"].append(label_m2)
                    dataset["label_m1"].append(label_m1)

                else :
                    dataset["text"].extend(df["body"])
                    dataset["label"].extend([label for i in df["body"]])
                    dataset["date"].extend([date for i in df["body"]])
                    dataset["score"].extend(df["score"])
                    dataset["nb_replies"].extend(df["nb_replies"])
                    dataset["stickied"].extend(df["stickied"])
                    dataset["label_m2"].extend([label_m2 for i in df["body"]])
                    dataset["label_m1"].extend([label_m1 for i in df["body"]])
                
                label_m2 = label_m1
                label_m1 = label
            count += 1
          
        current_date.add(day=1)
        
    print("Number of files loaded : ", count)
    return pd.DataFrame(dataset)

def get_LDA_data():
    return pd.read_csv("../Data/LDA_Data/save2.csv", sep=",")

def get_TFIDF_data():
    return pd.read_csv("../Data/TFIDF.csv", sep=",")

def get_prediction_stats(df_prediction):
    counter_correct_preds = collections.Counter(df_prediction["correct"])
    correct_pred = counter_correct_preds[True]
    wrong_pred = counter_correct_preds[False]
    
    print(f"""Number Correct/Wrong Guess : {correct_pred}/{wrong_pred}
              Accuracy : {(correct_pred/(correct_pred + wrong_pred)) * 100}""" )
    print("Invalid sentences count", collections.Counter(df_prediction["preds"])[-1])

# -- ==user_accounts== --