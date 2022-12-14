from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("course", main, name="main"),
    path('tech', techHubHome, name="techHubHome"),
    path('signup', handleSignUp, name="handleSignUp"),
    path('login', handeLogin, name="handleLogin"),
    path('logout', handelLogout, name="handleLogout"),
    path('contact', contact, name="contact"),
    path("listing", listing, name="listing"),
    path("listing/<int:id>/", listing, name="listing"),
    path("editing/<int:id>/", editing, name="editing"),
    path("tag_listing/<slug:tags>/", tag_listing, name="tag_listing"),
    path('search', search, name="search"),
]