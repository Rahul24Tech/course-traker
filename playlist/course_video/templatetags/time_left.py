from django import template
from course_video.models import Course, PlaylistItem

register = template.Library()

@register.inclusion_tag("user_profile.html", takes_context=True)
def gettime(context):
    
    profile = context['page_user']
    # import pdb
    # pdb.set_trace()
    queryset_item = []
    course = Course.objects.all()
    for item in course:
        filtered_data = PlaylistItem.objects.filter(author=profile.user.id).filter(playlist_title=item.title)
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
    Hours_title = {}
    Second_title = {}
    Minute_title = {}
    for title,duration_sec in response_time.items():
        if profile.time_preference == 'H':
            hours = (duration_sec - ( duration_sec % 3600))/3600
            Hours_title[title]=hours
            # return Hours_title
        elif profile.time_preference == 'M':
            hours = (duration_sec - ( duration_sec % 3600))/3600
            seconds_minus_hours = (duration_sec - hours*3600)
            minutes = (seconds_minus_hours - (seconds_minus_hours % 60) )/60
            Minute_title[title]=minutes
        else:
            hours = (duration_sec - ( duration_sec % 3600))/3600
            seconds_minus_hours = (duration_sec - hours*3600)
            seconds = seconds_minus_hours - minutes*60
            Second_title[title]=seconds
    # import pdb
    # pdb.set_trace()
    print(Hours_title)
    print(Minute_title)
    print(Second_title)
    
    return {"Hours_title":Hours_title}, {"Minute_title":Minute_title}, {"Second_title":Second_title}
