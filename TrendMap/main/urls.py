""" Urls for the app """
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('begin_twitter_authentication/', views.begin_twitter_authentication),
]
