from django.shortcuts import render
from django.views.generic import View


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
        return render(request, 'Matches/all-matches.html',{ })
class MyMatchesView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Matches/my-matches.html',{ })
class CreateMatchesView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Matches/create-matches.html',{ })
class TurfsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'turf/main.html',{ })