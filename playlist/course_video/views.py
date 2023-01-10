from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from taggit.models import Tag
from django.http import HttpResponse
from django.views import View, generic
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django import template as tt


from .models import *
from .forms import CreateUserForm, ContactForm, AddCourseForm, EditProfileForm, ProfilePageForm, TimePreferenceForm
from django.core.paginator import Paginator
from django.db.models import Count

import youtube_dl
import openpyxl
import calendar
import time
# import datetime
import pytz
from datetime import datetime
from copy import deepcopy

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
    paginate_by = 4  # add this
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
        # import pdb
        # pdb.set_trace()
        course = Course.objects.all()
        for item in course.iterator():
            course_list = Course.objects.get(id=item.id)
            course_id.append(course_list)
        progress = {}
        for data in course_id:
            global_count = 0
            list_total = PlaylistItem.objects.filter(playlist_title=data.title).filter(author=data.author).count()
            list_item = PlaylistItem.objects.filter(playlist_title=data.title).filter(author=data.author)
            for title in list_item.iterator():
                if title.status == "Completed":
                    global_count = global_count + 1
                if global_count == 0:
                    percentage = 0
                else:
                    total = global_count
                    percentage = 100 * float(total) / float(list_total)
                progress[data.id] = round(percentage)
            self.request.session["progress"] = progress
        # import pdb
        # pdb.set_trace()
        print(progress)
        context["course"] = paginator.page(context["page_obj"].number)
        context["per"] = progress
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
        playlist_info = []
        for video in result["entries"]:
            video_url = dict(
                (k, video[k])
                for k in ["title", "duration", "webpage_url"]
                if k in video
            )
            playlist_info.append(video_url.copy())

        form.instance.title = result.get("title")
        # import pdb
        # pdb.set_trace()
        form.instance.author = self.request.user
        obj = form.save()
        obj.tags.add(*tag)
        for i in playlist_info:
            title = i.get("title")
            duration = i.get("duration")
            playlist_url = i.get("webpage_url")
            list_store = PlaylistItem(
                list_item=title,
                time=duration,
                playlist_title=result.get("title"),
                link=playlist_url,
                author=self.request.user
            )
            list_store.save()
        form.send_email()
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
        list_item = PlaylistItem.objects.filter(playlist_title=course_list.title)
        request.session["id"] = id

        course_info = {"videoDetail": list_item, "id": id, "overall": status_data, "title": course_list.title}

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
        query = request.GET["query"]
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
        PlaylistItem.objects.filter(playlist_title=string_var).update(
            playlist_title=course.title
        )
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
            playlist = PlaylistItem.objects.filter(playlist_title=old_obj.title)
            old_playlist = deepcopy(playlist)
            
            old_tag = old_obj.tags.all()
            course.id = None
            course.author = self.request.user
            for item in old_playlist:
                PlaylistItem.objects.create(
                    list_item=item.list_item,
                    time=item.time,
                    playlist_title=old_obj.title,
                    link=item.link,
                    status="Yet To Start",
                    author=self.request.user
                )
            course.save()
            for tag in old_tag.iterator():
                course.tags.add(tag.name)
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
                            playlist_title=result.get("title"),
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
    form_class = EditProfileForm
    template_name = "edit_profile.html"
    success_url = "/" 
    
    def get_object(self):
        return self.request.user
    
    
class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = "/"
    
    
class ShowProfilePageView(DetailView):
    model = Profile
    template_name = "user_profile.html"
    
    def get_context_data(self, *args, **kwargs):
        # users = Profile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        
        pages_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context["page_user"] = pages_user
        return context   
    
    
class EditProfilePageView(generic.UpdateView):
    model = Profile
    fields = ['bio', 'profile_pic', 'website_url', 'facebook_url', 'time_preference']
    template_name = "edit_profile_page.html"
    success_url = "/"
    
    
class CreateProfilePage(CreateView):
    model = Profile
    form_class = ProfilePageForm
    template_name = "create_user_profile.html"
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    
# class TimePreferencePage(View):
#     def post(self, request):
#         form = TimePreferenceForm(request.POST)
#         if form.is_valid():
#             time = form.cleaned_data.get('time_preference')
#             profile = Profile(time_preference=time)
#             profile.save()
#             # do something with your results
#         else:
#             form = TimePreferenceForm