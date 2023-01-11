from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_time_in_sec(context):
    """
    This function takes context data of current loaded template tags html page reference and return time value in seconds

    return - second_value in seconds format
    """
    course = context["course_title"]
    seconds_value = {}
    for item in course:
        time = item.time_left
        seconds_value[item.title] = time
    print(seconds_value)
    return seconds_value


@register.filter
def time_conversion(second, time_preference):
    """
    This function takes second , time_preference and convert seconds value into given preference i.e:-H,M,S

    Args:-
        second(sec)- this contain the time in seconds form
        time_preference(string)- It is the preference given by the user in which format they want to show time_left field.
    """
    if time_preference == "H":
        second = second % (24 * 3600)
        hour = second // 3600
        return hour
    elif time_preference == "M":
        second %= 3600
        minutes = second // 60
        return minutes
    else:
        second %= 60
        return second
