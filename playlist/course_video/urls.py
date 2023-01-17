from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include
from django.urls import path

from .views import *


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
    path("fav/<int:id>/", FavouriteAdd.as_view(), name="favourite_add"),
    path("profile/favourite", FavouriteList.as_view(), name="profile_favourite"),
    path("watch/<int:id>/", WatchLaterCourseAdd.as_view(), name="watch_later_add"),
    path(
        "profile/watch_later",
        WatchLaterCourseList.as_view(),
        name="profile_watch_later",
    ),
    path(
        "watch_playlist/<int:id>/",
        WatchLaterPlaylistItemAdd.as_view(),
        name="watch_later_playlist_add",
    ),
    path(
        "profile/watch_later_playlist",
        WatchLaterPlaylistItemList.as_view(),
        name="profile_watch_later_playlist",
    ),
]
