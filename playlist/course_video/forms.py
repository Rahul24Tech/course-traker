from django import forms

from .models import Course
from .tasks import send_mail_func


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["link", "tags", "public"]
        labels = {"link": "Video Link", "tag": "Tag", "public": "IsPublic"}

    def send_email(self):
        send_mail_func.delay()
