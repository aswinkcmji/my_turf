from django.shortcuts import render
from .models import MatchModel,RequestModel
from django.views.generic import View
from .forms import RequestForm

# Create your views here.

class Test(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html',{ })
class Shop(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'e_commerce/shop.html',{ })

# class Signin(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'accounts/sign-up.html',{ })

class AllMatchesView(View):
    def get(self, request, *args, **kwargs):
        context={}
        matches=MatchModel.objects.filter(locality="malampuzha",status="Upcoming")
        print("hllo",matches)
        context['matches']=matches
        return render(request, 'Matches/all-matches.html',context)
class MyMatchesView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Matches/my-matches.html',{ })
class CreateMatchesView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Matches/create-matches.html',{ })
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