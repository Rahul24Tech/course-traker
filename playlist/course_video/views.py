import calendar
import time
from copy import deepcopy
from datetime import datetime

import openpyxl
import pytz
import youtube_dl
from django import template as tt
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import generic
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from taggit.models import Tag

from .forms import AddCourseForm
from .forms import ContactForm
from .forms import CreateUserForm
from .forms import EditProfileForm
from .forms import ProfilePageForm
from .models import *

# import datetime

# Create your views here.


class Home(View):
    """
    This class is used to display home page of an app.
    """

    def get(self, request):
        return render(request, "home.html")


class Main(ListView):
    """
    This class is used to display the course,
    and progress bar status too, and after successfully adition of course email
    notification is sent.
    """

    model = Course
    paginate_by = 4
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(Main, self).get_context_data(**kwargs)
        paginator = Paginator(Course.objects.select_related().all(), self.paginate_by)
        page = self.request.GET.get("page")
        try:
            course = paginator.page(page)
        except PageNotAnInteger:
            course = paginator.page(1)
        except EmptyPage:
            course = paginator.page(paginator.num_pages)

        course_id = []
        course = Course.objects.all()
        profile = Profile.objects.get(user=self.request.user)
        for item in course.iterator():
            course_list = Course.objects.get(id=item.id)
            course_id.append(course_list)
        progress = {}
        for data in course_id:
            global_count = 0
            # import pdb
            # pdb.set_trace()
            list_item = PlaylistItem.objects.filter(playlist=data.id).filter(
                author=data.author
            )
            for title in list_item.iterator():
                if title.status == "Completed":
                    global_count = global_count + 1
                if global_count == 0:
                    percentage = 0
                else:
                    total = global_count
                    percentage = 100 * float(total) / float(list_item.count())
                progress[data.id] = round(percentage)
            self.request.session["progress"] = progress
        print(progress)
        context["course"] = paginator.page(context["page_obj"].number)
        context["per"] = progress
        context["profile"] = profile
        return context


class AddCourse(FormView):
    """
    This class is used to add course to list_of_playlist
    """

    template_name = "add_course.html"
    form_class = AddCourseForm
    success_url = "course"

    def form_valid(self, form):

        link = form.cleaned_data["link"]
        tag = form.cleaned_data["tags"]
        ydl = youtube_dl.YoutubeDL({"ignoreerrors": True, "quiet": True})
        with ydl:
            result = ydl.extract_info(
                link, download=False  # We just want to extract the info
            )
        # import pdb
        # pdb.set_trace()
        playlist_info = []
        for video in result["entries"]:
            video_url = dict(
                (k, video[k])
                for k in ["title", "duration", "webpage_url"]
                if k in video
            )
            playlist_info.append(video_url.copy())

        form.instance.title = result.get("title")

        form.instance.author = self.request.user
        obj = form.save()
        obj.tags.add(*tag)
        cource = Course.objects.get(id=obj.id)
        for i in playlist_info:
            title = i.get("title")
            duration = i.get("duration")
            playlist_url = i.get("webpage_url")
            list_store = PlaylistItem(
                list_item=title,
                time=duration,
                link=playlist_url,
                playlist=cource,
                author=self.request.user,
            )
            list_store.save()
        messages.success(
            self.request, "Sent Email Successfully...Check your mail please"
        )
        return super().form_valid(form)


class TagListing(View):
    """
    This class is used to filter out course based on given tags

    Args:-
        tags = slug of tag name
    return-
        list of course based on provided tags.
    """

    def get(self, request, tags):
        course = Course.objects.all()
        tags = Tag.objects.filter(slug=tags).values_list("name", flat=True)
        posts = course.filter(tags__name__in=tags)
        info = {
            "tags": posts,
        }
        return render(request, "tag.html", info)


class Listing(View):
    """
    This class is used to open particular video playlist and maintain the progress
    bar status.

    Args-
     id - This is the id of particular video playlist.

    return-
        list of video playlist.
    """

    def get(self, request, id):
        status_data = ["Yet to Start", "In Progress", "On Hold", "Completed"]
        course_list = Course.objects.get(id=id)
        list_item = PlaylistItem.objects.filter(playlist=course_list.id)
        request.session["id"] = id

        course_info = {
            "videoDetail": list_item,
            "id": id,
            "overall": status_data,
            "title": course_list.title,
        }

        return render(request, "List.html", course_info)


