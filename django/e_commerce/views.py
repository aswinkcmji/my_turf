from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.generic import View
from .forms import addToCartForm
from .models import CartModel, ProductsModel
from django.conf import settings 
from django.http import HttpResponseRedirect
from django.contrib import messages



class E_commercePage(View):
    def get(self, request ,*args, **kwargs):
        cartForm = addToCartForm()
        ecom_data = ProductsModel.objects.all()
        cartData = CartModel.objects.filter(username = request.user.username)
        # cartorbuy = CartModel.objects.filter(username = request.user.username).values_list('product_id')
        # cartorbuylist = []
        # for i in cartorbuy:
        #     cartorbuylist = cartorbuylist + list(i)

        context = {
            'ecom_data':ecom_data, 
            'media_url':settings.MEDIA_URL,
            'cartForm':cartForm,
            'cartData':cartData,
            # 'cartorbuylist':cartorbuylist,
        }
        helo="hello"

        return render(request,'e_commerce/shop.html',context)
    
    

    def post(self,request,*args,**kwargs):
        if request.method == 'POST':  
            form = addToCartForm(request.POST)
            if form.is_valid():  
                cartCount = CartModel.objects.filter(username = request.user.username).count()
                if cartCount < 5 :
                    form.save() 
                    return HttpResponseRedirect(reverse('shop'))
                else:  
                    messages.warning(request, 'Your cart is full Please do purchase...')
        return HttpResponseRedirect(reverse('shop'))  
        
class DeleteStock(View):
    def get(self , request, id,*args, **kwargs):
        item = CartModel.objects.get(id=id)
        item.delete()
        return HttpResponseRedirect(reverse('shop'))