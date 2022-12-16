from django.shortcuts import render, HttpResponse, redirect, get_list_or_404
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from taggit.models import Tag
from taggit.utils import _parse_tags
from .models import *
from .forms import CreateUserForm

import youtube_dl

# Create your views here.

def home(request):
    return render(request, "home.html")

@login_required(login_url="login")
def main(request):
    course = Course.objects.all()
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
                             for k in ['title', 'duration'] if k in video)
            playlist_info.append(video_url.copy())
        course_result = Course(title=result.get('title'), link=link, public=public)
        course_result.author =request.user
        course_result.save()
        course_result.tags.add(*tag_result)

    result = {
        "course": course,
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

    course_list = Course.objects.get(id=id)
    link = course_list.link
    ydl = youtube_dl.YoutubeDL({"ignoreerrors": True, "quiet": True})
    with ydl:
        result = ydl.extract_info(
            link,
            download=False  # We just want to extract the info
        )
    playlist_info = []
    print(result)
    for video in result['entries']:
        video_url = dict((k, video[k])
                         for k in ['title', 'duration'] if k in video)
        playlist_info.append(video_url.copy())

    print(playlist_info)

    status = Status.objects.all()
    course_info = {
        "videoDetail": playlist_info,
        "status": status
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
            # return render(request, "login.html")
    return render(request, "login.html")

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/')

@login_required(login_url="login")
def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
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
    query=request.GET['query']
    allCourse= Course.objects.filter(title__icontains=query)
    params={'allCourse': allCourse}
    return render(request, 'search.html', params)

@login_required(login_url="login")
def editing(request, id):
    course = Course.objects.get(id=id)
    if request.method == "POST":
        title = request.POST['title']
        course.title = title
        course.save(update_fields=["title"])
        messages.success(request, "Successfully updated title")
        return redirect('/course')
        
    return render(request, "edit.html", {"course": course, "id":id})
