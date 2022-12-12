from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("", main, name="main"),
    path('course', detail, name="detail"),
    path("list", playList, name="playList")
]