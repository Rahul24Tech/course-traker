from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from taggit.utils import _parse_tags

from .models import *
from .forms import CreateUserForm, ContactForm, StatusForm
from django.core.paginator import Paginator

import youtube_dl
import openpyxl
import re
import calendar
import time
from datetime import datetime
from copy import deepcopy

# Create your views here.


def home(request):
    return render(request, "home.html")


@login_required(login_url="login")
def main(request):
    course = Course.objects.all()
    p = Paginator(Course.objects.all(), 4)
    page = request.GET.get('page')
    courses = p.get_page(page)
    if request.method == 'POST':
        link = request.POST['link']
        tag = request.POST['tag']
        tag_result = tag.split(",")
        tag = _parse_tags(request.POST['tag'])
        public = request.POST.get('public', '') == 'on'

        ydl = youtube_dl.YoutubeDL({"ignoreerrors": True, "quiet": True})
        with ydl:
            result = ydl.extract_info(
                link,
                download=False  # We just want to extract the info
            )

        playlist_info = []
        for video in result['entries']:
            video_url = dict((k, video[k])
                             for k in ['title', 'duration', 'webpage_url'] if k in video)
            playlist_info.append(video_url.copy())
        course_result = Course(title=result.get(
            'title'), link=link, public=public)
        course_result.author = request.user
        course_result.save()
        course_result.tags.add(*tag_result)
        print(playlist_info)
        for i in playlist_info:
            title = i.get('title')
            duration = i.get('duration')
            playlist_url = i.get("webpage_url")
            list_store = PlaylistItem(
                list_item=title, time=duration, playlist_title=result.get('title'), link=playlist_url)
            list_store.save()

    course_id = []
    for item in course.iterator():
        course_list = Course.objects.get(id=item.id)
        course_id.append(course_list)

    progress = {}
    for data in course_id:
        global_count = 0
        list_total = PlaylistItem.objects.filter(
            playlist_title=data.title).count()
        list_item = PlaylistItem.objects.filter(playlist_title=data.title)
        for title in list_item.iterator():
            if title.status == "Completed":
                global_count = global_count+1
            if global_count == 0:
                percentage = 0
            else:
                total = global_count
                percentage = 100 * float(total)/float(list_total)
            progress[data.id] = round(percentage)
    request.session['progress'] = progress
   
    
    
    result = {
        "course": course,
        "per": progress,
        "courses": courses
    }

    return render(request, "index.html", result)


@login_required(login_url="login")
def listing(request):
    course = Course.objects.all()

    info = {
        "course": course
    }

    return render(request, "index.html", info)


@login_required(login_url="login")
def tag_listing(request, tags):
    course = Course.objects.all()
    tags = Tag.objects.filter(slug=tags).values_list('name', flat=True)
    posts = course.filter(tags__name__in=tags)
    info = {
        "tags": posts,
    }
    return render(request, "tag.html", info)


@login_required(login_url="login")
def listing(request, id):
    status_data = ["Yet to Start", "In Progress", "On Hold", "Completed"]
    course_list = Course.objects.get(id=id)
    list_item = PlaylistItem.objects.filter(playlist_title=course_list.title)
    request.session['id'] = id

    course_info = {
        "videoDetail": list_item,
        "id": id,
        "overall": status_data
    }

    return render(request, "List.html", course_info)


def handleSignUp(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, "Techhub account was created for" + user)
            return redirect('login')
    return render(request, "signup.html", {"form": form})


def handeLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.info(request, "Username OR Password is incorrect")
    return render(request, "login.html")


def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/')


@login_required(login_url="login")
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            content = form.cleaned_data['content']
            if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(content) < 4:
                messages.error(request, "Please fill the form correctly")
            else:
                contact = Contact(name=name, email=email,
                                  phone=phone, content=content)
                contact.save()
                messages.success(
                    request, "Your message has been successfully sent")
    return render(request, "contact.html")


@login_required(login_url="login")
def search(request):
    query = request.GET['query']
    allCourse = Course.objects.filter(title__icontains=query)
    params = {'allCourse': allCourse}
    return render(request, 'search.html', params)


@login_required(login_url="login")
def editing(request, id):
    course = Course.objects.get(id=id)
    string_var = course.title
    item = PlaylistItem.objects.filter(playlist_title=string_var)
    if request.method == "POST":
        title = request.POST['title']
        course.title = title
        course.save(update_fields=["title"])
        PlaylistItem.objects.filter(playlist_title=string_var).update(
            playlist_title=course.title)
        messages.success(request, "Successfully updated title")
        return redirect('/course')

    return render(request, "edit.html", {"course": course, "id": id})


