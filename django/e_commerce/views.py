from email.mime import image
from multiprocessing import context
from select import select
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.generic import View
from .forms import addStockForm, addToCartForm ,billingAddressForm
from .models import CartModel, CheckoutModel, ProductsModel,BillingAddressModel
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
        cartData = CartModel.objects.filter(username = request.user.username)


        cartorbuy = CartModel.objects.filter(username = request.user.username).values_list('product_id')
        cartorbuylist = []
        for i in cartorbuy:
            cartorbuylist = cartorbuylist + list(i)

        totalPrice = CartModel.objects.filter(username = request.user.username).values_list('quantity','price')
        totalAmount = 0
        totalItemCount = CartModel.objects.filter(username = request.user.username).count()
        for i in totalPrice:
            totalAmount = totalAmount + (i[0]*i[1])
        context = {
            'default': default,
            'media_url':settings.MEDIA_URL,
            'cartForm':cartForm,
            'cartData':cartData,
            'cartorbuylist':cartorbuylist,
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

        shipping_address = BillingAddressModel.objects.filter(username=request.user.username)
        form = billingAddressForm()

        num = int(random.random()*99999)
        cartData = CartModel.objects.filter(username = request.user.username)
        totalPrice = CartModel.objects.filter(username = request.user.username).values_list('quantity','price')
        totalAmount = 0
        totalItemCount = CartModel.objects.filter(username = request.user.username).count()
        if cartData :
            for i in totalPrice:
            
                totalAmount = totalAmount + (i[0]*i[1])


                context = {
                    'shipping_address': shipping_address if shipping_address else None,
                    'totalAmount':totalAmount,
                    'totalItemCount':totalItemCount,
                    'cartData':cartData,
                    'num':num,
                    'form': form,
                    
                }


                return render(request,'e_commerce/checkout.html',context)
        else :

            return HttpResponseRedirect(reverse('shop'))


    def post(self,request, *args, **kwargs):
        if request.method == 'POST':  
            form = billingAddressForm(request.POST)
            if form.is_valid(): 

                if request.user.username == request.POST['username']:

                    if BillingAddressModel.objects.filter(username = request.user.username):

                        updatedRecord = BillingAddressModel.objects.get(username=request.POST['username'])

                        updatedRecord.firstname = request.POST['firstname']

                        updatedRecord.contactnumber = request.POST['contactnumber']

                        updatedRecord.houseno = request.POST['houseno']

                        updatedRecord.landmark = request.POST['landmark']

                        updatedRecord.location = request.POST['location']

                        updatedRecord.state = request.POST['state']

                        updatedRecord.pincode = request.POST['pincode']

                        updatedRecord.save()

                        

                        messages.success(request, 'Billing Address Updated...')
                        
                        return HttpResponseRedirect(reverse('checkout')) 

                    else :

                        form.save()
                        messages.success(request, 'Billing Address Added...')
                        return HttpResponseRedirect(reverse('checkout'))

                else :

                    messages.error(request, 'Enter Valid Username...')
                    return HttpResponseRedirect(reverse('checkout'))

            else:  
                print(form.errors,"sdgfjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
                messages.error(request, 'Form Validation Failed...')
                return HttpResponseRedirect(reverse('checkout'))
        

class OrderView(View):
    def get(self, request, id ,*args, **kwargs):

        # select cartDetails
        shipping_address = BillingAddressModel.objects.filter(username=request.user.username)

        if shipping_address :


            cartData = CartModel.objects.filter(username = request.user.username).values_list('product_name','quantity')

            # subtract the quantity from the stock quantity

            if cartData :
                for i in cartData :

                    productQty = ProductsModel.objects.filter(product_name=i[0]).values_list('quantity')[0][0]

                    ProductsModel.objects.filter(product_name = i[0]).update(quantity = productQty - i[1])
            
            # insert the order to ordermodel
            
                for i in CartModel.objects.filter(username = request.user.username).values_list() :

                    CheckoutModel.objects.create(orderno=id,username=i[1],
                                                 product_id=i[2],
                                                 product_name=i[3],
                                                 price=i[4],
                                                 quantity=i[5],
                                                 image=i[6],
                                                 date=datetime.now().date()
                                                )

                # delete the cartData

                CartModel.objects.filter(username = request.user.username).delete()

            messages.success(request, 'Your order confirmed successfully')
            
            return HttpResponseRedirect(reverse('shop'))
        
        else :

            messages.warning(request, 'Please fill your billing address')
            return HttpResponseRedirect(reverse('checkout'))

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

                    updatedRecord.price = request.POST['price']
                    
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



class HtoL_Filter(View):
    def get(self,request,*args, **kwargs):
        highPrice = ProductsModel.objects.order_by('-price').all()
        cartForm = addToCartForm()
        cartorbuy = CartModel.objects.filter(username = request.user.username).values_list('product_id')
        cartorbuylist = []
        for i in cartorbuy:
            cartorbuylist = cartorbuylist + list(i)
            

        context = {
            'default': highPrice,
            'cartForm': cartForm,
            'media_url':settings.MEDIA_URL,
            'cartorbuylist':cartorbuylist,
            


        }
        return render(request, 'e_commerce/productlist.html',context)



class LtoH_Filter(View):
    def get(self,request,*args, **kwargs):
        lowPrice = ProductsModel.objects.order_by('price').all()
        cartForm = addToCartForm()
        cartorbuy = CartModel.objects.filter(username = request.user.username).values_list('product_id')
        cartorbuylist = []
        for i in cartorbuy:
            cartorbuylist = cartorbuylist + list(i)
            

        context = {
            'default': lowPrice,
            'cartForm': cartForm,
            'media_url':settings.MEDIA_URL,
            'cartorbuylist':cartorbuylist,
            


        }
        return render(request, 'e_commerce/productlist.html',context)


class AtoZ_Filter(View):
    def get(self,request,*args, **kwargs):

        AtoZ = ProductsModel.objects.order_by('product_name').all()
        cartForm = addToCartForm()
        cartorbuy = CartModel.objects.filter(username = request.user.username).values_list('product_id')
        cartorbuylist = []
        for i in cartorbuy:
            cartorbuylist = cartorbuylist + list(i)
            

        context = {
            'default': AtoZ,
            'cartForm': cartForm,
            'media_url':settings.MEDIA_URL,
            'cartorbuylist':cartorbuylist,
            

        }
        return render(request, 'e_commerce/productlist.html',context)


class Latest_Filter(View):
    def get(self,request,*args, **kwargs):

        latest = ProductsModel.objects.order_by('-id').all()
        cartForm = addToCartForm()
        cartorbuy = CartModel.objects.filter(username = request.user.username).values_list('product_id')
        cartorbuylist = []
        for i in cartorbuy:
            cartorbuylist = cartorbuylist + list(i)
            

        context = {
            'default': latest,
            'cartForm': cartForm,
            'media_url':settings.MEDIA_URL,
            'cartorbuylist':cartorbuylist,
            


        }
        return render(request, 'e_commerce/productlist.html',context)


class SearchProduct(View):
    def post(self, request, *args, **kwargs):
        cartForm = addToCartForm()
        cartorbuy = CartModel.objects.filter(username = request.user.username).values_list('product_id')
        cartorbuylist = []
        for i in cartorbuy:
            cartorbuylist = cartorbuylist + list(i)
        search_word = request.POST.get('searchproduct')
        result = ProductsModel.objects.filter(product_name__icontains=search_word)

        context = {
                    'default': result,
                    'cartForm': cartForm,
                    'media_url':settings.MEDIA_URL,
                    'cartorbuylist':cartorbuylist,
                    'is_searching' : True,
                    'search_KW' : search_word,


                }
        return render(request, 'e_commerce/productlist.html',context)


class PurchaseHistoryView(View):
    def get(self, request,*args, **kwargs):
        purchasedata = CheckoutModel.objects.all()
        purchasedatauser = CheckoutModel.objects.filter(username = request.user.username)

        context = {
            'puchasedata': purchasedata,
            'purchasedatauser' : purchasedatauser,
        }
        return render(request, 'e_commerce/purchasehistory.html',context)


class UpdateOrderStatusView(View) :
    def get(self, request, id, *args, **kwargs):

        updatedRecord = CheckoutModel.objects.get(id=id)

        if updatedRecord.status == "Awaiting Fulfillment":
            
            updatedRecord.status = "Shipped"
            updatedRecord.save()
            messages.success(request, 'Order Confirmed...')



        return HttpResponseRedirect(reverse('puchasehistory'))

class OrderDetailsView(View):
    def get( self, request, id, *args, **kwargs):
        order = CheckoutModel.objects.filter(orderno=id)
        billingAddressData = BillingAddressModel.objects.filter(username = request.user.username).first()
        if order.count() == 1:
            context = {
                'order': order,
                'media_url':settings.MEDIA_URL,
                'billingAddressData': billingAddressData

            }
            return render(request,'e_commerce/orderdetails.html',context)
        else:
            context = {
                'order': order,
                'oneorder': order.first(),
                'media_url':settings.MEDIA_URL,
                'billingAddressData': billingAddressData

            }
            return render(request,'e_commerce/orderdetails.html',context)

            




