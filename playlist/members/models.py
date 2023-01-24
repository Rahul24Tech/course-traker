from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=100)
    content = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return "Message from " + self.name + " - " + self.email
    
    
class Profile(models.Model):
    OPTIONS = (
        ("H", "Hours"),
        ("M", "Minutes"),
        ("S", "Seconds"),
    )

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/Profile/")
    website_url = models.CharField(max_length=255, null=True, blank=True)
    facebook_url = models.CharField(max_length=255, null=True, blank=True)
    time_preference = models.CharField(max_length=100, choices=OPTIONS)

    def get_absolute_url(self):
        return reverse("course_video:home")