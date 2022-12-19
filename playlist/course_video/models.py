from django.db import models
import uuid
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
# Create your models here.

class Course(models.Model):
    course_id = models.UUIDField(
     primary_key = True,
     default = uuid.uuid4,
     editable = False),
    author = models.ForeignKey(User, on_delete=models.CASCADE, null='true')
    title = models.CharField(max_length=100)
    link = models.URLField(max_length=200, blank='true')
    tags = TaggableManager()
    public = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.title


class Status(models.Model):
    STATUS_CHOICES =(
    ("1", "Yet to Start"),
    ("2", "In Progress"),
    ("3", "On Hold"),
    ("4", "Completed"),)
    status = models.CharField(max_length=1, choices = STATUS_CHOICES)
    
    def __str__(self) -> str:
        return self.status
    
    
    
class Contact(models.Model):
     sno= models.AutoField(primary_key=True)
     name= models.CharField(max_length=255)
     phone= models.CharField(max_length=13)
     email= models.CharField(max_length=100)
     content= models.TextField()
     timeStamp=models.DateTimeField(auto_now_add=True, blank=True)

     def __str__(self):
          return "Message from " + self.name + ' - ' + self.email   
      
      
      
class PlaylistItem(models.Model):
    
    
    playlist_id = models.UUIDField(
     primary_key = True,
     default = uuid.uuid4,
     editable = False),
    list_item = models.CharField(max_length=150)
    time = models.IntegerField()
    
    playlist_title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.list_item