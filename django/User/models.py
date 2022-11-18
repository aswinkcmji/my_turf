from email.policy import default
from unicodedata import category
from django.db import models
from unittest.util import _MAX_LENGTH
from datetime import datetime,timedelta
from dashboard.models import CategoriesModel
from accounts.models import UserModel
from django.contrib.postgres.fields import ArrayField
# Create your models here.


   
class MatchModel(models.Model):
    category = models.ForeignKey(CategoriesModel, on_delete=models.CASCADE)
    date= models.DateField(blank=True)
    start_time= models.DateTimeField(max_length=30,default=datetime.now(),blank=True)
    end_time= models.DateTimeField(max_length=30,default=datetime.now(),blank=True)
    locality = models.CharField(max_length=50,null=True,blank=False)
    city=models.CharField(max_length=100,null=True,blank=False)
    creator = models.CharField(max_length=30,null=True,blank=False)
    status = models.CharField(default="Upcoming",max_length=30,null=False,blank=False)
    slots =models.IntegerField(default=2,null=False,blank=False)
    slot_available =models.IntegerField(default = 1,null=False,blank=False)
    cron =models.IntegerField(default = 1,null=True,blank=False)



class RequestModel(models.Model):
    match_id = models.ForeignKey(MatchModel, on_delete=models.CASCADE)
    category=models.ForeignKey(CategoriesModel, on_delete=models.CASCADE)
    username=models.ForeignKey(UserModel, on_delete=models.CASCADE)
    phoneno=models.CharField(max_length=16,default=7414414141)
    status=models.CharField(default="Pending",max_length=30,null=False,blank=False)
    date= models.DateField(blank=True)
    start_time= models.TimeField(default=datetime.now().strftime('%H:%M:%S'),blank=True)
    end_time= models.TimeField(default=datetime.now().strftime('%H:%M:%S'),blank=True)
    locality = models.CharField(max_length=50,null=True,blank=False)

    
class TournamentModel(models.Model):
    category = models.ForeignKey(CategoriesModel, on_delete=models.CASCADE)
    # team_name =  models.ForeignKey('User.CreateTeamModel', on_delete=models.CASCADE)
    team_name = models.CharField(max_length=30,null=True,blank=False)
    start_date= models.DateField(blank=True)
    end_date= models.DateField(blank=True) 
    start_time= models.DateTimeField(max_length=30,default=datetime.now(),blank=True)
    end_time= models.DateTimeField(max_length=30,default=datetime.now(),blank=True)
    locality = models.CharField(max_length=30,null=True,blank=False)
    creator = models.CharField(max_length=30,null=True,blank=False)
    status = models.CharField(default="Upcoming",max_length=30,null=False,blank=False)
    teams =models.IntegerField(default=1,null=False,blank=False)
    team_space_available =models.IntegerField(default = 1,null=False,blank=False)

    # start_time= models.DateTimeField(default=datetime.now().strftime('%H:%M:%S'),blank=True)
    # end_time= models.DateTimeField(default=datetime.now().strftime('%H:%M:%S'),blank=True)
class TournamentRequestModel(models.Model):
    tournament_id = models.ForeignKey(TournamentModel, on_delete=models.CASCADE)
    category=models.ForeignKey(CategoriesModel, on_delete=models.CASCADE)
    # team_name =  models.ForeignKey("CreateTeamModel", on_delete=models.CASCADE)
    team_name = models.CharField(max_length=30,null=True,blank=False)
    username=models.CharField(max_length=30,null=False,blank=False)
    phoneno=models.CharField(max_length=16,default=7414414141)
    status=models.CharField(default="Pending",max_length=30,null=False,blank=False)
    start_date= models.DateField(blank=True)
    end_date= models.DateField(blank=True) 
    start_time= models.TimeField(default=datetime.now().strftime('%H:%M:%S'),blank=True)
    end_time= models.TimeField(default=datetime.now().strftime('%H:%M:%S'),blank=True)
    locality = models.CharField(max_length=30,null=True,blank=False)

class CreateTeamModel(models.Model):
    team_name = models.CharField(max_length=30,blank=False,null=False)
    # category=models.ForeignKey(CategoriesModel, on_delete=models.CASCADE)
    # members=models.IntegerField()
    # # tournament_id=models.ForeignKey(TournamentModel, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.team_name)



class TurfCommentsModel(models.Model):
    turf = models.ForeignKey(UserModel, on_delete=models.CASCADE , related_name='turf')
    commenter = models.ForeignKey(UserModel, on_delete=models.CASCADE , related_name='commenter')
    comment = models.CharField(max_length=1000,null=False,blank=False)
    likes_count = models.IntegerField(default=0, null=False)
    date = models.DateTimeField(max_length=30,default=datetime.now())
    liked_users = ArrayField(models.CharField(max_length=512, null=False) , null=False, default=list) 


class CitiesModel(models.Model):
    name=models.CharField(max_length=100,null=True,blank=False)
    country=models.CharField(max_length=100,null=True,blank=False)
    subcountry=models.CharField(max_length=100,null=True,blank=False)
    geonameid=models.IntegerField(default=1,null=True,blank=False)