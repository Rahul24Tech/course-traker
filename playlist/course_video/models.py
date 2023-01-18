from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager

# Create your models here.


class Course(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null="true")
    title = models.CharField(max_length=100)
    link = models.URLField(max_length=200, blank="true")
    tags = TaggableManager()
    public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    favourites = models.ManyToManyField(
        User, related_name="favourite", blank=True, default=None
    )
    watch_later = models.ManyToManyField(
        User, related_name="watch_later", blank=True, default=None
    )

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


class PlaylistItem(models.Model):
    list_item = models.CharField(max_length=150)
    time = models.IntegerField(null=True, blank=True)
    link = models.URLField(max_length=200, blank="true")
    author = models.ForeignKey(User, on_delete=models.CASCADE, null="true")
    status = models.CharField(max_length=50, default="Yet To Start")
    playlist = models.ForeignKey(Course, on_delete=models.CASCADE)
    watch_later_playlist = models.ManyToManyField(
        User, related_name="watch_later_playlist", blank=True, default=None
    )

    def __str__(self):
        return self.list_item