def getstatus(request, id):
    update_status = PlaylistItem.objects.get(id=id)
    list_id = request.session.get('id')

    if request.method == "POST":
        choice = request.POST['choice']
        update_status.author = request.user
        update_status.status = choice
        update_status.save(update_fields=["status", "author"])

    return redirect('listing', id=list_id)


def clone(request, id):
    course = Course.objects.get(id=id)
    if request.user.id != course.author.id and course.public:
        old_obj = deepcopy(course)
        old_tag = old_obj.tags.all()
        course.id = None
        course.author = request.user
        course.save()
        for tag in old_tag.iterator():
            course.tags.add(tag.name)
    return redirect("main")


def course_csv(request):
    wb = openpyxl.Workbook()
    sheetOne = wb.create_sheet("ListOfPlaylist")
    course = Course.objects.filter(public=False)
    data_view = []
   
    for item in course.iterator():

        if request.user.id == item.author.id:

            progress = request.session.get('progress')
            for i in progress.keys():
                if i.find(str(item.id)) > -1:
                    progress_data = f'{progress[i]} %'
            old_tag = item.tags.all()
            for tag in old_tag.iterator():
                data = (item.title, item.link, tag.name, progress_data)
            
            data_view.append(list(data))
            item_list = [tuple(l) for l in data_view]
            add_tuple = ("Title", "Link", "Tag", "Progress")
            item_list.insert(0, add_tuple)
            
            sheetTwo = wb.create_sheet(item.title)
            per_item = PlaylistItem.objects.filter(playlist_title=item.title)
            playlist_view = []
            for item in per_item.iterator():
                reg = re.compile(r'[\\/:*?"<>|\r\n]+')
                valid_name = reg.findall(item.list_item)
                if valid_name:
                    for nv in valid_name:
                        per_item = item.list_item.replace(nv, " ")
                    playlist_data = (per_item, item.time, item.link, item.status)
                else:
                    playlist_data = (item.list_item, item.time, item.link,item.status)
                playlist_view.append(list(playlist_data))
                item_playlist = [tuple(l) for l in playlist_view]
                add_tuple = ("List", "Time", "Link", "Current Status")
                item_playlist.insert(0, add_tuple)
            
            for i in item_playlist:
                sheetTwo.append(i)
    
    for playlist_item in item_list:
        sheetOne.append(playlist_item)
    wb.remove(wb['Sheet'])
    current_GMT = time.gmtime()

# ts stores timestamp
    ts = calendar.timegm(current_GMT)
    date_time = datetime.fromtimestamp(ts)

# convert timestamp to string in dd-mm-yyyy HH:MM:SS
    str_date_time = date_time.strftime("%d-%m-%Y, %H:%M:%S")
    wb.save(f'{request.user} {str_date_time}.xlsx')
    return redirect("main")


def upload(request):
    if request.method == "POST":
        excel_file = request.FILES["excel_file"]

        wb = openpyxl.load_workbook(excel_file)
        sheets = wb.sheetnames
        excel_data = []
        excel_playlist = list()
        for i in sheets:
            excel_data = []
            work = wb[i]
            
            for row in work.iter_rows():
                row_data = list()
                for cell in row:
                    row_data.append(str(cell.value))
                excel_data.append(row_data)
            excel_data.insert(0, i)
            excel_playlist.append(excel_data)
                
        for item in excel_playlist:
            if ['Title', 'Link', 'Tag', 'Progress'] == item[1]:
                to_exclude = {1}
                data = [element for i, element in enumerate(item) if i not in to_exclude]
                del data[0]
                for item in data:
                    try:
                        old_course = Course.objects.get(title=item[0])
                    except Course.DoesNotExist:
                        old_course = None
                    if old_course:
                        messages.info(request, "course is already present in List of playlist")
                    else:
                        course = Course.objects.create(author=request.user, title=item[0], link=item[1], public=True)
                        course.tags.add(item[2])
                        course.save()
            elif ['List', 'Time', 'Link', 'Current Status'] == item[1]:
                exclude = {1}
                playlist_data = [element for i, element in enumerate(item) if i not in exclude]
                title = playlist_data[0]
                del playlist_data[0]
                for item in playlist_data:
                    playlist = PlaylistItem.objects.create(
                                list_item=item[0], time=item[1], link=item[2], author=request.user, status="", playlist_title=title)
                    playlist.save()
            else:
                messages.info(request, "Format of excel sheet not meet as expected please Go through the sample excel file for correct format")
      
        return redirect(main)
            
    return render(request, 'upload.html')


def download(request):
    filename = "sample.xlsx" # this is the file people must download
    with open(filename, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=' + filename
        response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-16'
        return response
