from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.generic import View
from e_commerce.forms import addStockForm
from e_commerce.models import ProductsModel
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


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
        return render(request,"turf/turf_dashboard.html",{})

@method_decorator(login_required,name='dispatch')
class TurfSchedule(View):
    def get(self,request):
        return render(request,"turf/schedule.html",{})