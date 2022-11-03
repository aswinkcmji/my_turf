from email.mime import image
from multiprocessing import context
from select import select
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.generic import View
from .forms import addStockForm, addToCartForm
from .models import CartModel, CheckoutModel, ProductsModel
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.contrib import messages
import random

from django import template

class E_commercePage(View):
    def get(self, request ,*args, **kwargs):
        cartForm = addToCartForm()
        ecom_data = ProductsModel.objects.all()
        cartData = CartModel.objects.filter(username = request.user.username)
        # cartorbuy = CartModel.objects.filter(username = request.user.username).values_list('product_id')
        # cartorbuylist = []
        # for i in cartorbuy:
        #     cartorbuylist = cartorbuylist + list(i)

        totalPrice = CartModel.objects.filter(username = request.user.username).values_list('quantity','price')
        totalAmount = 0
        totalItemCount = CartModel.objects.filter(username = request.user.username).count()
        for i in totalPrice:
            totalAmount = totalAmount + (i[0]*i[1])
        context = {
            'ecom_data':ecom_data, 
            'media_url':settings.MEDIA_URL,
            'cartForm':cartForm,
            'cartData':cartData,
            # 'cartorbuylist':cartorbuylist,
            'totalAmount':totalAmount,
            'totalItemCount':totalItemCount
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
        
class DeleteCartItem(View):
    def get(self , request, id,*args, **kwargs):
        item = CartModel.objects.get(id=id)
        item.delete()
        return HttpResponseRedirect(reverse('shop'))

class Checkout(View):
    def get(self , request, *args, **kwargs):


        num = int(random.random()*99999)
        cartData = CartModel.objects.filter(username = request.user.username)
        totalPrice = CartModel.objects.filter(username = request.user.username).values_list('quantity','price')
        totalAmount = 0
        totalItemCount = CartModel.objects.filter(username = request.user.username).count()
        for i in totalPrice:
            
            totalAmount = totalAmount + (i[0]*i[1])


        context = {
            
            'totalAmount':totalAmount,
            'totalItemCount':totalItemCount,
            'cartData':cartData,
            'num':num,
            
        }


        return render(request,'e_commerce/checkout.html',context)

class OrderView(View):
    def get(self, request, id ,*args, **kwargs):

        # select cartDetails

        cartData = CartModel.objects.filter(username = request.user.username).values_list('product_name','quantity')

        # subtract the quantity from the stock quantity

        for i in cartData :

            productQty = ProductsModel.objects.filter(product_name=i[0]).values_list('quantity')[0][0]

            ProductsModel.objects.filter(product_name = i[0]).update(quantity = productQty - i[1])
        
        # insert the order to ordermodel
        
        for i in CartModel.objects.filter(username = request.user.username).values_list() :

            CheckoutModel.objects.create(orderno=id,username=i[1],product_id=i[2],product_name=i[3],price=i[4],quantity=i[5],image=i[6])

        # delete the cartData

        CartModel.objects.filter(username = request.user.username).delete()

        messages.success(request, 'your order confirmed successfully')
        
        return HttpResponseRedirect(reverse('shop'))

class OutOfStock(View):
    def get(self, request, *args, **kwargs):

        messages.success(request, 'OutOfStock')

        return HttpResponseRedirect(reverse('shop'))


class StockTable(View):
    def get(self, request, *args,**kwargs):

        template = 'e_commerce/list.html'

        ecom_data = ProductsModel.objects.all()

        form = addStockForm()

        context={
            'ecom_data': ecom_data,
            'form': form,
        }

        return render(request, template,context)

    def post(self, request, *args, **kwargs):

        if request.method == 'POST':  
            form = addStockForm(request.POST, request.FILES)
            if form.is_valid(): 
                print(request.POST)

                updatedRecord = ProductsModel.objects.get(id=request.POST['product_id'])

                updatedRecord.product_name = request.POST['product_name']

                updatedRecord. price = request.POST['price']
                
                updatedRecord.quantity = request.POST['quantity']
                
                updatedRecord.image = request.FILES['image']

                updatedRecord.save()
                
                return HttpResponseRedirect(reverse('stocktable'))  
            else:  
                
                form = addStockForm()    
                
        return HttpResponseRedirect(reverse('stocktable'))

class DeleteStock(View):
    def get(self, request,id, *args,**kwargs):
        item = ProductsModel.objects.get(id=id)
        item.delete()
        return HttpResponseRedirect(reverse('stocktable'))
