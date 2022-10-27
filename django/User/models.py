from email.policy import default
from unicodedata import category
from django.db import models
from unittest.util import _MAX_LENGTH
from datetime import datetime,timedelta

# Create your models here.
class MatchModel(models.Model):
    category = models.CharField(max_length=30,null=False,blank=False)
    date= models.DateField(blank=True)
    start_time= models.TimeField(default=datetime.now().strftime('%H:%M:%S'),blank=True)
    end_time= models.TimeField(default=datetime.now().strftime('%H:%M:%S'),blank=True)
    locality = models.CharField(max_length=30,null=True,blank=False)
    creator = models.CharField(max_length=30,null=True,blank=False)
    status = models.CharField(default="Upcoming",max_length=30,null=False,blank=False)
    slots =models.IntegerField(default=1,null=False,blank=False)
    slot_available =models.IntegerField(default = 1,null=False,blank=False)


class RequestModel(models.Model):
    match_id = models.ForeignKey(MatchModel, on_delete=models.CASCADE)
    category=models.CharField(max_length=30,null=False,blank=False)
    username=models.CharField(max_length=30,null=False,blank=False)
    phoneno=models.CharField(max_length=16,default=7414414141)
    status=models.CharField(default="Pending",max_length=30,null=False,blank=False)
    date= models.DateField(blank=True)
    start_time= models.TimeField(default=datetime.now().strftime('%H:%M:%S'),blank=True)
    end_time= models.TimeField(default=datetime.now().strftime('%H:%M:%S'),blank=True)
    locality = models.CharField(max_length=30,null=True,blank=False)



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

class creatematchModel(models.Model):
    category = models.CharField(max_length=50, blank=False,null=False)
    location =  models.CharField(max_length=200, blank=False,null=False)
    creator = models.CharField(max_length=150, blank=False,null=False)
    date = models.DateTimeField()
    time = models.DateTimeField()
    nos = models.IntegerField() #nos = number of slots
    avs = models.IntegerField()
    status = models.BooleanField(default=False)


    
