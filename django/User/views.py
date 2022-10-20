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
            category=request.POST.get('id_category')
            date=request.POST.get('id_date')
            time=request.POST.get('id_time')
            username=request.user.username
            phoneno=request.user.phone
            location=request.POST.get('id_locality')
            match_id=request.POST.get('id')
            selected_match=MatchModel.objects.get(id=match_id)
            print(category,date,time,username,phoneno,location,match_id)
            RequestModel.objects.create(match_id=selected_match,category=category,username=username,phoneno=phoneno,status="Pending",date=date,time=time,locality=location)
            return HttpResponseRedirect(reverse('matches'))


#############################################################    View for matches user has created or joined  ###########################################################
@method_decorator(login_required,name='dispatch')
class MyMatchesView(View):
    def get(self, request, *args, **kwargs):
        print(request.user.username)
        context={}
        id_list=RequestModel.objects.filter(username=request.user.username,status="Accepted").values_list('match_id',flat=True)
        print(list(id_list))
        matches=MatchModel.objects.filter(id__in=list(id_list))
        context['matches']=matches
        return render(request, 'Matches/my-matches.html',context)


#############################################################   View for
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




@method_decorator(login_required,name='dispatch')
class JoinMatchesView(View):
    def get(self, request,id, *args, **kwargs):
        reqdata=MatchModel.objects.get(id=id)
        data={
                "category":reqdata.category,
                "date":reqdata.date,
                "time":reqdata.time,
                "username":reqdata.creator,
                "locality":reqdata.locality,
                "match_id":id,
                "phoneno":+98765487654,
                "status":"Pending"
        }
        context ={}
        form = RequestForm(data)
        context['form']=form
        return render(request, 'Matches/join-matches.html',context)
    def post(self, request, *args, **kwargs):
         if request.method == 'POST':
            form =RequestForm(request.POST )
            print(form)




class TurfsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'turf/main.html',{ })