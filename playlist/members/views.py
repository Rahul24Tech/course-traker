import youtube_dl
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, HttpResponseRedirect, redirect, render
from django.views import generic
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from members.forms import ContactForm, CreateUserForm, EditProfileForm, ProfilePageForm
from members.models import *
from course_video.models import Course, PlaylistItem
# Create your views here.

class HandleSignUp(View):
    """
    HandleSignUp class is used to handle SignUp of new user.
    """

    form = CreateUserForm()

    def post(self, request):

        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, "Techhub account was created for" + user)
            return redirect("members:login")

    def get(self, request):
        return render(request, "account/signup.html", {"form": self.form})


class HandeLogin(View):
    """
    HandleLogin class is used to handle login or allauth social login also.
    """

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.info(request, "Username OR Password is incorrect")

    def get(self, request):
        return render(request, "account/login.html")


class HandelLogout(View):
    """
    HandleLogout class is used to handle logout and redirect to homepage of an app.
    """

    def get(self, request):
        logout(request)
        messages.success(request, "Successfully logged out")
        return redirect("/")


class Contact(View):
    """
    Contact class is used to take any query from an app.
    """

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            content = form.cleaned_data["content"]
            if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(content) < 4:
                messages.error(request, "Please fill the form correctly")
            else:
                contact = Contact(name=name, email=email, phone=phone, content=content)
                contact.save()
                messages.success(request, "Your message has been successfully sent")

    def get(self, request):
        return render(request, "account/contact.html")


class UserEditView(generic.UpdateView):
    """UserEditView class is used to edit users setting"""

    form_class = EditProfileForm
    template_name = "account/edit_profile.html"
    success_url = "/"

    def get_object(self):
        return self.request.user


class ShowProfilePageView(DetailView):
    """
    ShowProfilePageView class is used to view profile page.

    return - context of profile data and course_author data
    """

    model = Profile
    template_name = "account/user_profile.html"

    def get_context_data(self, *args, **kwargs):

        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        pages_user = get_object_or_404(Profile, id=self.kwargs["pk"])
        course_title = Course.objects.filter(author=pages_user.user)
        context["page_user"] = pages_user
        context["course_title"] = course_title
        return context


class EditProfilePageView(generic.UpdateView):
    """
    EditProfilePageView class is used to edit profile page
    """

    model = Profile
    fields = ["bio", "profile_pic", "website_url", "facebook_url", "time_preference"]
    template_name = "account/edit_profile_page.html"
    success_url = "/"


class CreateProfilePage(CreateView):
    """
    CreateProfilePage class is used to profile page of user.
    """

    model = Profile
    form_class = ProfilePageForm
    template_name = "account/create_user_profile.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class FavouriteAdd(View):
    """
    FavouriteAdd class used to add favourite course for particular user.

    Args:
        id(int)- It is id of particular course to add as favourite

    return: First filter the favourite field if exist then it remove the already present course
            and if favourite field is empty then add the course.
    """

    def get(self, request, id):
        course = get_object_or_404(Course, id=id)
        if course.favourites.filter(id=self.request.user.id).exists():
            course.favourites.remove(self.request.user)
            messages.success(
                self.request, "Course successfully removed from Favourite list"
            )
        else:
            course.favourites.add(self.request.user)
            messages.success(
                self.request, "Course successfully added to Favourite list"
            )

        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    def post(self, request, id):
        if request.POST.get("delete"):
            selected_course = Course.objects.filter(
                pk__in=list(map(int, self.request.POST.getlist("selected[]")))
            )
            for course in selected_course:
                if course.favourites.filter(id=self.request.user.id).exists():
                    course.favourites.remove(self.request.user)
            messages.success(
                self.request, "Course successfully removed from Favourite list"
            )
        return HttpResponseRedirect(request.META["HTTP_REFERER"])


class FavouriteList(ListView):
    """
    FavouriteList class is used to view all favourite listed course.

    return: It return all data which is in favourite field.
    """

    model = Course
    template_name = "account/favourite.html"

    def get_context_data(self, **kwargs):
        context = super(FavouriteList, self).get_context_data(**kwargs)
        favourite = Course.objects.filter(favourites=self.request.user)
        context["favourite"] = favourite
        return context


