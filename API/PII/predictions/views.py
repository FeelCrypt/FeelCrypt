from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import get_chart_price_cryptocurrencies_csv
import dataset
#import keras_bitcoin
import moment
import pickle
import pandas as pd

def home(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    return HttpResponse("""
        <h1>Bienvenue sur mon blog !</h1>
        <p>Les crêpes bretonnes ça tue des mouettes en plein vol !</p>
    """)

def accueil(request):
    return render(request, "predictions/accueil.html")

def get_prediction(request):
    #update reddit data
    df = dataset.read_today_data(threads=["bitcoin", "btc"])
    text_to_predict = dataset.encode_data(df["text"])
    xg_class = pickle.load(open("xgboost_bitcoin.dat", "rb"))
    preds = xg_class.predict(text_to_predict)
    pred = collections.Counter(preds).most_common()[0][0]
    #dico = {"brand": "Ford", "model": "Mustang", "year": 1964}
    return JsonResponse({"pred" : pred}, status = 200)

def get_prediction_noword(request):
    


# Create your views here.
