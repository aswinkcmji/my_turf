from email.policy import default
from unicodedata import category
from django.db import models

# Create your models here.
class MatchModel(models.Model):
    category = models.CharField(max_length=30,null=False,blank=False)
    date= models.CharField(max_length=30,null=True,blank=True)
    time= models.CharField(max_length=30,null=True,blank=True)
    locality = models.CharField(max_length=30,null=True,blank=False)
    creator = models.CharField(max_length=30,null=True,blank=False)
    status = models.CharField(default="Upcoming",max_length=30,null=False,blank=False)
    slots =models.IntegerField(default=1,null=False,blank=False)
    slot_available =models.IntegerField(default = 1,null=False,blank=False)


class RequestModel(models.Model):
    match_id = models.ForeignKey(MatchModel, on_delete=models.CASCADE)
    category=models.CharField(max_length=30,null=False,blank=False)
    username=models.CharField(max_length=30,null=False,blank=False)
    phoneno=models.IntegerField(default=1,null=False,blank=False)
    status=models.CharField(default="Pending",max_length=30,null=False,blank=False)
    date= models.CharField(max_length=30,null=True,blank=False)
    time= models.CharField(max_length=30,null=True,blank=False)
    locality = models.CharField(max_length=30,null=True,blank=False)