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
    # tags = TaggableManager()

    def __str__(self):
        return self.title

class Status(models.Model):
    status = models.CharField(max_length=50)
    