from datetime import datetime
from email import message
from multiprocessing import context
from tkinter import FLAT
from django.shortcuts import render
from .models import *
from django.views.generic import View
from .forms import *
from django.http import HttpResponseRedirect
from django.urls import is_valid_path, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from datetime import datetime,timedelta, date, time
from django.utils import timezone
from django.contrib import messages
from pytz import timezone
from django import template
from django.utils.dateparse import parse_time
from accounts.models import UserModel
from django.conf import settings  
from dashboard.models import TurfGallery

from accounts.models import UserModel
import operator
from django.db.models import Q
from functools import reduce
from django.http import HttpResponse
from django.db.models import Count
import json
from django.views.decorators.http import require_http_methods
# from datetime import datetime
# import datetime as datetime
# from .models import slotModel

# Create your views here.

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html',{})




#d######################################################### View for listing all matches in user locality which user hasn't requested or joined or created ################################################################################ 
@method_decorator(login_required,name='dispatch')
class AllMatchesView(View):
        def get(self, request, *args, **kwargs):
            if not request.user.is_superuser and not request.user.is_superuser:
                print(request.user.username)
                id_list=RequestModel.objects.filter(username=request.user.pk).values_list('match_id',flat=True)
                matches=MatchModel.objects.filter(city=request.user.current_location,status="Upcoming").exclude(id__in=list(id_list)).order_by("-id")
                form=RequestForm(request=request)
                print("hllo",matches)
                context ={'RequestForm': form ,'is_requestform':False , 'matches':matches}
                print(context)
                return render(request, 'Matches/all-matches.html',context)
            else:
                return render(request, 'errors/error403.html',{})
        def post(self, request, *args, **kwargs):
            location=request.POST.get('location')
            if location :
                list=location.split(", ")
                if len(list) ==3:
                    check_location=CitiesModel.objects.filter(name=list[0],subcountry=list[1],country=list[2])
                    if len(check_location) == 0:
                            messages.error(request,'Please Select a City from the provided list')
                            return HttpResponseRedirect(reverse('matches'))
                else:
                    messages.error(request,'Please Select a City from the provided list')
                    return HttpResponseRedirect(reverse('matches'))  
            if location!=request.user.current_location:
                user=UserModel.objects.get(username=request.user.username)
                user.current_location=location
                user.save()
            return HttpResponseRedirect(reverse('matches'))


##d###########################################################    View for matches user has created or joined  ###########################################################
@method_decorator(login_required,name='dispatch')
class MyMatchesView(View):
    def get(self, request, *args, **kwargs):
        print(request.user.username)
        print(datetime.now())
        context={}
        id_list=RequestModel.objects.filter(username=request.user.pk,status="Accepted").values_list('match_id',flat=True)
        print(list(id_list))
        exclude_status=["Completed","Cancelled"]
        matches=MatchModel.objects.filter(id__in=list(id_list)).exclude(status__in=exclude_status).order_by("-id")
        context['matches']=matches
        context[request]=request
        return render(request, 'Matches/my-matches.html',context)


##d###########################################################   View for creating matches ###############################################################################
@method_decorator(login_required,name='dispatch')
class CreateMatchesView(View):
    template = 'Matches/create-matches.html'
    def get(self, request, *args, **kwargs):
        print(datetime.now()+timedelta(hours=1))
        end_time=(datetime.now()+timedelta(hours=1))
        print(end_time)
        # now = timezone.now()
        # print(now)
        # print(CategoriesModel.objects.get(id=1))
        data={
            'category':CategoriesModel.objects.first(),
            'date':datetime.now().date(),
            'start_time_f':datetime.now().strftime("%H:%M:%S"),
            'end_time_f':end_time.strftime("%H:%M:%S"),
            'start_time':datetime.now(),
            'end_time':end_time,
            'locality':"",
            'city':request.user.location,
            'creator' : request.user.username,
            'status' : "Upcoming",
            'slot_available': 0,
            'slots': 2,
        }
        form = creatematchForm(initial=data,request=request)
        # user = request.user
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",form.options)
        context = {'form': form,
                    'data': 'Add match',
                    # 'user': user,
                    }
        
        return render(request,self.template,context)

    def post(self, request, *args, **kwargs):
        form=creatematchForm(request.POST,request=request)
        # print(form)
        slots=int(request.POST['slots'])
        # print(form.slot_available)
        # print(form)
        # print(request.POST['date']>datetime.now().date(),"djkASGHDGVDGUIJFSABV")
        if form.is_valid():
            print("kikikiki")
            print(form.errors.as_data())
        
            start_date =form.cleaned_data["date"]
            start_time= parse_time(request.POST["start_time_f"])
            end_time= parse_time(request.POST["end_time_f"])

            # start_datetime=datetime(start_date.year,start_date.month,start_date.day,start_time.hour,start_time.minute,start_time.second)
            # end_datetime=datetime(start_date.year,start_date.month,start_date.day,end_time.hour,end_time.minute,end_time.second)
            
            # start_datetime=pd.Timestamp.combine(date(start_date.year, start_date.month, start_date.day), time(start_time.hour,start_time.minute,start_time.second))
            # end_datetime=pd.Timestamp.combine(date(start_date.year, start_date.month, start_date.day), time(end_time.hour,end_time.minute,end_time.second))
         
            print(type(start_time))
            start_datetime= datetime.combine(start_date, start_time).astimezone(timezone('UTC'))
            end_datetime= datetime.combine(start_date, end_time).astimezone(timezone('UTC'))


            # now = timezone.now()
            # print(now,"adddddddttttttttttttttttttddddddddddddddddddddddddddddddddddddddddddddddd")


            form_cf=form.save(commit=False)
            form_cf.start_time=start_datetime
            form_cf.end_time=end_datetime
            print(start_datetime,end_datetime,"ssssssssssssssssssssssssssssssssssss")
            form_cf.save()

            user=UserModel.objects.get(username=request.user.username)
            RequestModel.objects.create(match_id=form_cf,category=form.cleaned_data['category'],username=user,phoneno=request.user.phone,status="Accepted",date=form.cleaned_data['date'],start_time=form.cleaned_data['start_time'],end_time=form.cleaned_data['end_time'],locality=form.cleaned_data['locality'])
            messages.success(request	,'Your match has been succesfully created. Visit My Match to see .')
            return HttpResponseRedirect(reverse('create-matches'))

        else:
            print("########### HAS CITY ERROR #############", form.has_error('end_time_f', code=None))
            if  not form.has_error('start_time_f', code=None) or not form.has_error('end_time_f', code=None) or not  form.has_error('city', code=None):
                     messages.error(request	,'Please do not change the fields')
            return render(request,self.template,{'form':form})
        

