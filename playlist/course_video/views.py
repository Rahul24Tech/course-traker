from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from taggit.utils import _parse_tags

from .models import *
from .forms import CreateUserForm, ContactForm

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
        # import pdb 
        # pdb.set_trace()
        course_result.author =request.user
        course_result.save()
        course_result.tags.add(*tag_result)
        print(playlist_info)
        for i in playlist_info:
            title = i.get('title')
            duration = i.get('duration')
            list_store = PlaylistItem(list_item=title, time=duration, playlist_title=result.get('title'))
            # list_store.city = course_result.title
            # Course.objects.distinct().filter(toy__name__icontains='star')
            # p = Course.objects.filter(city__title=result.get('title'))
            list_store.save()


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
    import pdb
    pdb.set_trace()
    course_list = Course.objects.get(id=id)
    list_item = PlaylistItem.objects.filter(playlist_title=course_list.title)
    # destination = get_object_or_404(Course, id=id)
    # if course_list.id == destination.id:
    # #     Item = PlaylistItem.objects.get(id=course_list.id)
    #     Item = PlaylistItem.objects.filter(city__in=Course.objects.filter(id=course_list.id))


    # for i in Item.iterator():
    #     print(i)   
    
    # context = {
    #     'destination': destination,
    # }
    # parents_id_that_have_childs = PlaylistItem.objects.filter(parent_id__isnull=False).values_list('playlist_id', flat=True)

    # parents = Course.objects.filter(id__in=list(set(parents_id_that_have_childs)))

    # playlist = PlaylistItem.objects.get(id=course_list.id)
    # link = course_list.link
    # ydl = youtube_dl.YoutubeDL({"ignoreerrors": True, "quiet": True})
    # with ydl:
    #     result = ydl.extract_info(
    #         link,
    #         download=False  # We just want to extract the info
    #     )
    # playlist_info = []
    # print(result)
    # for video in result['entries']:
    #     video_url = dict((k, video[k])
    #                      for k in ['title', 'duration'] if k in video)
    #     playlist_info.append(video_url.copy())

    # import pdb
    # pdb.set_trace()
    
    status = Status.objects.all()
    course_info = {
        "videoDetail": list_item,
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
