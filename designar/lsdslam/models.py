from __future__ import unicode_literals

from django.db import models

def content_file_name(instance, filename):
    return '/'.join(['videos', instance.name])

# Create your models here.
class Video(models.Model):
    videofile = models.FileField(upload_to=content_file_name)
    name = models.CharField(max_length=200)



