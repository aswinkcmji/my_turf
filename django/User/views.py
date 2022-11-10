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
from .forms import *
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
                print(request.user.username)
                # context={}
                id_list=RequestModel.objects.filter(username=request.user.username).values_list('match_id',flat=True)
                user_location=request.user.location
                location_list=user_location.split(",")
                # print()
                try:
                    location_list.remove(' India')
                except:
                    pass
                print(location_list)
                matches=MatchModel.objects.filter(reduce(operator.or_, (Q(locality__icontains=x) for x in location_list)),status="Upcoming").exclude(id__in=list(id_list)).order_by("-id")
                form=RequestForm(request=request)
                print("hllo",matches)
                # context['matches']=matches
                # context['form']=form
                context ={'RequestForm': form ,'is_requestform':False , 'matches':matches}
                print(context)
                return render(request, 'Matches/all-matches.html',context)


##d###########################################################    View for matches user has created or joined  ###########################################################
@method_decorator(login_required,name='dispatch')
class MyMatchesView(View):
    def get(self, request, *args, **kwargs):
        print(request.user.username)
        print(datetime.now())
        context={}
        id_list=RequestModel.objects.filter(username=request.user.username,status="Accepted").values_list('match_id',flat=True)
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
            'locality':request.user.location,
            'creator' : request.user.username,
            'status' : "Upcoming",
            'slot_available': 0,
            'slots': 2,
        }
        form = creatematchForm(data,request=request)
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


            RequestModel.objects.create(match_id=form_cf,category=form.cleaned_data['category'],username=form.cleaned_data['creator'],phoneno=request.user.phone,status="Accepted",date=form.cleaned_data['date'],start_time=form.cleaned_data['start_time'],end_time=form.cleaned_data['end_time'],locality=form.cleaned_data['locality'])
            messages.success(request	,'Your match has been succesfully created. Visit My Match to see .')
            return HttpResponseRedirect(reverse('create-matches'))

        else:
            # print(form.errors['start_time'])
            if  not form.has_error('start_time_f', code=None) or not form.has_error('end_time_f', code=None):
                     messages.error(request	,'Please do not change the fields')
            return render(request,self.template,{'form':form})
        

