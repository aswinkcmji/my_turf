from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.generic import View
from .forms import addToCartForm
from .models import ProductsModel
from django.conf import settings  


class E_commercePage(View):
    def get(self, request ,*args, **kwargs):
        cartForm = addToCartForm()
        ecom_data = ProductsModel.objects.all()
        context = {
            'ecom_data':ecom_data, 
            'media_url':settings.MEDIA_URL,
            'cartForm':cartForm
        }
        helo="hello"
        return render(request,'e_commerce/shop.html',context)
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            cartForm = addToCartForm(request.POST)
            if cartForm.is_valid():
                cartForm.save()
            
            return redirect(reverse('shop')) 

        