class HandleSignUp(View):
    """
    This class is used to handle SignUp of new user.
    """

    form = CreateUserForm()

    def post(self, request):

        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, "Techhub account was created for" + user)
            return redirect("login")

    def get(self, request):
        return render(request, "signup.html", {"form": self.form})


class HandeLogin(View):
    """
    This class is used to handle login or allauth social login also.
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
    This class is used to handle logout and redirect to homepage of an app.
    """

    def get(self, request):
        logout(request)
        messages.success(request, "Successfully logged out")
        return redirect("/")


class Contact(View):
    """
    This class is used to take any query from an app.
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
        return render(request, "contact.html")


class Search(View):
    """
    This class is used to filter out course which is written on search box.
    """

    def get(self, request):
        query = self.request.GET["query"]
        allCourse = Course.objects.filter(title__icontains=query)
        params = {"allCourse": allCourse}
        return render(request, "search.html", params)


class Editing(View):
    """
    This class is used to edit the title of course.
    """

    def post(self, request, id):
        course = Course.objects.get(id=id)
        string_var = course.title
        title = request.POST["title"]
        course.title = title
        course.save(update_fields=["title"])
        PlaylistItem.objects.filter(playlist=course.id).update(playlist=course.id)
        messages.success(request, "Successfully updated title")
        return redirect("/course")

    def get(self, request, id):
        course = Course.objects.get(id=id)
        return render(request, "edit.html", {"course": course, "id": id})


class GetStatus(View):
    """
    This class is used to store current status value
    ("Yet to Start", "In Progress", "On Hold", "Completed")
    to DB.
    """

    def post(self, request, id):
        update_status = PlaylistItem.objects.get(id=id)
        list_id = request.session.get("id")
        choice = request.POST["choice"]
        update_status.author = self.request.user
        update_status.status = choice
        update_status.save(update_fields=["status", "author"])

        return redirect("listing", id=list_id)


class Clone(View):
    """
    This class is used to make clone of public course of other user.
    """

    def get(self, request, id):
        # import pdb
        # pdb.set_trace()
        course = Course.objects.get(id=id)
        if self.request.user.id != course.author.id and course.public:
            old_obj = deepcopy(course)
            playlist = PlaylistItem.objects.filter(playlist=old_obj.id)
            old_playlist = deepcopy(playlist)

            old_tag = old_obj.tags.all()
            course.id = None
            course.author = self.request.user

            course.save()
            for tag in old_tag.iterator():
                course.tags.add(tag.name)
            for item in old_playlist:
                PlaylistItem.objects.create(
                    list_item=item.list_item,
                    time=item.time,
                    playlist=course,
                    link=item.link,
                    status="Yet To Start",
                    author=self.request.user,
                )
        return redirect("main")


class CourseCsv(View):
    """
    This class is used to download private course in excel format.
    """

    def get(self, request):
        wb = openpyxl.Workbook()
        sheetOne = wb.create_sheet("ListOfPlaylist")
        course = Course.objects.filter(public=False)
        data_view = []

        for item in course.iterator():
            if request.user.id == item.author.id:
                progress = request.session.get("progress")
                for i in progress.keys():
                    if i.find(str(item.id)) > -1:
                        progress_data = f"{progress[i]} %"
                old_tag = item.tags.all()
                for tag in old_tag.iterator():
                    data = (item.title, item.link, tag.name, progress_data)

                data_view.append(list(data))
                item_list = [tuple(l) for l in data_view]
                add_tuple = ("Title", "Link", "Tag", "Progress")
                item_list.insert(0, add_tuple)

        for playlist_item in item_list:
            sheetOne.append(playlist_item)
        wb.remove(wb["Sheet"])
        current_GMT = time.gmtime()

        # ts stores timestamp
        ts = calendar.timegm(current_GMT)
        date_time = datetime.fromtimestamp(ts)

        # convert timestamp to string in dd-mm-yyyy HH:MM:SS
        str_date_time = date_time.strftime("%d-%m-%Y, %H:%M:%S")
        wb.save(f"{request.user} {str_date_time}.xlsx")
        return redirect("main")


class Upload(View):
    """
    This class is used to added course by just providing excel sheets in proper format.
    """

    def post(self, request):
        excel_file = request.FILES["excel_file"]
        wb = openpyxl.load_workbook(excel_file)
        sheets = wb.sheetnames
        excel_data = []
        excel_playlist = list()
        for i in sheets:
            work = wb[i]

            for row in work.iter_rows():
                row_data = list()
                for cell in row:
                    row_data.append(str(cell.value))
                excel_data.append(row_data)
            excel_playlist.append(excel_data)

        for item in excel_playlist:
            if ["Title", "Link", "Tag", "Progress"] in item:
                to_exclude = {0}
                data = [
                    element for i, element in enumerate(item) if i not in to_exclude
                ]
                for item in data:
                    try:
                        old_course = Course.objects.get(title=item[0])
                    except Course.DoesNotExist:
                        old_course = None
                    if old_course:
                        messages.info(
                            request, "course is already present in List of playlist"
                        )
                    else:
                        course = Course.objects.create(
                            author=request.user,
                            title=item[0],
                            link=item[1],
                            public=True,
                        )
                        course.tags.add(item[2])
                        course.save()
                    ydl = youtube_dl.YoutubeDL({"ignoreerrors": True, "quiet": True})
                    with ydl:
                        result = ydl.extract_info(
                            item[1], download=False  # We just want to extract the info
                        )

                    playlist_info = []
                    for video in result["entries"]:
                        video_url = dict(
                            (k, video[k])
                            for k in ["title", "duration", "webpage_url"]
                            if k in video
                        )
                        playlist_info.append(video_url.copy())
                    for i in playlist_info:
                        title = i.get("title")
                        duration = i.get("duration")
                        playlist_url = i.get("webpage_url")
                        list_store = PlaylistItem(
                            list_item=title,
                            time=duration,
                            playlist=result.get("title"),
                            link=playlist_url,
                        )
                        list_store.save()
            else:
                messages.info(
                    request,
                    "Format of excel sheet not meet as expected please Go through the sample excel file for correct format",
                )

            return redirect(Main)

    def get(self, request):
        return render(request, "upload.html")


class Download(View):
    """
    This class is to download sample.xlsx file for correct excel file format.
    """

    def get(self, request):
        filename = "sample.xlsx"  # this is the file people must download
        with open(filename, "rb") as f:
            response = HttpResponse(f.read(), content_type="application/vnd.ms-excel")
            response["Content-Disposition"] = "attachment; filename=" + filename
            response["Content-Type"] = "application/vnd.ms-excel; charset=utf-16"
            return response


class UserEditView(generic.UpdateView):
    """This class is used to edit users setting"""

    form_class = EditProfileForm
    template_name = "edit_profile.html"
    success_url = "/"

    def get_object(self):
        return self.request.user


class ShowProfilePageView(DetailView):
    """
    This class is used to view profile page.

    return - context of profile data and course_author data
    """

    model = Profile
    template_name = "user_profile.html"

    def get_context_data(self, *args, **kwargs):

        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        pages_user = get_object_or_404(Profile, id=self.kwargs["pk"])
        course_title = Course.objects.filter(author=pages_user.user)
        context["page_user"] = pages_user
        context["course_title"] = course_title
        return context


class EditProfilePageView(generic.UpdateView):
    """
    This class is used to edit profile page
    """

    model = Profile
    fields = ["bio", "profile_pic", "website_url", "facebook_url", "time_preference"]
    template_name = "edit_profile_page.html"
    success_url = "/"


class CreateProfilePage(CreateView):
    """
    This class is used to profile page of user.
    """

    model = Profile
    form_class = ProfilePageForm
    template_name = "create_user_profile.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class FavouriteAdd(View):
    """
    This class used to add favourite course for particular user.

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
    This class is used to view all favourite listed course.

    return: It return all data which is in favourite field.
    """

    model = Course
    template_name = "favourite.html"

    def get_context_data(self, **kwargs):
        context = super(FavouriteList, self).get_context_data(**kwargs)
        favourite = Course.objects.filter(favourites=self.request.user)
        context["favourite"] = favourite
        return context


class WatchLaterCourseAdd(View):
    """
    This class is used to add course to watch later section.

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
    This class is used to view all course present in watch_later field.

    return:- It return all data of watch_later field.
    """

    model = Course
    paginate_by = 4
    template_name = "watch_later_course.html"

    def get_context_data(self, **kwargs):
        context = super(WatchLaterCourseList, self).get_context_data(**kwargs)
        watch_later = Course.objects.filter(watch_later=self.request.user)
        context["watch_later"] = watch_later
        return context


class WatchLaterPlaylistItemAdd(View):
    """
    This class is used to add particular playlist video in watch_later section.

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
    This class is used to view all playlist in watch_later_playlist section.

    return: It return playlist_info contains(title, duration, thumbnail, webpage_url).
    """

    model = PlaylistItem
    template_name = "watch_later_playlist.html"

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
