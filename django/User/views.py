from datetime import date
from email import message
from multiprocessing import context
from django.shortcuts import render
from .models import MatchModel,RequestModel
from django.views.generic import View
from .forms import RequestForm, updatematchform
from django.http import HttpResponseRedirect
from django.urls import is_valid_path, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from .forms import creatematchForm,updatematchform
from datetime import datetime,timedelta
from django.utils import timezone
from django.contrib import messages
# from .models import slotModel

# Create your views here.

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html',{ })




########################################################## View for listing all matches in user locality which user hasn't requested or joined or created ################################################################################ 
@method_decorator(login_required,name='dispatch')
class AllMatchesView(View):
        def get(self, request, *args, **kwargs):
                print(request.user.username)
                # context={}
                id_list=RequestModel.objects.filter(username=request.user.username).values_list('match_id',flat=True)
                matches=MatchModel.objects.filter(locality=request.user.location,status="Upcoming").exclude(id__in=list(id_list))
                form=RequestForm(request=request)
                print("hllo",matches)
                # context['matches']=matches
                # context['form']=form
                context ={'RequestForm': form ,'is_requestform':False , 'matches':matches}
                print(context)
                return render(request, 'Matches/all-matches.html',context)


#############################################################    View for matches user has created or joined  ###########################################################
@method_decorator(login_required,name='dispatch')
class MyMatchesView(View):
    def get(self, request, *args, **kwargs):
        print(request.user.username)
        print(datetime.now())
        context={}
        id_list=RequestModel.objects.filter(username=request.user.username,status="Accepted").values_list('match_id',flat=True)
        print(list(id_list))
        matches=MatchModel.objects.filter(id__in=list(id_list))
        context['matches']=matches
        context[request]=request
        return render(request, 'Matches/my-matches.html',context)


#############################################################   View for creating matches ###############################################################################
@method_decorator(login_required,name='dispatch')
class CreateMatchesView(View):
    template = 'Matches/create-matches.html'
    def get(self, request, *args, **kwargs):
        print(datetime.now()+timedelta(hours=1))
        end_time=(datetime.now()+timedelta(hours=1)).strftime('%H:%M:%S')
        print(end_time)
        now = timezone.now()
        print(now)
        data={
            'category':'Cricket',
            'date':datetime.now().date(),
            'start_time':datetime.now().strftime('%H:%M:%S'),
            'end_time':end_time,
            'locality':request.user.location,
            'creator' : request.user.username,
            "status": "Upcoming",
            "slot_available": 0,
            "slots": 2,
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
            obj=form.save()
            RequestModel.objects.create(match_id=obj,category=form.cleaned_data['category'],username=form.cleaned_data['creator'],phoneno=request.user.phone,status="Accepted",date=form.cleaned_data['date'],start_time=form.cleaned_data['start_time'],end_time=form.cleaned_data['end_time'],locality=form.cleaned_data['locality'])
            messages.success(request	,'Your match has been succesfully created. Visit My Match to see .')
            return HttpResponseRedirect(reverse('create-matches'))

        else:
            # print(form.errors['start_time'])
            messages.error(request	,'Please do not change the fields')
            return render(request,self.template,{'form':form})
        

############################################################ View for listing requested matches ###########################################################################
@method_decorator(login_required,name='dispatch')
class RequestedMatchesView(View):
    def get(self, request, *args, **kwargs):
        print(request.user.username)
        context={}
        id_list=RequestModel.objects.filter(username=request.user.username,status="Pending").values_list('match_id',flat=True)
        print(list(id_list))
        matches=MatchModel.objects.filter(id__in=list(id_list))
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
        id_list1=RequestModel.objects.filter(username=request.user.username,status="Accepted").values_list('match_id',flat=True)
        jum=MatchModel.objects.filter(status="Upcoming",id__in=list(id_list1)).exclude(creator=request.user.username).values()#joined upcoming matches
        id_list2=RequestModel.objects.filter(username=request.user.username,status="Accepted").values_list('match_id',flat=True)
        jcom=MatchModel.objects.filter(status="Completed",id__in=list(id_list2)).exclude(creator=request.user.username).values()#joined completed matches
        id_list3=RequestModel.objects.filter(username=request.user.username,status="Accepted").values_list('match_id',flat=True)
        jcam=MatchModel.objects.filter(status="Cancelled",id__in=list(id_list3)).exclude(creator=request.user.username).values()#joined cancelled matches
        crum=MatchModel.objects.filter(creator=request.user.username,locality=request.user.location,status="Upcoming") #created upcoming matches
        crcom=MatchModel.objects.filter(creator=request.user.username,locality=request.user.location,status="Completed") #created completed matches
        crcam=MatchModel.objects.filter(creator=request.user.username,locality=request.user.location,status="Cancelled") #created cancelled matches
        reqcan=RequestModel.objects.filter(username=request.user.username,status="Cancelled")#requests cancelled
        reqrej=RequestModel.objects.filter(username=request.user.username,status="Rejected")#requests rejected
        id_list4=MatchModel.objects.filter(creator=request.user.username,locality=request.user.location).values_list('id',flat=True)
        reqaccep=RequestModel.objects.filter(match_id__in=list(id_list4),status="Accepted")
        reqrejec=RequestModel.objects.filter(match_id__in=list(id_list4),status="Rejected")
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
class TurfsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'turf/main.html',{ })

