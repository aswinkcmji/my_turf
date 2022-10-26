from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.generic import View
from accounts.models import UserModel
from e_commerce.forms import addStockForm
from e_commerce.models import ProductsModel
from django.conf import settings  
from django.views.generic import View
# Create your views here.

class AddStockView(View):
    def get(self, request, *args, **kwargs):
        form = addStockForm()
        return render(request, 'e_commerce/addProduct.html',{'form':form})

    def post(self,request,*args,**kwargs):
        print("helllllllllllllllllllllllllllllllllllllllllllllllll")  
        if request.method == 'POST':  
            form = addStockForm(request.POST, request.FILES)
            if form.is_valid():  
                form.save()  

                # Getting the current instance object to display in the template  
                # img_object = form.instance  
                
                return redirect(reverse('addstock'))  
            else:  
                
                form = addStockForm()  
        
            return render(request, 'e_commerce/addProduct.html',{'form':form})
class Turf_Dashboard(View):
    def get(self,request):

        # turfDetails = UserModel.objects.all().exclude(username="admin")

        turfDetails = UserModel.objects.filter(username = request.user.username).values()
        
        context = {

            'turfDetails': turfDetails,
            'media_url':settings.MEDIA_URL,

        }
        print("==============",context)


        return render(request,'turf/turf_dashboard.html',context)


# class TurfGalleryView(View):
#     def get(self, request, *args, **kwargs):
#         form = 