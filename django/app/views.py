from django.shortcuts import render
from django.views.generic import View


# Create your views here.

class Test(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'layouts/base_boxed_fancy.html',{ })

class Signin(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/sign-up.html',{ })