############################################################ View for listing requested matches ###########################################################################
@method_decorator(login_required,name='dispatch')
class RequestedMatchesView(View):
    def get(self, request, *args, **kwargs):
        print(request.user.username)
        context={}
        id_list=RequestModel.objects.filter(username=request.user.username,status="Pending").values_list('match_id',flat=True).order_by("-id")
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
        id_list1=RequestModel.objects.filter(username=request.user.username,status="Accepted").values_list('match_id',flat=True).order_by("-id")
        jum=MatchModel.objects.filter(status="Upcoming",id__in=list(id_list1)).exclude(creator=request.user.username).values().order_by("-id")#joined upcoming matches
        id_list2=RequestModel.objects.filter(username=request.user.username,status="Accepted").values_list('match_id',flat=True).order_by("-id")
        jcom=MatchModel.objects.filter(status="Completed",id__in=list(id_list2)).exclude(creator=request.user.username).values().order_by("-id")#joined completed matches
        id_list3=RequestModel.objects.filter(username=request.user.username,status="Accepted").values_list('match_id',flat=True).order_by("-id")
        jcam=MatchModel.objects.filter(status="Cancelled",id__in=list(id_list3)).exclude(creator=request.user.username).values().order_by("-id")#joined cancelled matches
        crum=MatchModel.objects.filter(creator=request.user.username,locality__iexact=request.user.location,status="Upcoming").order_by("-id") #created upcoming matches
        crcom=MatchModel.objects.filter(creator=request.user.username,locality__iexact=request.user.location,status="Completed").order_by("-id") #created completed matches
        crcam=MatchModel.objects.filter(creator=request.user.username,locality__iexact=request.user.location,status="Cancelled").order_by("-id") #created cancelled matches
        reqcan=RequestModel.objects.filter(username=request.user.username,status="Cancelled").order_by("-id")#requests cancelled
        reqrej=RequestModel.objects.filter(username=request.user.username,status="Rejected").order_by("-id")#requests rejected
        id_list4=MatchModel.objects.filter(creator=request.user.username,locality__iexact=request.user.location).values_list('id',flat=True).order_by("-id")
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
        requests=RequestModel.objects.filter(status='Pending',match_id__in=list(id_list)).values().order_by("-id")
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
                    requesti.save()
                    match_id=requesti.match_id.pk
                    print(match_id,type(match_id))
                    obj=MatchModel.objects.get(id=match_id)
                    obj.slot_available=obj.slot_available-1
                    if obj.slot_available<=0:
                             messages.error(request	,'Slots are full. User cant be selected')
                             return HttpResponseRedirect(reverse('requests'))
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
                user_location=request.user.location
                location_list=user_location.split(",")
                matches=MatchModel.objects.filter(id=id)

                
                if len(matches) == 1:
                    match = matches[0]
                if len(matches) == 0:
                    return render(request,'errors/error404.html',{})
                print("##################### INSIDE JOIN MATCHES #########################",match)
                joined=RequestModel.objects.filter(status='Accepted',match_id=match.pk).values().order_by("id")
                request.session['id']=match.id 
                print("#### Match.Category #####",match.category,type(match.category))
                data={
                    'category':match.category,
                    'date':match.date,
                    'start_time':match.start_time.astimezone(timezone('Asia/Kolkata')).strftime("%H:%M:%S"),
                    'end_time':match.end_time.astimezone(timezone('Asia/Kolkata')).strftime("%H:%M:%S"),
                    'locality':match.locality,
                    'username':request.user.username,
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
            data={
                    'category':requested_match.category.id,
                    'date':requested_match.date,
                    'start_time':requested_match.start_time.astimezone(timezone('Asia/Kolkata')).strftime("%H:%M:%S"),
                    'end_time':requested_match.end_time.astimezone(timezone('Asia/Kolkata')).strftime("%H:%M:%S"),
                    'locality':requested_match.locality,
                    'username':request.user.username,
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
        form = createtournamentForm(data,request=request)
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


            TournamentRequestModel.objects.create(tournament_id=form_cf,category=form.cleaned_data['category'],username=form.cleaned_data['creator'],phoneno=request.user.phone,status="Accepted",start_date=form.cleaned_data['start_date'],end_date=form.cleaned_data['end_date'],start_time=form.cleaned_data['start_time'],end_time=form.cleaned_data['end_time'],locality=form.cleaned_data['locality'])
            messages.success(request	,'Your tournament has been succesfully created. Visit My tournament to see .')
            return HttpResponseRedirect(reverse('create-tournament'))

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
            updatedRecord. start_date = form.cleaned_data['start_date']
            updatedRecord. end_date = form.cleaned_data['end_date']
            updatedRecord. start_time = start_datetime
            updatedRecord. end_time = end_datetime
            updatedRecord. locality = form.cleaned_data['locality']
            updatedRecord. teams = form.cleaned_data['teams']
            updatedRecord. team_space_available = form.cleaned_data['team_space_available']
            updatedRecord.save()
            messages.success(request	,'Your tournament has been successfully edited.')
            TournamentRequestModel.objects.filter(tournament_id=updatedRecord).update(category=form.cleaned_data['category'],username=form.cleaned_data['creator'],phoneno=request.user.phone,status="Accepted",start_date=form.cleaned_data['start_date'],end_date=form.cleaned_data['end_date'],start_time=form.cleaned_data['start_time_f'],end_time=form.cleaned_data['end_time_f'],locality=form.cleaned_data['locality'])
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
                location_list=user_location.split(",")
                tournament=TournamentModel.objects.filter(id=id)

                # tournament=TournamentModel.objects.filter(id=id,locality=request.user.location)
                # if len(tournament) == 1:
                #     tournament = tournament[0]
                # if len(tournament) == 0:
                #     return render(request,'errors/error404.html',{})
                print("##################### INSIDE JOIN MATCHES #########################",tournament)
                a=TournamentRequestModel.objects.filter(status='Accepted',tournament_id=tournament.pk).values().order_by("id")
                request.session['id']=tournament.id 
                print("#### Match.Category #####",tournament.category,type(tournament.category))
                data={
                    'category':tournament.category,
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
                # form=RequestForm(data,request=request)
                # print(form)
                context ={'is_tournamentrequestform':True ,'tournament':tournament,'a':a,'data':data}
                print(context)
                return render(request, 'Tournaments/all-tournaments.html',context)
        # except:
        #     pass
    def post(self, request, *args, **kwargs):
            tournament_id=request.session.get('id')
            print(tournament_id)
            tournament=TournamentModel.objects.filter(id=tournament_id)
            if len(tournament) == 1:
                requested_tournament = tournament[0]
            data={
                    'category':requested_tournament.category.id,
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
            form=TournamentRequestForm(data,request=request)
            print(form)
            if form.is_valid():
                print("kikikiki")
                obj=form.save(commit=False)
                obj.tournament_id=requested_tournament
                obj.save()
                return  HttpResponseRedirect(reverse('all-tournaments'))
            else:
                messages.error(request	,'Please do not change the fields')
                joined=TournamentRequestModel.objects.filter(status='Accepted',tournament_id=requested_tournament.pk).values()
                context ={'is_tournamentrequestform':True ,'tournament':requested_tournament,'joined':joined,'data':data}
                print(context)
                return render(request, 'Tournaments/all-tournaments.html',context)

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
                    obj=TournamentModel.objects.get(id=id)
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
        id = kwargs.pop('id')

        turf = UserModel.objects.filter(id=id).first()  
        images = TurfGallery.objects.filter(username = "tr001").values()

        context = {'id': id,
                    'turf':turf,
                    'media_url':settings.MEDIA_URL,
                    'images':images}
        return render(request, 'turf/turf_profile.html',context)
