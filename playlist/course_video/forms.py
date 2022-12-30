from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Contact


class CreateUserForm(UserCreationForm):
    class Meta:
        model =User
        fields=['username','email','password1','password2']
        
        
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"
        
        
class StatusForm(forms.Form):
    STATUS_CHOICES =(
    ("Yet to Start", "Yet to Start"),
    ("In Progress", "In Progress"),
    ("On Hold", "On Hold"),
    ("Completed", "Completed"),)
    status = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=STATUS_CHOICES)