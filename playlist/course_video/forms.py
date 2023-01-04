from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Contact, Course
from .tasks import send_mail_func


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["link", "tags", "public"]
        labels = {"link": "Video Link", "tag": "Tag", "public": "IsPublic"}

    def send_email(self):
        send_mail_func.delay()
