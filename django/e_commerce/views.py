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
from datetime import datetime,timedelta, date, time
# from pytz import timezone

class E_commercePage(View):
    def get(self, request ,*args, **kwargs):
        cartForm = addToCartForm()
        default = ProductsModel.objects.all()
        highPrice = ProductsModel.objects.order_by('-price').all()
        lowPrice = ProductsModel.objects.order_by('price').all()
        AtoZ = ProductsModel.objects.order_by('product_name').all()
        latest = ProductsModel.objects.order_by('-id').all()

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
            'default': default,
            'hTol' : highPrice,
            'lToh' : lowPrice,
            'aToz' : AtoZ,
            'latest' : latest,
            'media_url':settings.MEDIA_URL,
            'cartForm':cartForm,
            'cartData':cartData,
            # 'cartorbuylist':cartorbuylist,
            'totalAmount':totalAmount,
            'totalItemCount':totalItemCount,
            # 'date':datetime.date()
        }
        print(totalItemCount,"hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")

        return render(request,'e_commerce/shop.html',context)
    
    

    def post(self,request,*args,**kwargs):
        if request.method == 'POST':  
            form = addToCartForm(request.POST)
            product_tot_qty = ProductsModel.objects.filter(product_name = request.POST['product_name']).values_list('quantity')[0][0]
            if form.is_valid():
                if int(request.POST.get("quantity")) <=0 :
                    messages.error(request,"Quantity must be greater than 0")
                    return HttpResponseRedirect(reverse('shop'))
                elif int(request.POST.get("quantity")) > int(product_tot_qty):
                    messages.error(request,"Unavilable Stock")
                    return HttpResponseRedirect(reverse('shop'))
                else:
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
        return HttpResponseRedirect(reverse('cartdetails'))

class Checkout(View):
    def get(self , request, *args, **kwargs):


        num = int(random.random()*99999)
        cartData = CartModel.objects.filter(username = request.user.username)
        totalPrice = CartModel.objects.filter(username = request.user.username).values_list('quantity','price')
        totalAmount = 0
        totalItemCount = CartModel.objects.filter(username = request.user.username).count()

        if cartData :
            for i in totalPrice:
            
                totalAmount = totalAmount + (i[0]*i[1])


                context = {
                    
                    'totalAmount':totalAmount,
                    'totalItemCount':totalItemCount,
                    'cartData':cartData,
                    'num':num,
                    
                }


                return render(request,'e_commerce/checkout.html',context)
        else :

            return HttpResponseRedirect(reverse('shop'))

        

class OrderView(View):
    def get(self, request, id ,*args, **kwargs):

        # select cartDetails

        cartData = CartModel.objects.filter(username = request.user.username).values_list('product_name','quantity')

        # subtract the quantity from the stock quantity

        if cartData :
            for i in cartData :

                productQty = ProductsModel.objects.filter(product_name=i[0]).values_list('quantity')[0][0]

                ProductsModel.objects.filter(product_name = i[0]).update(quantity = productQty - i[1])
        
        # insert the order to ordermodel
        
            for i in CartModel.objects.filter(username = request.user.username).values_list() :

                CheckoutModel.objects.create(orderno=id,username=i[1],product_id=i[2],product_name=i[3],price=i[4],quantity=i[5],image=i[6],date=datetime.now().date())

            # delete the cartData

            CartModel.objects.filter(username = request.user.username).delete()

        messages.success(request, 'your order confirmed successfully')
        
        return HttpResponseRedirect(reverse('shop'))

class OutOfStock(View):
    def get(self, request, *args, **kwargs):

        messages.warning(request, 'OutOfStock')

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

                if int(request.POST.get('quantity')) >= 1 :

                    updatedRecord = ProductsModel.objects.get(id=request.POST['product_id'])

                    updatedRecord.product_name = request.POST['product_name']

                    updatedRecord. price = request.POST['price']
                    
                    updatedRecord.quantity = request.POST['quantity']
                    
                    updatedRecord.image = request.FILES['image']

                    updatedRecord.save()

                    messages.success(request, 'Stock Updated Successfully')
                    
                    return HttpResponseRedirect(reverse('stocktable'))  
                
                else :

                    messages.error(request,"Quantity must be greater than 1 !")

            else:  
                
                form = addStockForm()    
                
        return HttpResponseRedirect(reverse('stocktable'))

class DeleteStock(View):
    def get(self, request,id, *args,**kwargs):
        item = ProductsModel.objects.get(id=id)
        item.delete()
        return HttpResponseRedirect(reverse('stocktable'))


class CartDetailsView(View):
    def get(self, request,*args, **kwargs):
        cartData = CartModel.objects.filter(username = request.user.username)
        totalPrice = CartModel.objects.filter(username = request.user.username).values_list('quantity','price')
        totalAmount = 0
        totalItemCount = CartModel.objects.filter(username = request.user.username).count()
        for i in totalPrice:
            totalAmount = totalAmount + (i[0]*i[1])
        context={
            'cart': cartData,
            'media_url':settings.MEDIA_URL,
            'totalItemCount':totalItemCount,
            'totalAmount':totalAmount,


        }
        return render(request,'e_commerce/cartPage.html',context)

def increaseBtn(request,id):
    item = CartModel.objects.get(id=id)
    item.update()
    return HttpResponseRedirect(reverse('stocktable'))
