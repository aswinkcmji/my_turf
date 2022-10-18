from email.policy import default
from django.db import models

# Create your models here.
class MatchModel(models.Model):
    category = models.CharField(max_length=30,null=False,blank=False)
    date= models.CharField(max_length=30,null=True,blank=False)
    time= models.CharField(max_length=30,null=True,blank=False)
    locality = models.CharField(max_length=30,null=True,blank=False)
    creator = models.CharField(max_length=30,null=True,blank=False)
    status = models.CharField(default="Upcoming",max_length=30,null=False,blank=False)
    slots =models.IntegerField(default=1,null=False,blank=False)
    is_slot_available =models.BooleanField(default = True,null=False,blank=False)