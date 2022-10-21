from datetime import date
from django.shortcuts import render
from .models import MatchModel,RequestModel
from django.views.generic import View
from .forms import RequestForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from .forms import creatematchForm
from datetime import datetime
# from .models import slotModel

# Create your views here.

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html',{ })
# class Shop(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'e_commerce/shop.html',{ })

# class Signin(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'accounts/sign-up.html',{ })




########################################################## View for listing all matches in user locality which user hasn't requested or joined ################################################################################ 
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
            # form.fields['match_id'].initial = selected_match.id
            if form.is_valid:
                print("kikikiki")
                obj=form.save(commit=False)
                obj.match_id=selected_match
                obj.save()
            else:
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

        form = creatematchForm()
        # user = request.user
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",form.options)
        context = {'form': form,
                    'data': 'Add match',
                    # 'user': user,
                    }
        
        return render(request,self.template,context)


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


################################################################   View for join matches ###################################################################################
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
        return render(request, 'Matches/match-history.html')

############################################################# View for listing all turfs in user locality ####################################################################
class TurfsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'turf/main.html',{ })