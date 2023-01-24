from django import forms
from django.contrib.auth.forms import UserChangeForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Contact
from .models import Profile


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"
        
        

class EditProfileForm(UserChangeForm):
    email = forms.EmailField(
        max_length=100, widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    first_name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    username = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_login = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    is_superuser = forms.CharField(
        max_length=100, widget=forms.CheckboxInput(attrs={"class": "form-control"})
    )
    is_active = forms.CharField(
        max_length=100, widget=forms.CheckboxInput(attrs={"class": "form-control"})
    )
    is_staff = forms.CharField(
        max_length=100, widget=forms.CheckboxInput(attrs={"class": "form-control"})
    )
    date_joined = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "username",
            "last_login",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
        )


class ProfilePageForm(forms.ModelForm):
    OPTIONS = (
        ("H", "Hours"),
        ("M", "Minutes"),
        ("S", "Seconds"),
    )
    time_preference = forms.ChoiceField(
        required=False,
        choices=OPTIONS,
    )

    class Meta:
        model = Profile
        fields = (
            "bio",
            "profile_pic",
            "website_url",
            "facebook_url",
            "time_preference",
        )

        widgets = {
            "bio": forms.Textarea(attrs={"class": "form-control"}),
            "website_url": forms.TextInput(attrs={"class": "form-control"}),
            "facebook_url": forms.TextInput(attrs={"class": "form-control"}),
        }


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]