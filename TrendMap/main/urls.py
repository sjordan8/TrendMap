""" Urls for the app """
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('begin_auth/', views.begin_auth),
    path('verify/', views.verify),
    path('get_tweets/', views.get_tweets),
]
