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
    avatar = models.ImageField( null=True , upload_to='images/avatar')
    turf_name= models.CharField(max_length=255, null=True)
    category = ArrayField(models.CharField(max_length=512, null=True) , null=True, default=list, blank=True) 
    landmark = models.CharField(max_length=255, null=True)
    is_turf = models.BooleanField(default=False )
    current_location=models.CharField(max_length=200,null=True,blank=True)


    USERNAME_FIELD = 'username'
