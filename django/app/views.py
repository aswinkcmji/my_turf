from django.shortcuts import render
from django.views.generic import View


# Create your views here.

class Test(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html',{ })

class Signin(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/sign-up.html',{ })

class Turfs(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'turf/main.html',{ })