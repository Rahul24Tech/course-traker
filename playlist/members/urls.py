from django.urls import path

from members.views import *

app_name = "members"

urlpatterns = [
    path("signup", HandleSignUp.as_view(), name="signup"),
    path("login", HandeLogin.as_view(), name="login"),
    path("logout", HandelLogout.as_view(), name="handleLogout"),
    path("contact", Contact.as_view(), name="contact"),
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
