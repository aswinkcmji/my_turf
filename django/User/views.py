from datetime import date
from multiprocessing import context
from django.shortcuts import render
from .models import MatchModel,RequestModel
from django.views.generic import View
from .forms import RequestForm, updatematchform
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from .forms import creatematchForm,updatematchform
from datetime import datetime
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
        context={}
        id_list=RequestModel.objects.filter(username=request.user.username).values_list('match_id',flat=True)
        matches=MatchModel.objects.filter(locality=request.user.location,status="Upcoming").exclude(id__in=list(id_list))
        form=RequestForm()
        print("hllo",matches)
        context['matches']=matches
        context['form']=form
        return render(request, 'Matches/all-matches.html',context)
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            print("hello")
            match_id=request.POST.get('id')
            try:
                selected_match=MatchModel.objects.get(id=match_id,status="Upcoming")
            except:
                return render(request, 'errors/error404.html')
            category=request.POST.get('id_category')
            date=request.POST.get('id_date')
            time=request.POST.get('id_time')
            username=request.user.username
            phoneno=request.user.phone
            location=request.POST.get('id_locality')
            print(category,date,time,username,phoneno,location,match_id)
            data={
                'category':category,
                'date':date,
                'time':time,
                'username':username,
                'locality':location,
                'status':"Pending",
                # 'match_id':selected_match,
                'phoneno':phoneno,

            }
            form = RequestForm(data)
            print(form)
            # form.fields['match_id'].initial = selected_match.id
            if form.is_valid():
                print("kikikiki")
                obj=form.save(commit=False)
                obj.match_id=selected_match
                obj.save()
            else:
                context={}
                id_list=RequestModel.objects.filter(username=request.user.username).values_list('match_id',flat=True)
                matches=MatchModel.objects.filter(locality=request.user.location,status="Upcoming").exclude(id__in=list(id_list))
                form=RequestForm()
                print("hllo",matches)
                context['matches']=matches
                context['form']=form
                return render(request, 'Matches/all-matches.html',context)
            print(form)
            # RequestModel.objects.create(match_id=selected_match,category=category,username=username,phoneno=phoneno,status="Pending",date=date,time=time,locality=location)
            return HttpResponseRedirect(reverse('matches'))


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
        print(datetime.now().strftime('%H:%M:%S'))
        now = timezone.now()
        print(now)
        data={
            'category':'Cricket',
            'date':datetime.now().date(),
            'time':datetime.now().strftime('%H:%M:%S'),
            'locality':request.user.location,
            'creator' : request.user.username,
            "status": "Upcoming",
            "slot_available": 0,
            "slots": 1,
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
        if form.is_valid():
            print("kikikiki")
            print(form.errors.as_data())
            obj=form.save()
            RequestModel.objects.create(match_id=obj,category=form.cleaned_data['category'],username=form.cleaned_data['creator'],phoneno=request.user.phone,status="Accepted",date=form.cleaned_data['date'],time=form.cleaned_data['time'],locality=form.cleaned_data['locality'])
            messages.success(request	,'Your match has been succesfully edit. Visit My Match to see .')
            return HttpResponseRedirect(reverse('create-matches'))

        else:
            print(form.errors.as_data())
            messages.error(request	,'Please do not change the fields')
            return render(request,self.template,{'form':creatematchForm(request.POST,request)})
        

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
        id_list=RequestModel.objects.filter(username=request.user.username,status="Accepted").values_list('match_id',flat=True)
        jum=MatchModel.objects.filter(status="Upcoming",id__in=list(id_list)).exclude(creator=request.user.username).values()#joined upcoming matches
        id_list=RequestModel.objects.filter(username=request.user.username,status="Accepted").values_list('match_id',flat=True)
        jcom=MatchModel.objects.filter(status="Completed",id__in=list(id_list)).exclude(creator=request.user.username).values()#joined completed matches
        id_list=RequestModel.objects.filter(username=request.user.username,status="Accepted").values_list('match_id',flat=True)
        jcam=MatchModel.objects.filter(status="Cancelled",id__in=list(id_list)).exclude(creator=request.user.username).values()#joined cancelled matches
        crum=MatchModel.objects.filter(creator=request.user.username,locality=request.user.location,status="Upcoming") #created upcoming matches
        crcom=MatchModel.objects.filter(creator=request.user.username,locality=request.user.location,status="Completed") #created completed matches
        crcam=MatchModel.objects.filter(creator=request.user.username,locality=request.user.location,status="Cancelled") #created cancelled matches
        reqcan=RequestModel.objects.filter(username=request.user.username,status="Cancelled")#requests cancelled
        reqrej=RequestModel.objects.filter(username=request.user.username,status="Rejected")#requests rejected
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
            'time':editobj.time,
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
        return render(request,'Matches/join-matches.html',context)
        
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
            updatedRecord. time = form.cleaned_data['time']
            updatedRecord. locality = form.cleaned_data['locality']
            updatedRecord. slots = form.cleaned_data['slots']
            updatedRecord. slot_available = form.cleaned_data['slot_available']
            updatedRecord.save()
            messages.success(request	,'Your match has been succesfully edit. Visit My Match to see .')
            return render(request,'Matches/join-matches.html',{'form':updatematchform(request.POST,request=request)})
            # RequestModel.objects.create(match_id=obj,category=form.cleaned_data['category'],username=form.cleaned_data['creator'],phoneno=request.user.phone,status="Accepted",date=form.cleaned_data['date'],time=form.cleaned_data['time'],locality=form.cleaned_data['locality'])
        else:
            print(form.errors.as_data())
            messages.error(request	,'Please do not change the fields')
            return render(request,'Matches/join-matches.html',{'form':updatematchform(request.POST,request=request)})
        # return HttpResponseRedirect(reverse('my-matches'))
