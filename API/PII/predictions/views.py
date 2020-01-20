from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

def home(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    return HttpResponse("""
        <h1>Bienvenue sur mon blog !</h1>
        <p>Les crêpes bretonnes ça tue des mouettes en plein vol !</p>
    """)

def accueil(request):
    return render(request, "predictions/accueil.html")

def get_prediction(request):
    dico = {"brand": "Ford", "model": "Mustang", "year": 1964}
    return JsonResponse(dico, status = 200)


# Create your views here.
