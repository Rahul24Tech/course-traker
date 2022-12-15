from django.shortcuts import render, HttpResponse, redirect, get_list_or_404
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from taggit.models import Tag
from .models import *

import youtube_dl

# Create your views here.
def home(request):
    # users_in_group = Group.objects.get(name="group name").user_set.all()
    # course = Course.objects.all()
    # playlist_info = []
    # playlist_link = []
    # for i in range(0, len(course)):
        
    #     ydl = youtube_dl.YoutubeDL({"ignoreerrors": True, "quiet": True})
    #     link = course.values('link')[i].get('link')
    #     with ydl:
    #         result = ydl.extract_info(
    #         link,
    #         download=False  # We just want to extract the info
    #         )
    
    
    #     for video in result['entries']:
    #     # print(video)
    #         video_url = dict((k, video[k])
    #                      for k in ['thumbnails'] if k in video)
    #         playlist_info.append(video_url.copy())
        
    #     for video_info in result['entries']:
    #         video_url_info = dict((k, video_info[k])
    #                      for k in ['title','duration'] if k in video_info)
    #         playlist_link.append(video_url_info.copy())
    
    # for j in range(len(playlist_info)):
    #     link = playlist_info[j].get('thumbnails')
    #     img_url = [li['url'] for li in link]
    
    # result = {
    #     # "course": course,
    #     "videoInfo": playlist_link,
    #     "image": img_url,
    #     "link": link
    # }
    return render(request, "home.html")


def main(request):
    course = Course.objects.filter(author=request.user).all()
    # users_in_group = Group.objects.get(name="Editor").user_set.all()
    result = {
        "course": course,
        # "user": users_in_group
    }
    print(result)
    return render(request, "index.html", result)


def listing(request):
    # import pdb
    # pdb.set_trace()
    course = Course.objects.all()
    # users_in_group = Group.objects.get(name="Editor").user_set.all()
    # user = User.objects.get(username=request.user.username, pk= request.user.id)
    team = Course.objects.filter(author=request.user).all()
    info = {
        "course": course,
        "user_info": team
    }

    return render(request, "index.html", info)


def tag_listing(request, tags):
    course = Course.objects.filter(author=request.user).all()
    tags = Tag.objects.filter(slug=tags).values_list('name', flat=True)
    posts = course.filter(tags__name__in=tags)
    info = {
        "tags": posts,
    }

    return render(request, "tag.html", info)


def listing(request, id):

    course_list = Course.objects.get(id=id)
    link = course_list.link
    # home(link)
    ydl = youtube_dl.YoutubeDL({"ignoreerrors": True, "quiet": True})
    with ydl:
        result = ydl.extract_info(
            link,
            download=False  # We just want to extract the info
        )
    playlist_info = []
    print(result)
    for video in result['entries']:
        # print(video)
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


def techHubHome(request):
    if request.method == 'POST':
        link = request.POST['link']
        tag = request.POST['tag']
        public = request.POST.get('public', '') == 'on'

        # import pdb
        # pdb.set_trace()
        # # course = Course.objects.all()
        # # users_in_group = Group.objects.get(name="Editor").user_set.all()
        # user = User.objects.get(username=request.user.username, pk= request.user.id)
    
        ydl = youtube_dl.YoutubeDL({"ignoreerrors": True, "quiet": True})

        with ydl:
            result = ydl.extract_info(
                link,
                download=False  # We just want to extract the info
            )

        playlist_info = []
        for video in result['entries']:
            # print(video)
            video_url = dict((k, video[k])
                             for k in ['title', 'duration'] if k in video)
            playlist_info.append(video_url.copy())

        print(playlist_info)
        course_result = Course(title=result.get('title'), link=link, public=public)
        course_result.author =request.user
        course_result.save()
        course_result.tags.add(tag)

        return render(request, "index.html")


def handleSignUp(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check for errorneous input
        if len(username) < 10:
            messages.error(
                request, " Your user name must be under 10 characters")
            return redirect('/')

        if not username.isalnum():
            messages.error(
                request, " User name should only contain letters and numbers")
            return redirect('/')
        if (pass1 != pass2):
            messages.error(request, " Passwords do not match")
            return redirect('/')

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        group = Group.objects.get(name='Editor')
        myuser.groups.add(group)
        messages.success(
            request, " Your TechHub account has been successfully created")
        return redirect('/')

    else:
        return HttpResponse("404 - Not found")


def handeLogin(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("/")

    return HttpResponse("404- Not found")


def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/')


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


def search(request):
    query=request.GET['query']
    allCourse= Course.objects.filter(title__icontains=query)
    params={'allCourse': allCourse}
    return render(request, 'search.html', params)

def editing(request, id):
    course = Course.objects.get(id=id)
    if request.method == "POST":
        title = request.POST['title']
        course.title = title
        course.save(update_fields=["title"])
        messages.success(request, "Successfully updated title")
        return redirect('/course')
        
    return render(request, "edit.html", {"course": course, "id":id})