############################################################ View for listing requested matches ###########################################################################
@method_decorator(login_required,name='dispatch')
class RequestedMatchesView(View):
    def get(self, request, *args, **kwargs):
        print(request.user.username)
        context={}
        id_list=RequestModel.objects.filter(username=request.user.pk,status="Pending").values_list('match_id',flat=True).order_by("-id")
        print(list(id_list))
        matches=MatchModel.objects.filter(id__in=list(id_list)).order_by("-id")
        context['matches']=matches
        return render(request, 'Matches/requested-matches.html',context)


################################################################  View for cancel match  requests ###################################################################################
@method_decorator(login_required,name='dispatch')
class CancelRequestView(View):
    def get(self, request,id, *args, **kwargs):
        try:
            reqdata=RequestModel.objects.get(match_id=id,username=request.user.username,status="Pending")
        except:
            return render(request, 'errors/error404.html')
        print("hiiiiiiiiiiiiiiiiiiiiiii",reqdata)
        reqdata.status="Cancelled"
        reqdata.save()
        return HttpResponseRedirect(reverse('matches'))

############################################################ View for match history #########################################################################################
@method_decorator(login_required,name='dispatch')
class MatchHistoryView(View):
    def get(self, request, *args, **kwargs):
        id_list1=RequestModel.objects.filter(username=request.user.pk,status="Accepted").values_list('match_id',flat=True).order_by("-id")
        jum=MatchModel.objects.filter(status="Upcoming",id__in=list(id_list1)).exclude(creator=request.user.username).order_by("-id")#joined upcoming matches
        id_list2=RequestModel.objects.filter(username=request.user.pk,status="Accepted").values_list('match_id',flat=True).order_by("-id")
        jcom=MatchModel.objects.filter(status="Completed",id__in=list(id_list2)).exclude(creator=request.user.username).order_by("-id")#joined completed matches
        id_list3=RequestModel.objects.filter(username=request.user.pk,status="Accepted").values_list('match_id',flat=True).order_by("-id")
        jcam=MatchModel.objects.filter(status="Cancelled",id__in=list(id_list3)).exclude(creator=request.user.username).order_by("-id")#joined cancelled matches
        crum=MatchModel.objects.filter(creator=request.user.username,status="Upcoming").order_by("-id") #created upcoming matches
        crcom=MatchModel.objects.filter(creator=request.user.username,status="Completed").order_by("-id") #created completed matches
        crcam=MatchModel.objects.filter(creator=request.user.username,status="Cancelled").order_by("-id") #created cancelled matches
        reqcan=RequestModel.objects.filter(username=request.user.pk,status="Cancelled").order_by("-id")#requests cancelled
        reqrej=RequestModel.objects.filter(username=request.user.pk,status="Rejected").order_by("-id")#requests rejected
        id_list4=MatchModel.objects.filter(creator=request.user.username).values_list('id',flat=True).order_by("-id")
        reqaccep=RequestModel.objects.filter(match_id__in=list(id_list4),status="Accepted").exclude(username=request.user.username).order_by("-id")
        reqrejec=RequestModel.objects.filter(match_id__in=list(id_list4),status="Rejected").exclude(username=request.user.username).order_by("-id")
        context={}
        context={
            'jum':jum,
            'jcom':jcom,
            'jcam':jcam,
            'crum':crum,
            'crcom':crcom,
            'crcam':crcam,
            'reqcan':reqcan,
            'reqrej':reqrej,
            'reqaccep':reqaccep,
            'reqrejec':reqrejec,

        }
        # context['data']=jum
        print(jum)
        print(context)
        return render(request, 'Matches/match-history.html',context)

############################################################# View for listing all turfs in user locality ####################################################################
# class TurfsView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'turf/main.html',{ })

############################################################## View for editing matches created by user #####################################################################


@method_decorator(login_required,name='dispatch')
class EditMatchesView(View):
    def get(self, request,id, *args, **kwargs):
        editobj=MatchModel.objects.get(id=id)

        print ( "type matvhodel : ", type( editobj.start_time ) )

        data={
            'category':editobj.category.id,
            'date':editobj.date,
            'start_time_f':editobj.start_time.astimezone(timezone('Asia/Kolkata')).strftime("%H:%M:%S"),
            'end_time_f':editobj.end_time.astimezone(timezone('Asia/Kolkata')).strftime("%H:%M:%S"),
            'start_time':editobj.start_time,
            'end_time':editobj.end_time,
            'city':editobj.city,
            'locality':editobj.locality,
            'status':editobj.status,
            "creator" : request.user.username,
            "slots": editobj.slots,
            'slot_available':editobj.slot_available,
            'match_id':editobj.id,
        }
        form=updatematchform(data,request=request)
        context={
            'form':form
        }
        return render(request,'Matches/edit-matches.html',context)
        
    def post(self, request, *args, **kwargs):
        match_id = request.POST['match_id']
        form=updatematchform(request.POST,request=request)
        # print(form)
        # print(form.slot_available)
        # print(form)
        if form.is_valid():
            print("kikfjsdhgusdjgusikiki")
            # form.save()
            start_date =form.cleaned_data["date"]
            start_time= parse_time(request.POST["start_time_f"])
            end_time= parse_time(request.POST["end_time_f"])
            print(type(start_time))
            start_datetime= datetime.combine(start_date, start_time).astimezone(timezone('UTC'))
            end_datetime= datetime.combine(start_date, end_time).astimezone(timezone('UTC'))
            updatedRecord = MatchModel.objects.get(id=match_id)
            updatedRecord. category = form.cleaned_data['category']
            updatedRecord. date = form.cleaned_data['date']
            updatedRecord. start_time = start_datetime
            updatedRecord. end_time = end_datetime
            updatedRecord. locality = form.cleaned_data['locality']
            updatedRecord. slots = form.cleaned_data['slots']
            updatedRecord. slot_available = form.cleaned_data['slot_available']
            # if updatedRecord. start_time > datetime.now.astimezone(timezone('UTC')):
            #     updatedRecord.status="Upcomming"
            updatedRecord.save()
            messages.success(request	,'Your match has been succesfully edit. Visit My Match to see .')
            RequestModel.objects.filter(match_id=updatedRecord).update(category=form.cleaned_data['category'],username=form.cleaned_data['creator'],phoneno=request.user.phone,status="Accepted",date=form.cleaned_data['date'],start_time=form.cleaned_data['start_time_f'],end_time=form.cleaned_data['end_time_f'],locality=form.cleaned_data['locality'])
            return HttpResponseRedirect(reverse('my-matches'))
        else:
            print(form.errors.as_data())
            messages.error(request	,'Please do not change the fields')
            return render(request,'Matches/edit-matches.html',{'form':updatematchform(request.POST,request=request)})
        # return HttpResponseRedirect(reverse('my-matches'))



