from datetime import datetime
import json
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.generic import View
from accounts.models import UserModel
from e_commerce.forms import addStockForm
from e_commerce.models import ProductsModel
from django.conf import settings  
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import TurfScheduleForm
from django.utils.dateparse import parse_datetime
from .models import TurfScheduleModel


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

@method_decorator(login_required,name='dispatch')
class TurfSchedule(View):
    def get(self,request):
        turf_schedule   = TurfScheduleModel.objects.filter(turf=request.user)

        addScheduleform = TurfScheduleForm(initial={'turf':request.user})
        context ={'addScheduleform': addScheduleform ,'is_addform':False , 'turf_schedule':turf_schedule}
        return render(request,"turf/schedule.html",context)
    def post(self, request, *args, **kwargs):
        txt_colors= ['rgba(206,32,20)','rgba(8,130,12)', 'rgba(58,87,232)','rgba(235,153,27)','rgba(108,117,125)']
        bg_colors= ['rgba(206,32,20,0.2)','rgba(8,130,12,0.2)', 'rgba(58,87,232,0.2)','rgba(235,153,27,0.2)','rgba(108,117,125,0.4)']
        if request.method == 'POST':
            print(request.POST["color"])
            form = TurfScheduleForm(request.POST)
            

            
            if form.is_valid():
                form2 =form.save(commit=False)
                for key,value in enumerate(bg_colors):
                    
                    if request.POST["color"] == str(key):
                        form2.color_txt =txt_colors[key]
                        form2.color_bg =bg_colors[key]
                # form2.start= parse_datetime(request.POST['start'])
                # form2.end= parse_datetime(request.POST['end'])
                form2.title = request.POST['category']+" - "+request.POST['user']
                form2.turf = request.user
                form2.save()
                    
                    
                    # messages.success(self.request, "Account Created Successfully")
                return HttpResponseRedirect(reverse('turf_schedule'))
                      
            else:
                turf_schedule   = TurfScheduleModel.objects.filter(turf=request.user)
                context ={'addScheduleform': form, 'is_addform':True ,'turf_schedule':turf_schedule}
                return render(request,"turf/schedule.html",context)

@method_decorator(login_required,name='dispatch')
class TurfScheduleEdit(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.pop('id')
        schedule = TurfScheduleModel.objects.filter(id=id).first()
        title = schedule.title.split(' - ')
        editTurfForm = TurfScheduleForm(initial={'category':title[0],'user':title[1] ,'start':schedule.start, 'end':schedule.end, 'turf':schedule.turf})
        context={'addScheduleform':editTurfForm,
                 'is_editform':True,
                 'schedule_id':id}
        return render(request,"turf/schedule.html",context)
    def post(self, request, *args, **kwargs):
        id = kwargs.pop('id')

        txt_colors= ['rgba(206,32,20)','rgba(8,130,12)', 'rgba(58,87,232)','rgba(235,153,27)','rgba(108,117,125)']
        bg_colors= ['rgba(206,32,20,0.2)','rgba(8,130,12,0.2)', 'rgba(58,87,232,0.2)','rgba(235,153,27,0.2)','rgba(108,117,125,0.4)']
        if request.method == 'POST':
            print(request.POST["color"])
            form = TurfScheduleForm(request.POST)
            
            schedule = TurfScheduleModel.objects.filter(id=id).first()
            if form.is_valid():
                
                schedule.title = request.POST['category']+" - "+request.POST['user']
                schedule.start = request.POST['start']
                schedule.end = request.POST['end']
                schedule.turf = request.user
                schedule.category = request.POST['category']
                
                for key,value in enumerate(bg_colors):
                    
                    if request.POST["color"] == str(key):
                        schedule.color_txt = txt_colors[key]
                        schedule.color_bg = bg_colors[key]
                schedule.save()
                    
                    # messages.success(self.request, "Account Created Successfully")
                return HttpResponseRedirect(reverse('turf_schedule'))
            else:
                turf_schedule   = TurfScheduleModel.objects.filter(turf=request.user)
                context =  {'addScheduleform': form, 'is_addform':True ,
                            'turf_schedule':turf_schedule,
                            'is_editform':True,
                            'schedule_id':id}
                return render(request,"turf/schedule.html",context)
@method_decorator(login_required,name='dispatch')
class TurfScheduleDelete(View):
    def get (self, request, *args, **kwargs):
        id = kwargs.pop('id')
        schedule = TurfScheduleModel.objects.filter(id=id).first()
        schedule.delete()
        return redirect('turf_schedule')


@method_decorator(login_required,name='dispatch')
class ManageUser(View):
    def get (self, request, *args, **kwargs):
        return render(request,'admin/manage_user.html',{})


@method_decorator(login_required,name='dispatch')
class ManageTurf(View):
    def get (self, request, *args, **kwargs):
        return render(request,'admin/manage_turf.html',{})