from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Contact, Course, Profile
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
        
        
class EditProfileForm(UserChangeForm):
    email = forms.EmailField(max_length=100,widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_login = forms.CharField(max_length=100,widget=forms.TextInput(attrs={"class":"form-control"}))
    is_superuser = forms.CharField(max_length=100,widget=forms.CheckboxInput(attrs={"class":"form-control"}))
    is_active = forms.CharField(max_length=100,widget=forms.CheckboxInput(attrs={"class":"form-control"}))
    is_staff = forms.CharField(max_length=100,widget=forms.CheckboxInput(attrs={"class":"form-control"}))
    date_joined = forms.CharField(max_length=100,widget=forms.TextInput(attrs={"class":"form-control"}))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'username', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined')
        
        
class ProfilePageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'profile_pic', 'website_url', 'facebook_url')
        # OPTIONS = (
        # ("H", "Hours"),
        # ("M", "Minutes"),
        # ("S", "Seconds"),
        # )
        
        widgets = {
            'bio': forms.Textarea(attrs={"class":"form-control"}),
            # 'profile_pic': forms.FileInput(attrs = {"id" : "image_field" }),
            'website_url': forms.TextInput(attrs={"class":"form-control"}),
            'facebook_url': forms.TextInput(attrs={"class":"form-control"})
            
        }
        
        
class TimePreferenceForm(forms.Form):
        OPTIONS = (
            ("H", "Hours"),
            ("M", "Minutes"),
            ("S", "Seconds"),
        )
        time_preference = forms.MultipleChoiceField(
                                    required=False,
                                    widget=forms.CheckboxSelectMultiple,
                                    choices=OPTIONS,
                                )
            # 'bio': forms.Textarea(attrs={"class":"form-control"}),
            # # 'profile_pic': forms.FileInput(attrs = {"id" : "image_field" }),
            # 'website_url': forms.TextInput(attrs={"class":"form-control"}),
            # 'facebook_url': forms.TextInput(attrs={"class":"form-control"})
            
        