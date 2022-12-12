from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import user_passes_test
import youtube_dl

# Create your views here.

def detail(request):
    course = Course.objects.all()
    result = {
        "course": course,
    }
    print(result)
    return render(request, "index.html", result)


def playList(request):
        ydl = youtube_dl.YoutubeDL({"ignoreerrors": True, "quiet": True})

        with ydl:
            result = ydl.extract_info(
            "https://www.youtube.com/watch?v=7wnove7K-ZQ&list=PLu0W_9lII9agwh1XjRt242xIpHhPT2llg",
            download=False # We just want to extract the info
        )

        playlist_info = []
        import pdb
        pdb.set_trace()
        print(result)
        for video in result['entries']:
            # print(video)
            video_url = dict((k, video[k]) for k in ['title', 'duration'] if k in video)
            playlist_info.append(video_url.copy())
            
        
        print(playlist_info)

        status = Status.objects.all()
        info={
                "videoDetail": playlist_info,
                "status": status
            }
    

        return render(request, "List.html", info)


def admin_check(user):
   return user.is_superuser


@user_passes_test(admin_check)
def main(request):
    if request.method == 'POST':
        # import pdb
        # pdb.set_trace()
        # title = request.POST['title']
        link = request.POST['link']
        
        ydl = youtube_dl.YoutubeDL({"ignoreerrors": True, "quiet": True})

        with ydl:
            result = ydl.extract_info(
                link,
                    download=False # We just want to extract the info
        )

        playlist_info = []
        for video in result['entries']:
            # print(video)
            video_url = dict((k, video[k]) for k in ['title', 'duration'] if k in video)
            playlist_info.append(video_url.copy())
            
        
        print(playlist_info)
        course_result = Course(title=result.get('title'), link=link)
        course_result.save()
        
        # status = Status.objects.all()
        info={
                "course": course
            }

    return render(request, "index.html", info)