##################################################################### View for Requests viewing #######################################################################
@method_decorator(login_required,name='dispatch')
class RequestsView(View):
    def get(self, request,*args, **kwargs):
        id_list=MatchModel.objects.filter(creator=request.user.username,status="Upcoming").values_list('id',flat=True).order_by("-id")
        print(list(id_list))
        requests=RequestModel.objects.filter(status='Pending',match_id__in=list(id_list)).order_by("-id")
        # print(requests)
        context={}
        context['requests']=requests
        return render(request,'Matches/requests.html',context)
    def  post(self, request, *args, **kwargs):
        selected=request.POST.getlist('selected[]')
        print(selected)
        if selected != []: 
            print("hiiiiiiiiiiiiiiiiiiiiiiiiiiiyyyyyyyyyyyyyyyyyyyyyyyhiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
            if 'Accept' in request.POST:
                print("Accepted requests")
                requests=RequestModel.objects.filter(id__in=selected)
                for requesti in requests:
                    requesti.status="Accepted"
                    match_id=requesti.match_id.pk
                    print(match_id,type(match_id))
                    obj=MatchModel.objects.get(id=match_id)
                    obj.slot_available=obj.slot_available-1
                    if obj.slot_available<0:
                             messages.error(request	,'Slots are full. User cant be selected')
                             return HttpResponseRedirect(reverse('requests'))
                    requesti.save()
                    obj.save()
                messages.success(request,'The requests were accepted')
                return HttpResponseRedirect(reverse('requests'))
            elif 'Reject' in request.POST:
                print("Rejected requests")
                requests=RequestModel.objects.filter(id__in=selected)
                for requestj in requests:
                    requestj.status="Rejected"
                    requestj.save()
                messages.success(request,'The requests were rejected')
                return HttpResponseRedirect(reverse('requests'))
        else:
            print("hyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyiiiiiiiiiiiiiiiiiiiiiiiiiiiiihyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
            messages.error(request	,'NO user request selected')
            return HttpResponseRedirect(reverse('requests'))
######################################################################### View for joining matches #######################################################
@method_decorator(login_required,name='dispatch')
class  JoinMatchView(View):
    def get(self, request,id, *args, **kwargs):
                # user_location=request.user.location
                # location_list=user_location.split(",")
                matches=MatchModel.objects.filter(id=id)

                
                if len(matches) == 1:
                    match = matches[0]
                if len(matches) == 0:
                    return render(request,'errors/error404.html',{})
                print("##################### INSIDE JOIN MATCHES #########################",match)
                joined=RequestModel.objects.filter(status='Accepted',match_id=match.pk).values().order_by("id")
                request.session['id']=match.id 
                print("#### Match.Category #####",match.category,type(match.category)) 
                user=UserModel.objects.get(id=request.user.pk)
                data={
                    'category':match.category.category,
                    'date':match.date,
                    'start_time':match.start_time.astimezone(timezone('Asia/Kolkata')).strftime("%H:%M:%S"),
                    'end_time':match.end_time.astimezone(timezone('Asia/Kolkata')).strftime("%H:%M:%S"),
                    'locality':match.locality,
                    'username':user,
                    'status':"Pending",
                    'phoneno': request.user.phone,
                    'match_id':match.pk,
                }
                print("##################data before initializing request form###########################",data)
                # form=RequestForm(data,request=request)
                # print(form)
                context ={'is_requestform':True ,'match':match,'joined':joined,'data':data}
                print(context)
                return render(request, 'Matches/all-matches.html',context)
        # except:
        #     pass
    def post(self, request, *args, **kwargs):
            match_id=request.session.get('id')
            print(match_id)
            matches=MatchModel.objects.filter(id=match_id)
            if len(matches) == 1:
                requested_match = matches[0]
            user=UserModel.objects.get(id=request.user.pk)
            data={
                    'category':requested_match.category.id,
                    'date':requested_match.date,
                    'start_time':requested_match.start_time.astimezone(timezone('Asia/Kolkata')).strftime("%H:%M:%S"),
                    'end_time':requested_match.end_time.astimezone(timezone('Asia/Kolkata')).strftime("%H:%M:%S"),
                    'locality':requested_match.locality,
                    'username':user.id,
                    'status':"Pending",
                    'phoneno': request.user.phone,
                    'match_id':requested_match.pk,
                }
            form=RequestForm(data,request=request)
            print(form)
            if form.is_valid():
                print("kikikiki")
                obj=form.save(commit=False)
                obj.match_id=requested_match
                obj.save()
                return  HttpResponseRedirect(reverse('matches'))
            else:
                messages.error(request	,'Please do not change the fields')
                joined=RequestModel.objects.filter(status='Accepted',match_id=requested_match.pk).values()
                context ={'is_requestform':True ,'match':requested_match,'joined':joined,'data':data}
                print(context)
                return render(request, 'Matches/all-matches.html',context)


################################################################## View for cancelling matches #####################################################################

@method_decorator(login_required,name='dispatch')
class CancelMatchView(View):
    def get(self, request,id, *args, **kwargs):
        try:
            reqdata=MatchModel.objects.get(id=id,creator=request.user.username,status="Upcoming")
        except:
             messages.error(request,'You cannot cancel this match')
             return HttpResponseRedirect(reverse('my-matches'))
        print("hiiiiiiiiiiiiiiiiiiiiiii",reqdata)
        reqdata.status="Cancelled"
        reqdata.cron=0
        reqdata.save()
        return HttpResponseRedirect(reverse('match-history'))



#-----------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------

#**********************************create tournament***********************************

@method_decorator(login_required,name='dispatch')
class CreateTournamentView(View):
    template = 'Tournaments/create-tournament.html'
    def get(self, request, *args, **kwargs):
        print(datetime.now()+timedelta(hours=1))
        end_time=(datetime.now()+timedelta(hours=1))
        print(end_time)
     
        data={
            'category':CategoriesModel.objects.first(),
            'team_name':CreateTeamModel.objects.first(),
            'start_date':datetime.now().date(),
            'end_date':datetime.now().date(),
            'start_time_f':datetime.now().strftime("%H:%M:%S"),
            'end_time_f':end_time.strftime("%H:%M:%S"),
            'start_time':datetime.now(),
            'end_time':end_time,
            'locality':request.user.location,
            'creator' : request.user.username,
            'status' : "Upcoming",
            'team_space_available': 0,
            'teams': 2,
        }
        form = createtournamentForm(initial=data,request=request)
        # user = request.user
        # print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",form.options)
        context = {'form': form,
                    'data': 'Add tournament',
                    # 'user': 'user',
                    }
        
        return render(request,'Tournaments/create-tournament.html',context)


    def post(self, request, *args, **kwargs):
        form=createtournamentForm(request.POST,request=request)
      
        teams=int(request.POST['teams'])
        # print(request.POST['start_date']>datetime.now().date(),"djkASGHDGVDGUIJFSABV")
        if form.is_valid():
            print("kikikiki")
            print(form.errors.as_data())
        
            start_date =form.cleaned_data["start_date"]
            end_date =form.cleaned_data["end_date"]
            start_time= parse_time(request.POST["start_time_f"])
            end_time= parse_time(request.POST["end_time_f"])

            
         
            print(type(start_time))
            start_datetime= datetime.combine(start_date, start_time).astimezone(timezone('UTC'))
            end_datetime= datetime.combine(start_date, end_time).astimezone(timezone('UTC'))



            form_cf=form.save(commit=False)
            form_cf.start_time=start_datetime
            form_cf.end_time=end_datetime
            print(start_datetime,end_datetime,"ssssssssssssssssssssssssssssssssssss")
            form_cf.save()


            TournamentRequestModel.objects.create(tournament_id=form_cf,category=form.cleaned_data['category'],team_name=form.cleaned_data['team_name'],username=form.cleaned_data['creator'],phoneno=request.user.phone,status="Accepted",start_date=form.cleaned_data['start_date'],end_date=form.cleaned_data['end_date'],start_time=form.cleaned_data['start_time'],end_time=form.cleaned_data['end_time'],locality=form.cleaned_data['locality'])
            messages.success(request	,'Your tournament has been succesfully created. Visit My tournament to see .')
            return HttpResponseRedirect(reverse('my-tournaments'))
            

        else:
            # print(form.errors['start_time'])
            if  not form.has_error('start_time_f', code=None) or not form.has_error('end_time_f', code=None):
                     messages.error(request	,'Please do not change the fields')
            return render(request,self.template,{'form':form})


#############################################################    View for tournaments user has created or joined  ###########################################################
@method_decorator(login_required,name='dispatch')
class MyTournamentView(View):
    def get(self, request, *args, **kwargs):
        print(request.user.username)
        print(datetime.now())
        # tournament=TournamentModel.objects.filter(id__in=list(id))
        tournament=TournamentModel.objects.all()
        # img1 = CategoriesModel.objects.values_list('image')[0][0]
        # img2 = CategoriesModel.objects.values_list('image')[1][0]
        # img3 = CategoriesModel.objects.values_list('image')[2][0]
        # img4 = CategoriesModel.objects.values_list('image')[3][0]
        # img5 = CategoriesModel.objects.values_list('image')[4][0]

        
        
        context={
            'tournaments':tournament,
            # 'img1' : img1,
            # "img2" : img2,
            # "img3" : img3,
            # "img4" : img4,
            # "img5" : img5,

            # 'media_url':settings.MEDIA_URL,
            
        }
        return render(request, 'Tournaments/my-tournament.html',context)

############################### view for editing created tournaments  ####################################################################
@method_decorator(login_required,name='dispatch')
class EditTournamentView(View):
    def get(self, request,id, *args, **kwargs):
        editobj1=TournamentModel.objects.get(id=id)
        # print(id,"44444444444444444444444444444444444444444444444444444444444")
        data={
            'category':editobj1.category.id,
            'team_name':editobj1.team_name,
            'start_date':editobj1.start_date,
            'end_date':editobj1.end_date,
            'start_time_f':editobj1.start_time.astimezone(timezone('Asia/Kolkata')).strftime("%H:%M:%S"),
            'end_time_f':editobj1.end_time.astimezone(timezone('Asia/Kolkata')).strftime("%H:%M:%S"),
            'start_time':editobj1.start_time,
            'end_time':editobj1.end_time,
            'locality':editobj1.locality,
            'status':editobj1.status,
            "creator" : request.user.username,
            "teams": editobj1.teams,
            'team_space_available':editobj1.team_space_available,
            'tournament_id':editobj1.id,
        }
        form=updatetournamentform(data,request=request)
        context={
            'form':form
            
        }
        return render(request,'Tournaments/edit-tournaments.html',context)
        
    def post(self, request, *args, **kwargs):
        tournament_id = request.POST['tournament_id']
        form=updatetournamentform(request.POST,request=request)
  
        if form.is_valid():
            print("kikfjsdhgusdjgusikiki")
            start_date =form.cleaned_data["start_date"]
            end_date =form.cleaned_data["end_date"]
            start_time= parse_time(request.POST["start_time_f"])
            end_time= parse_time(request.POST["end_time_f"])
            print(type(start_time))
            start_datetime= datetime.combine(start_date, start_time).astimezone(timezone('UTC'))
            end_datetime= datetime.combine(end_date, end_time).astimezone(timezone('UTC'))
            updatedRecord = TournamentModel.objects.get(id=tournament_id)
            updatedRecord. category = form.cleaned_data['category']
            updatedRecord. team_name = form.cleaned_data['team_name']
            updatedRecord. start_date = form.cleaned_data['start_date']
            updatedRecord. end_date = form.cleaned_data['end_date']
            updatedRecord. start_time = start_datetime
            updatedRecord. end_time = end_datetime
            updatedRecord. locality = form.cleaned_data['locality']
            updatedRecord. teams = form.cleaned_data['teams']
            updatedRecord. team_space_available = form.cleaned_data['team_space_available']
            updatedRecord.save()
            messages.success(request	,'Your tournament has been successfully edited.')
            TournamentRequestModel.objects.filter(tournament_id=updatedRecord).update(category=form.cleaned_data['category'],team_name=form.cleaned_data['team_name'],username=form.cleaned_data['creator'],phoneno=request.user.phone,status="Accepted",start_date=form.cleaned_data['start_date'],end_date=form.cleaned_data['end_date'],start_time=form.cleaned_data['start_time_f'],end_time=form.cleaned_data['end_time_f'],locality=form.cleaned_data['locality'])
            return HttpResponseRedirect(reverse('my-tournaments'))
        else:
            print("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
            print(form.errors.as_data())
            messages.error(request	,'Please do not change the fields')
            return render(request,'Tournaments/edit-tournaments.html',{'form':updatetournamentform(request.POST,request=request)})
            


########################################################## View for listing all tournament in user locality which user hasn't requested or joined or created ################################################################################ 
@method_decorator(login_required,name='dispatch')
class AllTournamentView(View):
        def get(self, request, *args, **kwargs):
                print(request.user.username)
                # context={}
                id_list=TournamentRequestModel.objects.filter(username=request.user.username).values_list('tournament_id',flat=True)
                tournament=TournamentModel.objects.filter(locality__iexact=request.user.location,status="Upcoming").exclude(id__in=list(id_list))
                form=TournamentRequestForm(request=request)
                context ={'TournamentRequestForm': form ,'is_tournamentrequestform':False , 'tournaments':tournament}
                print(context)
                return render(request, 'Tournaments/tournaments.html',context)


# @method_decorator(login_required,name='dispatch')
# class CreateTeamView(View):

############################################################ View for listing requested tournaments ###########################################################################
@method_decorator(login_required,name='dispatch')
class RequestedTournamentView(View):
    def get(self, request, *args, **kwargs):
        print(request.user.username)
        context={}
        id_list=TournamentRequestModel.objects.filter(username=request.user.username,status="Pending").values_list('tournament_id',flat=True).order_by("-id")
        print(list(id_list))
        tournament=TournamentModel.objects.filter(id__in=list(id_list)).order_by("-id")
        context['tournaments']=tournament
        return render(request, 'Tournaments/requested-tournaments.html',context)


###########################################################view for joining tournaments########################################################################

@method_decorator(login_required,name='dispatch')
class  JoinTournamentView(View):
    def get(self, request,id, *args, **kwargs):
                user_location=request.user.location
                tournaments=TournamentModel.objects.filter(id=id)
                team_now=TournamentModel.objects.filter(id=id)

                teams = CreateTeamModel.objects.all()
                
                print("==================================",tournaments)

                if len(tournaments) == 1:
                        tournament = tournaments[0]
                        team=teams[0]
           

                if len(tournaments) == 0:
                    return render(request,'errors/error404.html',{})
                print("##################### INSIDE JOIN MATCHES #########################",tournament)

                a=TournamentRequestModel.objects.filter(status='Accepted',tournament_id=tournament.pk).values().order_by("id")
                b=TournamentRequestModel.objects.values_list()
                request.session['id']=tournament.id 
                print("#### Match.Category #####",tournament.category,type(tournament.category))
                print("#### Match.Category #####",tournament.team_name,type(tournament.team_name))
                # print("--",b.team_name)
                

                data={
                    'category':tournament.category,
                    # 'team_name_now':b.team_name,
                    'joined_teams':TournamentRequestModel.objects.order_by('tournament_id'),
                    # 'joined_teams':TournamentRequestModel.objects.annotate(count=Count('tournament_id')).order_by('id').distinct('tournament_id').filter(count__gt=1),
                    'team_name':CreateTeamModel.objects.filter(),
                    'start_date':tournament.start_date,
                    'end_date':tournament.end_date,
                    'start_time':tournament.start_time.astimezone(timezone('Asia/Kolkata')).strftime("%H:%M:%S"),
                    'end_time':tournament.end_time.astimezone(timezone('Asia/Kolkata')).strftime("%H:%M:%S"),
                    'locality':tournament.locality,
                    'username':request.user.username,
                    'status':"Pending",
                    'phoneno': request.user.phone,
                    'tournament_id':tournament.pk,
                }
                print("##################data before initializing request form###########################",data)
                # print("================++++++++++++=================",team)

                context ={'is_tournamentrequestform':True ,'tournament':tournament,'a':a,'data':data,}
                print(context)
                return render(request, 'Tournaments/tournaments.html',context)

    def post(self, request, *args, **kwargs):
            tournament_id=request.session.get('id')
            print(tournament_id)
            tournaments=TournamentModel.objects.filter(id=tournament_id)
            # form=updatetournamentform(request.POST,request=request)

            # teams = CreateTeamModel.objects.all()
            # print("==================+++++++++++++++++++++======================",teams)
            print("===request.POST",(request.POST['team-select']))
            if len(tournaments) == 1:
                requested_tournament = tournaments[0]
                # team=teams[0]
          
            data1={
                    'category':requested_tournament.category.id,
                    'team_name':request.POST['team-select'],
                    # "team_name":requested_tournament.team_name,
                    'start_date':requested_tournament.start_date,
                    'end_date':requested_tournament.end_date,
                    'start_time':requested_tournament.start_time.astimezone(timezone('Asia/Kolkata')).strftime("%H:%M:%S"),
                    'end_time':requested_tournament.end_time.astimezone(timezone('Asia/Kolkata')).strftime("%H:%M:%S"),
                    'locality':requested_tournament.locality,
                    'username':request.user.username,
                    'status':"Pending",
                    'phoneno': request.user.phone,
                    'tournament_id':requested_tournament.pk,
                }
            form=TournamentRequestForm(data1,request=request)
            print("================++++++++++++=================",data1)
            print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\",form.errors)
            # print("",team_name)

            if form.is_valid():
                print("kikikiki")
                obj=form.save(commit=False)
                obj.tournament_id=requested_tournament
                obj.save()
                print("========================================================================")
                messages.success(request,"Tournamnt Requested Successfully")
                return  HttpResponseRedirect(reverse('all-tournaments'))
            else:
                messages.error(request	,'Please do not change the fields')
                a=TournamentRequestModel.objects.filter(status='Accepted',tournament_id=requested_tournament.pk).values()
                context ={'is_tournamentrequestform':True ,'tournament':requested_tournament,'a':a,'data1':data1,}
                print(context)
                # return render(request, 'Tournaments/tournaments.html',context)
                return render(request, 'Tournaments/tournaments.html',context)
                

##################################################################### View for Requests viewing #######################################################################
@method_decorator(login_required,name='dispatch')
class TournamentRequestsView(View):
    def get(self, request,*args, **kwargs):
        id_list=TournamentModel.objects.filter(creator=request.user.username,status="Upcoming").values_list('id',flat=True).order_by("-id")
        print(list(id_list))
        tournament_requests=TournamentRequestModel.objects.filter(status='Pending',tournament_id__in=list(id_list)).values().order_by("-id")
        # print(requests)
        context={}
        context['requests']=tournament_requests
        return render(request,'Tournaments/requests.html',context)
    def  post(self, request, *args, **kwargs):
        selected=request.POST.getlist('selected[]')
        print(selected)
        if selected != []: 
            print("hiiiiiiiiiiiiiiiiiiiiiiiiiiiyyyyyyyyyyyyyyyyyyyyyyyhiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
            if 'Accept' in request.POST:
                print("Accepted requests")
                requests=TournamentRequestModel.objects.filter(id__in=selected)
                for requesti in requests:
                    requesti.status="Accepted"
                    requesti.save()

                    tournament_id=requesti.tournament_id.pk
                    print(tournament_id,type(tournament_id))
                    obj=TournamentModel.objects.get(id=tournament_id)
                    obj.team_space_available=obj.team_space_available-1
                    if obj.team_space_available<=0:
                             messages.error(request	,'Slots are full. User cant be selected')
                             return HttpResponseRedirect(reverse('tournament-requests'))
                    obj.save()
                messages.success(request,'The requests were accepted')
                return HttpResponseRedirect(reverse('tournament-requests'))
            elif 'Reject' in request.POST:
                print("Rejected requests")
                requests=TournamentRequestModel.objects.filter(id__in=selected)
                for requestj in requests:
                    requestj.status="Rejected"
                    requestj.save()
                messages.success(request,'The requests were rejected')
                return HttpResponseRedirect(reverse('tournament-requests'))
        else:
            print("hyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyiiiiiiiiiiiiiiiiiiiiiiiiiiiiihyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
            messages.error(request	,'NO user selected')
            return HttpResponseRedirect(reverse('tournament-requests'))



################################################################  View for cancel tournament requested by user ###################################################################################
@method_decorator(login_required,name='dispatch')
class CancelTournamentsRequestView(View):
    def get(self, request,id, *args, **kwargs):
        try:
            reqdatat=TournamentRequestModel.objects.get(tournament_id=id,username=request.user.username,status="Pending")
            messages.success(request,'You successfully canceled this Tournament')

        except:
            return render(request, 'errors/error404.html')
        print("hiiiiiiiiiiiiiiiiiiiiiii",reqdatat)
        reqdatat.status="Cancelled"
        reqdatat.save()
        return HttpResponseRedirect(reverse('all-tournaments'))

################################################################## View for cancelling Tournaments #####################################################################

@method_decorator(login_required,name='dispatch')
class CancelTournamentView(View):
    def get(self, request,id, *args, **kwargs):
        try:
            reqdata1=TournamentModel.objects.get(id=id,creator=request.user.username,status="Upcoming")
            messages.success(self.request, "Tournament Cancelled Successfully")

        except:
            
             messages.error(request,'You cannot cancel this Tournament')
             return HttpResponseRedirect(reverse('all-tournaments'))
        print("hiiiiiiiiiiiiiiiiiiiiiii",reqdata1)
        reqdata1.status="Cancelled"
        reqdata1.save()
        return HttpResponseRedirect(reverse('tournament-history'))


############################################################ View for tournament history #########################################################################################
@method_decorator(login_required,name='dispatch')
class TournamentHistoryView(View):
    def get(self, request, *args, **kwargs):
        id_list1=TournamentRequestModel.objects.filter(username=request.user.username,status="Accepted").values_list('tournament_id',flat=True).order_by("-id")
        jum=TournamentModel.objects.filter(status="Upcoming",id__in=list(id_list1)).exclude(creator=request.user.username).values().order_by("-id")#joined upcoming matches
        id_list2=TournamentRequestModel.objects.filter(username=request.user.username,status="Accepted").values_list('tournament_id',flat=True).order_by("-id")
        jcom=TournamentModel.objects.filter(status="Completed",id__in=list(id_list2)).exclude(creator=request.user.username).values().order_by("-id")#joined completed matches
        id_list3=TournamentRequestModel.objects.filter(username=request.user.username,status="Accepted").values_list('tournament_id',flat=True).order_by("-id")
        jcam=TournamentModel.objects.filter(status="Cancelled",id__in=list(id_list3)).exclude(creator=request.user.username).values().order_by("-id")#joined cancelled matches
        crum=TournamentModel.objects.filter(creator=request.user.username,locality__iexact=request.user.location,status="Upcoming").order_by("-id") #created upcoming matches
        crcom=TournamentModel.objects.filter(creator=request.user.username,locality__iexact=request.user.location,status="Completed").order_by("-id") #created completed matches
        crcam=TournamentModel.objects.filter(creator=request.user.username,locality__iexact=request.user.location,status="Cancelled").order_by("-id") #created cancelled matches
        reqcan=TournamentRequestModel.objects.filter(username=request.user.username,status="Cancelled").order_by("-id")#requests cancelled
        reqrej=TournamentRequestModel.objects.filter(username=request.user.username,status="Rejected").order_by("-id")#requests rejected
        id_list4=TournamentModel.objects.filter(creator=request.user.username,locality__iexact=request.user.location).values_list('id',flat=True).order_by("-id")
        reqaccep=TournamentRequestModel.objects.filter(tournament_id__in=list(id_list4),status="Accepted").exclude(username=request.user.username).order_by("-id")
        reqrejec=TournamentRequestModel.objects.filter(tournament_id__in=list(id_list4),status="Rejected").exclude(username=request.user.username).order_by("-id")
        context={}
        context={
            'jum':jum,
            'jcom':jcom,
            'jcam':jcam,
            'crum':crum,
            'crcom':crcom,
            'crcam':crcam,
            'reqcan':reqcan,
            'reqrej':reqrej,
            'reqaccep':reqaccep,
            'reqrejec':reqrejec,

        }
        # context['data']=jum
        print(jum)
        print(context)
        return render(request, 'Tournaments/tournament-history.html',context)

@method_decorator(login_required,name='dispatch')
class Createteamview(View):
    # template = 'Tournaments/create-team.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = TeamCreationForm
            context={
                'form': form,
                # 'data' : 'Add team'

            }
            # context['form'] = TeamCreationForm()
            return render(request,'Tournaments/create-team.html',context)
        else:
            return HttpResponseRedirect(reverse('all-tournaments'))
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = TeamCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(self.request, "team created successfully")
                return HttpResponseRedirect(reverse('create-tournament'))

            else:
                context = {
                    "form": form,
                }
                return render(request,'Tournaments/create-tournament.html',context)




        # team = CreateTeamModel.objects.all()
        # # print(team,"=========================================")


        # data={
        #     'team_name': team.team_name,
        #     'category':CategoriesModel.objects.first(),
        #     'members': team.members
        # }

        # form = TeamCreationForm(data,request=request)

        # context ={
        #     "form":form,
        #     'data' : 'Add team'
        # }


















@method_decorator(login_required,name='dispatch')
class TurfsListView(View):
    def get(self, request, *args, **kwargs):
        turfs = UserModel.objects.filter(is_turf=True)
        categories = CategoriesModel.objects.all()
        categories_dict={}
        for category in categories:
            categories_dict[str(category.id)]=category.category
        context = {'media_url':settings.MEDIA_URL, 'turfs':turfs,
                    'categories_dict': categories_dict}
        return render(request, 'turf/turfs_list.html',context)


@method_decorator(login_required,name='dispatch')
class TurfProfileView(View):
    def get(self, request, *args, **kwargs):
        username = kwargs.pop('username')
        

        turf = UserModel.objects.filter(username=username).first()  
        if turf:
            images = TurfGallery.objects.filter(username = username )
            categories = CategoriesModel.objects.all()
            categories_dict={}
            for category in categories:
                categories_dict[str(category.id)]={'category':category.category,'image':category.image}
            comments = TurfCommentsModel.objects.filter(turf=turf).order_by('-date')
            # commentForm = CreateTurfCommentForm(initial={'turf':turf,'commenter':request.user,'date':datetime.now()})
            liked_comments = []
            for comment in comments:
                if comment.liked_users:
                    for user in comment.liked_users:
                        if user == request.user.username:
                            liked_comments.append(comment)
                            continue

            
            header = TurfGallery.objects.filter( username = username ,isheader = True).first()
            context = {'id': turf.id,
                        'turf':turf,
                        'media_url':settings.MEDIA_URL,
                        'images':images,
                        'categories_dict': categories_dict,
                        'liked_comments':liked_comments,
                        'comments':comments,
                        "header":header}
            return render(request, 'turf/turf_profile.html',context)
        else:
            return render(request, 'errors/error404.html',{})
    # def post (self, request, *args, **kwargs):
    #     username = kwargs.pop('username')

    #     turf = UserModel.objects.filter(username=username).first()  
    #     images = TurfGallery.objects.filter(username = username )
    #     categories = CategoriesModel.objects.all()
    #     categories_dict={}
    #     for category in categories:
    #         categories_dict[str(category.id)]={'category':category.category,'image':category.image}
    #     comments = TurfCommentsModel.objects.filter(turf=turf).order_by('-date')
    #     print(comments)
    #     commentForm = CreateTurfCommentForm(initial={'turf':turf,'commenter':request.user,'date':datetime.now()})
    #     context = {'id': turf.id,
    #                 'turf':turf,
    #                 'media_url':settings.MEDIA_URL,
    #                 'images':images,
    #                 'categories_dict': categories_dict,
    #                 'commentForm':commentForm,
    #                 'comments':comments,}

    #     if request.method == 'POST':
    #         commentForm = CreateTurfCommentForm(request.POST)
    #         if commentForm.is_valid():
    #             commentForm.turf = turf
    #             commentForm.commenter = request.user
    #             commentForm.date=datetime.now()
    #             commentForm.save()
    #             return HttpResponseRedirect(reverse('turf_profile',args=[str(username)]))
    #         else:
    #             context['commentForm']=commentForm
    #             return render(request, 'turf/turf_profile.html',context)
    #     messages.error(request	,'Something went wrong')
    #     return render(request, 'turf/turf_profile.html',context)
@method_decorator(login_required,name='dispatch')
class AddTurfCommentView(View):
    def post(self, request, *args, **kwargs):
        print("working rrrrrrrrrrrrrrrrrrrrrrrr")
        username = kwargs.pop('username')

        turf = UserModel.objects.filter(username=username).first() 
        try:
            if  request.POST.get("comment") != "":
                comment= TurfCommentsModel.objects.create(  turf = turf,
                                                            commenter = request.user ,
                                                            date=datetime.now(),comment=request.POST.get("comment"),)
        except:
            message.error(request , "something went wrong, Retry")
            
        
        comments = TurfCommentsModel.objects.filter(turf=turf).order_by('-date')
        context = {
                    'media_url':settings.MEDIA_URL,
                    'comments':comments,}
     
        return render(request, 'turf/comment_list.html',context)

@method_decorator(login_required,name='dispatch')
class LikeTurfCommentView(View):
    # @require_http_methods(['LIKETURFCOMMENT'])
    def post(self, request, *args, **kwargs):
        id = kwargs.pop('id')

        comment = TurfCommentsModel.objects.get(id=id)
        liked_users= comment.liked_users
        


        if liked_users:
            if request.user.username in liked_users:
                liked_users.remove(request.user.username)
                comment.likes_count -= 1
                comment.save()
                return HttpResponse(' <div class="d-flex justify-content-start "> <div class="me-1 ms-2 text-body">'+ str(comment.likes_count)+' Likes </div>  <div><svg style="cursor:pointer ;" class="mb-1" width="15" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"> <path fill-rule="evenodd" clip-rule="evenodd" d="M2.87187 11.5983C1.79887 8.24832 3.05287 4.41932 6.56987 3.28632C8.41987 2.68932 10.4619 3.04132 11.9999 4.19832C13.4549 3.07332 15.5719 2.69332 17.4199 3.28632C20.9369 4.41932 22.1989 8.24832 21.1269 11.5983C19.4569 16.9083 11.9999 20.9983 11.9999 20.9983C11.9999 20.9983 4.59787 16.9703 2.87187 11.5983Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"> </path> <path d="M16 6.69995C17.07 7.04595 17.826 8.00095 17.917 9.12195" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>  </svg> </div></div> ')

            else:
                liked_users.append(request.user.username)
                comment.liked_users = liked_users
                comment.likes_count += 1
                comment.save()
                return HttpResponse('<div class="d-flex justify-content-start "> <div class="me-1 ms-2 text-body">'+ str(comment.likes_count)+' Likes </div>  <div> <svg style="cursor:pointer ;" class="mb-1" width="17" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"> <path fill-rule="evenodd" clip-rule="evenodd" d="M15.85 2.50065C16.481 2.50065 17.111 2.58965 17.71 2.79065C21.401 3.99065 22.731 8.04065 21.62 11.5806C20.99 13.3896 19.96 15.0406 18.611 16.3896C16.68 18.2596 14.561 19.9196 12.28 21.3496L12.03 21.5006L11.77 21.3396C9.48102 19.9196 7.35002 18.2596 5.40102 16.3796C4.06102 15.0306 3.03002 13.3896 2.39002 11.5806C1.26002 8.04065 2.59002 3.99065 6.32102 2.76965C6.61102 2.66965 6.91002 2.59965 7.21002 2.56065H7.33002C7.61102 2.51965 7.89002 2.50065 8.17002 2.50065H8.28002C8.91002 2.51965 9.52002 2.62965 10.111 2.83065H10.17C10.21 2.84965 10.24 2.87065 10.26 2.88965C10.481 2.96065 10.69 3.04065 10.89 3.15065L11.27 3.32065C11.3618 3.36962 11.4649 3.44445 11.554 3.50912C11.6104 3.55009 11.6612 3.58699 11.7 3.61065C11.7163 3.62028 11.7329 3.62996 11.7496 3.63972C11.8354 3.68977 11.9247 3.74191 12 3.79965C13.111 2.95065 14.46 2.49065 15.85 2.50065ZM18.51 9.70065C18.92 9.68965 19.27 9.36065 19.3 8.93965V8.82065C19.33 7.41965 18.481 6.15065 17.19 5.66065C16.78 5.51965 16.33 5.74065 16.18 6.16065C16.04 6.58065 16.26 7.04065 16.68 7.18965C17.321 7.42965 17.75 8.06065 17.75 8.75965V8.79065C17.731 9.01965 17.8 9.24065 17.94 9.41065C18.08 9.58065 18.29 9.67965 18.51 9.70065Z" fill="currentColor"></path>  </svg> </div></div>')
            
        else:
            liked_users = []
            liked_users.append(request.user.username)
            comment.liked_users = liked_users
            comment.likes_count += 1
            comment.save()
            return HttpResponse('<div class="d-flex justify-content-start "> <div class="me-1 ms-2 text-body">'+ str(comment.likes_count)+' Likes </div>  <div> <svg style="cursor:pointer ;" class="mb-1" width="17" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"> <path fill-rule="evenodd" clip-rule="evenodd" d="M15.85 2.50065C16.481 2.50065 17.111 2.58965 17.71 2.79065C21.401 3.99065 22.731 8.04065 21.62 11.5806C20.99 13.3896 19.96 15.0406 18.611 16.3896C16.68 18.2596 14.561 19.9196 12.28 21.3496L12.03 21.5006L11.77 21.3396C9.48102 19.9196 7.35002 18.2596 5.40102 16.3796C4.06102 15.0306 3.03002 13.3896 2.39002 11.5806C1.26002 8.04065 2.59002 3.99065 6.32102 2.76965C6.61102 2.66965 6.91002 2.59965 7.21002 2.56065H7.33002C7.61102 2.51965 7.89002 2.50065 8.17002 2.50065H8.28002C8.91002 2.51965 9.52002 2.62965 10.111 2.83065H10.17C10.21 2.84965 10.24 2.87065 10.26 2.88965C10.481 2.96065 10.69 3.04065 10.89 3.15065L11.27 3.32065C11.3618 3.36962 11.4649 3.44445 11.554 3.50912C11.6104 3.55009 11.6612 3.58699 11.7 3.61065C11.7163 3.62028 11.7329 3.62996 11.7496 3.63972C11.8354 3.68977 11.9247 3.74191 12 3.79965C13.111 2.95065 14.46 2.49065 15.85 2.50065ZM18.51 9.70065C18.92 9.68965 19.27 9.36065 19.3 8.93965V8.82065C19.33 7.41965 18.481 6.15065 17.19 5.66065C16.78 5.51965 16.33 5.74065 16.18 6.16065C16.04 6.58065 16.26 7.04065 16.68 7.18965C17.321 7.42965 17.75 8.06065 17.75 8.75965V8.79065C17.731 9.01965 17.8 9.24065 17.94 9.41065C18.08 9.58065 18.29 9.67965 18.51 9.70065Z" fill="currentColor"></path>  </svg> </div></div>')



class SearchCityView(View):
    def get (self, request,*args, **kwargs):
        return HttpResponse("Method Not Allowed")
    def post(self, request, *args, **kwargs):
            feildname = kwargs.pop('feildname')
            search_text = request.POST.get(feildname)
            print("#########################INSIDE SearchCityView" ,search_text ,"##################")
            if search_text:
                if len(search_text)>=3:
                    results=CitiesModel.objects.filter(name__icontains=search_text)
                    print(results,"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                    return render(request, 'Matches/cities-list.html',{"results":results})
                else:
                    return render(request, 'Matches/cities-list.html',{})
            else:
                # return render(request, 'Matches/cities-list.html',{"results":results})
                return render(request, 'Matches/cities-list.html',{})




@method_decorator(login_required,name='dispatch')
class SearchTurfListView(View):
    def post(self, request, *args, **kwargs):
        searchkey = request.POST.get('search_turf_list')
        turfs = UserModel.objects.filter(is_turf=True)

        searched_category = CategoriesModel.objects.filter(category__icontains=searchkey)
        turfs_by_category=CategoriesModel.objects.none()
        for item in searched_category:
            searched_category_id =item.pk
            turfs_by_category |= turfs.filter(category__icontains=searched_category_id)
        
        turfs_by_username = turfs.filter(turf_name__icontains=searchkey)
        turfs_by_location = turfs.filter(location__icontains=searchkey)

        turfs_result = (turfs_by_username | turfs_by_location | turfs_by_category).distinct()
        # print("turfs_by_location......................... ",turfs_by_location)

        # if turfs:
        #     if turfs_by_username:
        #         if turfs_by_location:
        #             turfs_by_username.union(turfs_by_location) 
        #         if turfs_by_category:
        #             turfs_by_username.union(turfs_by_category) 
        categories = CategoriesModel.objects.all()
        categories_dict={}
        for category in categories:
            categories_dict[str(category.id)]=category.category
        context = {'media_url':settings.MEDIA_URL, 'turfs':turfs_result,
                    'categories_dict': categories_dict,
                    'is_searching':True,
                    'search_KW':searchkey,}
        return render(request , 'turf/turfs.html',context)

@method_decorator(login_required,name='dispatch')
class SearchMatchView(View):
    def post(self, request, *args, **kwargs):
        search_word = request.POST.get('search')
        try:
            date_obj=datetime.strptime(search_word, '%Y-%m-%d')
        except:
            date_obj=datetime.strptime("2000-01-01", '%Y-%m-%d')
        print(date_obj,type(date_obj))
        categories=CategoriesModel.objects.filter(category__icontains=search_word)
        print(categories)
        id_list=RequestModel.objects.filter(username=request.user.pk).values_list('match_id',flat=True)
        # print(id_list)
        matches=MatchModel.objects.filter(Q(Q(creator__icontains=search_word)|Q(date=date_obj)|Q(category__in=categories))&Q(status="Upcoming")).exclude(id__in=list(id_list))
        # matches=MatchModel.objects.filter(category__in=categories).exclude(creator=request.user.username,id__in=list(id_list))
        form=RequestForm(request=request)
        context ={'RequestForm': form ,'is_requestform':False , 'matches':matches,'is_searching':True,'search_KW':search_word}
        print("###################### Inside SearchMatchView ###########################",context,"@@@@@@@@@@@@@@@@@@@",id_list,"!!!!!!!!!!!!!!!!!!!!!!!",matches)
        return render(request, 'Matches/matches.html',context)


# @method_decorator(login_required,name='dispatch')
# class UpdateCurrentLocView(View):
#     def post(self, request, *args, **kwargs):
#         pass