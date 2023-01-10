from django import template
from playlist.course_video.models import Course, PlaylistItem

register = template.Library()

@register.inclusion_tag("user_profile.html", takes_context=True)
def gettime(params):
    # import pdb
    # pdb.set_trace()
    user = params.user

    queryset_item = []
    course = Course.objects.all()
    for item in course:
        filtered_data = PlaylistItem.objects.filter(author=user).filter(playlist_title=item.title)
        queryset_item.append(filtered_data)
    queryset_list = [queryset for queryset in queryset_item if queryset]
    course_time = {}
    response_time = {}
    completed_time = []
    total_time = []
    for item in queryset_list:
        for data in item:
            total_time.append(data.time)
            if data.status == "Completed":
                completed_time.append(data.time)
        course_time["completed"]=sum(completed_time)
        course_time["total"]=sum(total_time)
        course_time["title"]=data.playlist_title
        time_left = course_time["total"]-course_time["completed"]
        response_time[course_time["title"]]=time_left
    print(response_time)
