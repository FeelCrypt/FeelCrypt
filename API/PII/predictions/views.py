from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import get_chart_price_cryptocurrencies_csv
import dataset
import keras_bitcoin
import pickle
import json
import collections
import moment
import pandas as pd
from django.http import FileResponse
from os import listdir


def home(request):
    return render(request, "predictions/index.html")

def CSSFiles(request, file=""):
    return FileResponse(open(f"./predictions/templates/css/{file}", 'rb'))

def JSfiles(request, file=""):
    return FileResponse(open(f"./predictions/templates/js/{file}", 'rb'))

def Imgfiles(request, file=""):
    return FileResponse(open(f"./predictions/templates/img/portfolio/{file}", 'rb'))

def VendorJquery(request):
    return FileResponse(open("./predictions/templates/vendor/jquery/jquery.min.js", 'rb'))

def VendorBoostrap(request):
    return FileResponse(open("./predictions/templates/vendor/bootstrap/js/bootstrap.bundle.min.js", 'rb'))

def VendorJqueryeasing(request):
    return FileResponse(open("./predictions/templates/vendor/jquery-easing/jquery.easing.min.js", 'rb'))

def VendorFontAwesome(request):
    return FileResponse(open("./predictions/templates/vendor/fontawesome-free/css/all.min.css", 'rb'))

def Fontfiles(request, file=""):
    return FileResponse(open(f"./predictions/templates/vendor/fontawesome-free/webfonts/{file}", "rb"))

def get_prediction(request):

    with open('params.json') as json_file:
        data = json.load(json_file)

    loaded_model = pickle.load(open("xgboost_bitcoin_texts.dat", "rb"))
    df = dataset.read_today_data(threads=["bitcoin", "btc"])
    preds = keras_bitcoin.get_predictions(df["text"], loaded_model, data["vocab_length"], data["max_sentence_size"])
    pred = collections.Counter(preds).most_common()[0][0]
    return JsonResponse({"pred" : int(pred)}, status = 200)
    
def get_prediction_noword(request):
    date = moment.now()
    date_m1 = moment.now().add(day=-1) 
    date_m2 = moment.now().add(day=-2) 

    bitcoin_price = dataset.get_multi_class_label([-5, -0.2, 0.2, 5])

    data = {"label_m1" : [bitcoin_price[date_m1.format("YYYY-MM-DD")]], "label_m2" : [bitcoin_price[date_m2.format("YYYY-MM-DD")]], "year" : [date.year],	"month" : [date.month], "day" : [date.day]}

    df = pd.DataFrame(data)

    loaded_model = pickle.load(open("xgboost_bitcoin_date.dat", "rb"))
    pred = loaded_model.predict(df)

    return JsonResponse({"pred" : int(pred[0])}, status = 200)