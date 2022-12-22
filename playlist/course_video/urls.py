from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("course", main, name="main"),
    path('signup', handleSignUp, name="signup"),
    path('login', handeLogin, name="login"),
    path('logout', handelLogout, name="handleLogout"),
    path('contact', contact, name="contact"),
    path("listing", listing, name="listing"),
    path("listing/<int:id>/", listing, name="listing"),
    path("listing/<int:id>/<int:pk>", listing, name="listing"),
    path("editing/<int:id>/", editing, name="editing"),
    path("tag_listing/<slug:tags>/", tag_listing, name="tag_listing"),
    path('search', search, name="search"),
    path('getstatus/<int:id>', getstatus, name="getstatus"),
    path('clone', clone, name="clone"),
    
]