class WatchLaterCourseAdd(View):
    """
    WatchLaterCourseAdd class is used to add course to watch later section.

    Args:
        id(int): First filter the watch_later field if exist then it remove the already present course
            and if watch_later field is empty then add the course to watch later section.
    """

    def get(self, request, id):
        course = get_object_or_404(Course, id=id)
        if course.watch_later.filter(id=self.request.user.id).exists():
            course.watch_later.remove(self.request.user)
            messages.success(
                self.request, "Course successfully removed from Watch Later list"
            )
        else:
            course.watch_later.add(self.request.user)
            messages.success(
                self.request, "Course successfully added to Watch Later list"
            )

        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    def post(self, request, id):
        if request.POST.get("delete"):
            selected_course = Course.objects.filter(
                pk__in=list(map(int, self.request.POST.getlist("selected[]")))
            )
            for course in selected_course:
                if course.watch_later.filter(id=self.request.user.id).exists():
                    course.watch_later.remove(self.request.user)
            messages.success(
                self.request, "Course successfully removed from Watch Later list"
            )
        return HttpResponseRedirect(request.META["HTTP_REFERER"])


class WatchLaterCourseList(ListView):
    """
    WatchLaterCourseList class is used to view all course present in watch_later field.

    return:- It return all data of watch_later field.
    """

    model = Course
    paginate_by = 4
    template_name = "account/watch_later_course.html"

    def get_context_data(self, **kwargs):
        context = super(WatchLaterCourseList, self).get_context_data(**kwargs)
        watch_later = Course.objects.filter(watch_later=self.request.user)
        context["watch_later"] = watch_later
        return context


class WatchLaterPlaylistItemAdd(View):
    """
    WatchLaterPlaylistItemAdd class is used to add particular playlist video in watch_later section.

    Args:
        id(int): It is id of particular playlist of a course
    """

    def get(self, request, id):
        playlist = get_object_or_404(PlaylistItem, id=id)

        if playlist.watch_later_playlist.filter(id=self.request.user.id).exists():
            playlist.watch_later_playlist.remove(self.request.user)
            messages.success(
                self.request, "playlist successfully removed from Watch Later list"
            )
        else:
            playlist.watch_later_playlist.add(self.request.user)
            messages.success(
                self.request, "playlist successfully added to Watch Later list"
            )

        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    def post(self, request, id):
        if request.POST.get("delete"):
            selected_playlist = PlaylistItem.objects.filter(
                pk__in=list(map(int, self.request.POST.getlist("selected[]")))
            )
            for course in selected_playlist:
                if course.watch_later_playlist.filter(id=self.request.user.id).exists():
                    course.watch_later_playlist.remove(self.request.user)
            messages.success(
                self.request, "playlist successfully removed from Watch Later list"
            )
        return HttpResponseRedirect(request.META["HTTP_REFERER"])


class WatchLaterPlaylistItemList(ListView):
    """
    WatchLaterPlaylistItemList class is used to view all playlist in watch_later_playlist section.

    return: It return playlist_info contains(title, duration, thumbnail, webpage_url).
    """

    model = PlaylistItem
    template_name = "account/watch_later_playlist.html"

    def get_context_data(self, **kwargs):
        context = super(WatchLaterPlaylistItemList, self).get_context_data(**kwargs)
        watch_later = PlaylistItem.objects.filter(
            watch_later_playlist=self.request.user
        )
        playlist_info = []
        for item in watch_later:
            ydl = youtube_dl.YoutubeDL({"ignoreerrors": True, "quiet": True})
            with ydl:
                result = ydl.extract_info(
                    item.link, download=False  # We just want to extract the info
                )
            video_url = dict(
                (k, result[k])
                for k in ["title", "duration", "webpage_url", "thumbnail"]
                if k in result
            )
            video_url["id"] = item.id
            playlist_info.append(video_url)
        context["playlist_info"] = playlist_info
        return context
