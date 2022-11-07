from email.policy import default
from unicodedata import category
from django.db import models
from unittest.util import _MAX_LENGTH
from datetime import datetime,timedelta
from dashboard.models import CategoriesModel
# Create your models here.


   
class MatchModel(models.Model):
    category = models.ForeignKey(CategoriesModel, on_delete=models.CASCADE)
    date= models.DateField(blank=True)
    start_time= models.DateTimeField(max_length=30,default=datetime.now(),blank=True)
    end_time= models.DateTimeField(max_length=30,default=datetime.now(),blank=True)
    locality = models.CharField(max_length=30,null=True,blank=False)
    creator = models.CharField(max_length=30,null=True,blank=False)
    status = models.CharField(default="Upcoming",max_length=30,null=False,blank=False)
    slots =models.IntegerField(default=2,null=False,blank=False)
    slot_available =models.IntegerField(default = 1,null=False,blank=False)
    cron =models.IntegerField(default = 1,null=True,blank=False)


class RequestModel(models.Model):
    match_id = models.ForeignKey(MatchModel, on_delete=models.CASCADE)
    category=models.ForeignKey(CategoriesModel, on_delete=models.CASCADE)
    username=models.CharField(max_length=30,null=False,blank=False)
    phoneno=models.CharField(max_length=16,default=7414414141)
    status=models.CharField(default="Pending",max_length=30,null=False,blank=False)
    date= models.DateField(blank=True)
    start_time= models.TimeField(default=datetime.now().strftime('%H:%M:%S'),blank=True)
    end_time= models.TimeField(default=datetime.now().strftime('%H:%M:%S'),blank=True)
    locality = models.CharField(max_length=30,null=True,blank=False)

    
class TournamentModel(models.Model):
    category = models.CharField(max_length=30,null=False,blank=False)
    start_date= models.DateField(blank=True)
    end_date= models.DateField(blank=True) 
    start_time= models.TimeField(default=datetime.now().strftime('%H:%M:%S'),blank=True)
    end_time= models.TimeField(default=datetime.now().strftime('%H:%M:%S'),blank=True)
    locality = models.CharField(max_length=30,null=True,blank=False)
    creator = models.CharField(max_length=30,null=True,blank=False)
    status = models.CharField(default="Upcoming",max_length=30,null=False,blank=False)
    teams =models.IntegerField(default=1,null=False,blank=False)
    team_space_available =models.IntegerField(default = 1,null=False,blank=False)

class TournamentRequestModel(models.Model):
    tournament_id = models.ForeignKey(MatchModel, on_delete=models.CASCADE)
    category=models.CharField(max_length=30,null=False,blank=False)
    username=models.CharField(max_length=30,null=False,blank=False)
    # phoneno=models.CharField(max_length=16,default=7414414141)
    status=models.CharField(default="Pending",max_length=30,null=False,blank=False)
    start_date= models.DateField(blank=True)
    end_date= models.DateField(blank=True) 
    start_time= models.TimeField(default=datetime.now().strftime('%H:%M:%S'),blank=True)
    end_time= models.TimeField(default=datetime.now().strftime('%H:%M:%S'),blank=True)
    locality = models.CharField(max_length=30,null=True,blank=False)

# class CreateTeamModel(models.Model):
#     Name = models.CharField(max_length=30,blank=False,null=False)





    # def __str__(self):
    #     return str(self.category)