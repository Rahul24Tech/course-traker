from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include
from django.urls import path

from .views import *

app_name = "course_video"

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("course", Main.as_view(), name="course"),
    path("add", AddCourse.as_view(), name="add"),
    path("listing/<int:id>/", Listing.as_view(), name="listing"),
    path("editing/<int:id>/", Editing.as_view(), name="editing"),
    path("tag_listing/<slug:tags>/", TagListing.as_view(), name="tag_listing"),
    path("search", Search.as_view(), name="search"),
    path("getstatus/<int:id>", GetStatus.as_view(), name="getstatus"),
    path("clone/<int:id>", Clone.as_view(), name="clone"),
    path("course_csv", CourseCsv.as_view(), name="course_csv"),
    path("upload", Upload.as_view(), name="upload"),
    path("download", Download.as_view(), name="download"),
]
