from django.db import models
import uuid
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.utils import timezone
from django.urls import reverse

# Create your models here.


class Course(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null="true")
    title = models.CharField(max_length=100)
    link = models.URLField(max_length=200, blank="true")
    tags = TaggableManager()
    public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def days_since_creations(self):
        diff = timezone.now() - self.created_at
        return diff.days

    @property
    def time_left(self):
        completed_item = self.playlistitem_set.filter(status="Completed")
        all_item = self.playlistitem_set.all()
        completed_time = [item.time for item in completed_item]
        total_time = [item.time for item in all_item]
        time = sum(total_time) - sum(completed_time)
        return time


class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=100)
    content = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return "Message from " + self.name + " - " + self.email


class PlaylistItem(models.Model):
    list_item = models.CharField(max_length=150)
    time = models.IntegerField(null=True, blank=True)
    link = models.URLField(max_length=200, blank="true")
    author = models.ForeignKey(User, on_delete=models.CASCADE, null="true")
    status = models.CharField(max_length=50, default="Yet To Start")
    playlist = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.list_item


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
        return reverse("home")
