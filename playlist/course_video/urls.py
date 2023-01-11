from django.contrib import admin
from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("course", Main.as_view(), name="main"),
    path("add", AddCourse.as_view(), name="add"),
    path("signup", HandleSignUp.as_view(), name="signup"),
    path("login", HandeLogin.as_view(), name="login"),
    path("logout", HandelLogout.as_view(), name="handleLogout"),
    path("contact", Contact.as_view(), name="contact"),
    path("listing", Listing.as_view(), name="listing"),
    path("listing/<int:id>/", Listing.as_view(), name="listing"),
    path("editing/<int:id>/", Editing.as_view(), name="editing"),
    path("tag_listing/<slug:tags>/", TagListing.as_view(), name="tag_listing"),
    path("search", Search.as_view(), name="search"),
    path("getstatus/<int:id>", GetStatus.as_view(), name="getstatus"),
    path("clone/<int:id>", Clone.as_view(), name="clone"),
    path("course_csv", CourseCsv.as_view(), name="course_csv"),
    path("upload", Upload.as_view(), name="upload"),
    path("download", Download.as_view(), name="download"),
    path("edit_profile", UserEditView.as_view(), name="edit_profile"),
    path("<int:pk>/profile", ShowProfilePageView.as_view(), name="show_profile"),
    path(
        "<int:pk>/edit_profile_page",
        EditProfilePageView.as_view(),
        name="edit_profile_page",
    ),
    path("create_profile", CreateProfilePage.as_view(), name="create_profile"),
]
