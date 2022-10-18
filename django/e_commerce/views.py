from webbrowser import get
from django.shortcuts import render
from django.views.generic import View

class E_commercePage(View):
    def get(self, request ,*args, **kwargs):
        return render(request, 'e_commerce/shop.html',{ })