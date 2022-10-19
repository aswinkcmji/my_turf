from tkinter.tix import Form
from django.shortcuts import render
from django.views.generic import View
from .forms import addStockForm
from .models import ProductsModel
from django.conf import settings  


class E_commercePage(View):
    def get(self, request ,*args, **kwargs):
        ecom_data = ProductsModel.objects.all()
        print("heloooooooooooooooooo",ecom_data)
        return render(request,'e_commerce/shop.html',{"ecom_data":ecom_data, 'media_url':settings.MEDIA_URL})


        