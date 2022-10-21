from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.
# class MatchModel(models.Model):
#     category = models.CharField(max_length=30,null=False,blank=False)


# class slotModel(models.Model):
#     category = models.CharField(max_length=50, blank=False,null=False)
#     location = models.CharField(max_length=200,)
#     creator = models.CharField(max_length=150, blank=False,null=False)
#     nos = models.IntegerField()                                                                       #nos = number of slots
#     avs = models.IntegerField()                                                                       #avs=available slots
#     time = models.DateTimeField()
#     date = models.DateTimeField()
#     status = models.BooleanField(default=False)


class createMatchModel(models.Model):
    category = models.CharField(max_length=50, blank=False,null=False)
    location =  models.CharField(max_length=200, blank=False,null=False)
    date = models.CharField(max_length=200, blank=False)
    time = models.CharField(max_length=200, blank=False)
    slots = models.IntegerField(default=0) 

class MatchModel(models.Model):
    category = models.CharField(max_length=50, blank=False,null=False)
    location =  models.CharField(max_length=200, blank=False,null=False)
    creator = models.CharField(max_length=150, blank=False,null=False)
    date = models.DateTimeField()
    time = models.DateTimeField()
    slots = models.IntegerField(default=0) 
    avs = models.IntegerField()
    status = models.BooleanField(default=False)
    
