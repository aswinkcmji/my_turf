from email.policy import default
from enum import unique
from unicodedata import category
from unittest.util import _MAX_LENGTH
from django.db import models
from django.forms import CharField
from accounts.models import UserModel




# Create your models here.

class TurfScheduleModel(models.Model):
    category = models.CharField(max_length=255, default="none")
    title = models.CharField(max_length=255)
    start = models.CharField(max_length=255)
    end = models.CharField(max_length=255)
    color_txt = models.CharField(max_length=255, null=True)
    color_bg = models.CharField(max_length=255, null=True)
    turf = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    
class GalleryImg(models.Model):
    username = models.TextField( max_length=55)
    image = models.ImageField( null=True , upload_to='image/image')
    caption = models.TextField( max_length=55)