############################################################## View for editing matches created by user #####################################################################
class EditMatchesView(View):
    def get(self, request,id, *args, **kwargs):
        editobj=MatchModel.objects.get(id=id)
        data={
            'category':editobj.category,
            'date':editobj.date,
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
            updatedRecord = MatchModel.objects.get(id=match_id)
            updatedRecord. category = form.cleaned_data['category']
            updatedRecord. date = form.cleaned_data['date']
            updatedRecord. start_time = form.cleaned_data['start_time']
            updatedRecord. end_time = form.cleaned_data['end_time']
            updatedRecord. locality = form.cleaned_data['locality']
            updatedRecord. slots = form.cleaned_data['slots']
            updatedRecord. slot_available = form.cleaned_data['slot_available']
            updatedRecord.save()
            messages.success(request	,'Your match has been succesfully edit. Visit My Match to see .')
            return render(request,'Matches/edit-matches.html',{'form':updatematchform(request.POST,request=request)})
            # RequestModel.objects.create(match_id=obj,category=form.cleaned_data['category'],username=form.cleaned_data['creator'],phoneno=request.user.phone,status="Accepted",date=form.cleaned_data['date'],time=form.cleaned_data['time'],locality=form.cleaned_data['locality'])
        else:
            print(form.errors.as_data())
            messages.error(request	,'Please do not change the fields')
            return render(request,'Matches/edit-matches.html',{'form':updatematchform(request.POST,request=request)})
        # return HttpResponseRedirect(reverse('my-matches'))



##################################################################### View for Requests viewing #######################################################################
class RequestsView(View):
    def get(self, request,*args, **kwargs):
        id_list=MatchModel.objects.filter(creator=request.user.username,status="Upcoming").values_list('id',flat=True)
        print(list(id_list))
        requests=RequestModel.objects.filter(status='Pending',match_id__in=list(id_list)).values()
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
            messages.error(request	,'NO user selected')
            return HttpResponseRedirect(reverse('requests'))
######################################################################### View for joining matches #######################################################
@method_decorator(login_required,name='dispatch')
class  JoinMatchView(View):
    def get(self, request,id, *args, **kwargs):
                matches=MatchModel.objects.filter(id=id,locality=request.user.location)
                if len(matches) == 1:
                    match = matches[0]
                if len(matches) == 0:
                    return render(request,'errors/error404.html',{})
                joined=RequestModel.objects.filter(status='Accepted',match_id=match.pk).values()
                request.session['id']=match.id
                request.session['category']=match.category
                # request.session['date']=match.date
                # request.session['start_time']=match.start_time
                # request.session['end_time']=match.end_time
                request.session['locality']=match.locality
                request.session['status']="Pending"
                data={
                    'category':match.category,
                    'date':match.date,
                    'start_time':match.start_time,
                    'end_time':match.end_time,
                    'locality':match.locality,
                    'username':request.user.username,
                    'status':"Pending",
                    'phoneno': request.user.phone,
                    'match_id':match.id,
                }
                form=RequestForm(data,request=request)
                print(form)
                context ={'RequestForm': form ,'is_requestform':True ,'match':match,'joined':joined}
                print(context)
                return render(request, 'Matches/all-matches.html',context)
        # except:
        #     pass
    def post(self, request, *args, **kwargs):

        try:
            matchid=int(request.POST['match_id'])
        except:
            return  HttpResponseRedirect(reverse('matches'))
        if matchid!=request.session.get('id'):
            id=int(request.session.get('id'))
            matches=MatchModel.objects.filter(id=id)
            if len(matches) == 1:
                requested_match = matches[0]
            context ={'RequestForm': RequestForm(request.POST,request=request) ,'is_requestform':True ,'match':requested_match}
            return render(request, 'Matches/all-matches.html',context)
        else:
            match_id=request.session.get('id')
            print(match_id)
            matches=MatchModel.objects.filter(id=match_id)
            if len(matches) == 1:
                requested_match = matches[0]
            form=RequestForm(request.POST,request=request)
            print(form)
            if form.is_valid():
                print("kikikiki")
                obj=form.save(commit=False)
                obj.match_id=requested_match
                obj.save()
                return  HttpResponseRedirect(reverse('matches'))
            else:
                messages.error(request	,'Please do not change the fields')
                context ={'RequestForm': RequestForm(request.POST,request=request) ,'is_requestform':True ,'match':requested_match}
                print(context)
                return render(request, 'Matches/all-matches.html',context)

