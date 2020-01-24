from django.urls import path
from . import views

urlpatterns = [
    path('accueil', views.accueil),
    path('get_prediction', views.get_prediction),
    path('get_prediction_noword', views.get_prediction_noword)
]
