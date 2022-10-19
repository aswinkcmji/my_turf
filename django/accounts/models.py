from ftplib import MAXLINE
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserModel(AbstractUser):
    location = models.CharField(max_length=200)
    phone = models.CharField(max_length=16)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=10)
    avatar = models.ImageField()
    turf_name= models.CharField(max_length=255, blank=True)
    catagory = ArrayField(models.CharField(max_length=512, default=None), default=None)
    is_turf = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
