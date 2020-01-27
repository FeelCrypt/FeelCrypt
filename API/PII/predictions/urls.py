from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path("vendor/fontawesome-free/css/all.min.css", views.VendorFontAwesome),
    path("vendor/fontawesome-free/webfonts/<str:file>", views.Fontfiles),
    path("vendor/jquery/jquery.min.js", views.VendorJquery),
    path("vendor/bootstrap/js/bootstrap.bundle.min.js", views.VendorBoostrap),
    path("vendor/jquery-easing/jquery.easing.min.js", views.VendorJqueryeasing),
    path("css/<str:file>", views.CSSFiles),
    path("js/<str:file>", views.JSfiles),
    path("img/portfolio/<str:file>", views.Imgfiles),
    path('get_prediction', views.get_prediction),
    path('get_prediction_noword', views.get_prediction_noword)
]
