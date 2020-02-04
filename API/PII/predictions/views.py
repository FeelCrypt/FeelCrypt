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
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# Endpoint pour les fichier .CSS et .JS pour le fonctionnement du front du site
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

# Endpoint prédiction du cours du bitcoin en utilisant le modèle basé sur les sentiments des textes
def get_prediction_texts(request):
    with open('params.json') as json_file:
        data = json.load(json_file)

    loaded_model = pickle.load(open("xgboost_bitcoin_texts.dat", "rb"))
    df = dataset.read_today_data(threads=["bitcoin", "btc"])
    preds = keras_bitcoin.get_predictions(df["text"], loaded_model, data["vocab_length"], data["max_sentence_size"])
    pred = -1
    if len(collections.Counter(preds).most_common()) > 0 and len(collections.Counter(preds).most_common()[0]) > 0:
        pred = collections.Counter(preds).most_common()[0][0]
    return JsonResponse({"pred" : int(pred)}, status = 200)


# Endpoint prédiction du cours du bitcoin en utilisant le modèle basé sur les labels des journées précédente et de la date actuelle
def get_prediction_date(request):
    date = moment.now()
    date_m1 = moment.now().add(day=-1) 
    date_m2 = moment.now().add(day=-2) 

    get_chart_price_cryptocurrencies_csv.get_csv_crypto_prices()
    bitcoin_price = dataset.get_multi_class_label()
    

    data = {"year" : [date.year],	"month" : [date.month], "day" : [date.day], "label_m1" : [bitcoin_price[date_m1.format("YYYY-MM-DD")]], "label_m2" : [bitcoin_price[date_m2.format("YYYY-MM-DD")]]}
    df = pd.DataFrame(data)
    loaded_model = pickle.load(open("xgboost_bitcoin_date.dat", "rb"))
    pred = loaded_model.predict(df)

    return JsonResponse({"pred" : int(pred[0])}, status = 200)

def train_model_texts(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    df = dataset.get_text_labeled_dataset(from_date = from_date, to_date = to_date, binary=False)
    texts = df["text"]
    labels = df["label"]
    texts_train, texts_test , labels_train, labels_test, vocab_length, max_sentence_size\
    = keras_bitcoin.get_train_test_data(texts, labels)

    xg_class = XGBClassifier(objective ='reg:tweedie',
                            max_depth = 9,
                            n_estimators = 100,
                            eta = 0.5,
                            )
    xg_class.fit(texts_train,labels_train)
    preds = xg_class.predict(texts_test)
    accuracy = accuracy_score(labels_test, preds)
    mse = mean_squared_error(labels_test, preds)

    data = {"vocab_length" : vocab_length, "max_sentence_size" : max_sentence_size}

    with open('params.json', 'w') as outfile:
        json.dump(data, outfile)
        
    pickle.dump(xg_class, open("xgboost_bitcoin_texts.dat", "wb"))

    return JsonResponse({"accuracy" : float(accuracy), "mse" : float(mse)}, status = 200)

def train_model_date(request):
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    df = dataset.get_date_labeled_dataset(from_date = from_date, to_date = to_date, binary=False)
   
    texts_train, texts_test , labels_train, labels_test = train_test_split(df.drop(columns=["label"]), df["label"] , test_size = 0.20)

    xg_class = XGBClassifier(objective ='reg:tweedie',
                            max_depth = 9,
                            n_estimators = 100,
                            eta = 0.5,
                            )
    xg_class.fit(texts_train,labels_train)
    preds = xg_class.predict(texts_test)
    accuracy = accuracy_score(labels_test, preds)
    mse = mean_squared_error(labels_test, preds)

        
    pickle.dump(xg_class, open("xgboost_bitcoin_date.dat", "wb"))

    return JsonResponse({"accuracy" : float(accuracy), "mse" : float(mse)}, status = 200)

