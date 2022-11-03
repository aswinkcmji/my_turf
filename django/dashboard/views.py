from contextvars import Context
from datetime import datetime
import json
from unicodedata import category
from django.contrib import messages
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
from .forms import GalleryImgForm, TurfScheduleForm, CategoriesForm
from django.utils.dateparse import parse_datetime
from .models import GalleryImg, TurfScheduleModel , CategoriesModel




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
                print(request.FILES) 
                form.save()  
                
                return redirect(reverse('addstock'))  
            else:  
                
                form = addStockForm()  
        
            return render(request, 'e_commerce/addProduct.html',{'form':form})
class Turf_Dashboard(View):
    def get(self,request):


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
                category = CategoriesModel.objects.get(id=request.POST['category'])
                form2 =form.save(commit=False)
                for key,value in enumerate(bg_colors):
                    
                    if request.POST["color"] == str(key):
                        form2.color_txt =txt_colors[key]
                        form2.color_bg =bg_colors[key]
                # form2.start= parse_datetime(request.POST['start'])
                # form2.end= parse_datetime(request.POST['end'])
                form2.title = category.category +" - "+request.POST['user']
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
        title = ""
        editTurfForm = TurfScheduleForm()
        if schedule:
            title = schedule.title.split(' - ')
            editTurfForm = TurfScheduleForm(initial={'category':schedule.category,'user':title[1] ,'start':schedule.start, 'end':schedule.end, 'turf':schedule.turf})
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
        users = UserModel.objects.filter(is_turf=False, is_superuser=False)
        context = {'users':users,
                'media_url':settings.MEDIA_URL}
        return render(request,'admin/manage_user.html',context)
    def post (self, request, *args, **kwargs):
        selected=request.POST.getlist('checkbox_user_table')
        if selected != []: 
            if 'Unblock' in request.POST:
                users = UserModel.objects.filter(is_turf=False,id__in=selected)
                for user in users:
                    if not user.is_active:
                        user.is_active = True
                        user.save()
                messages.success(request,'Unblocked')
                return HttpResponseRedirect(reverse('manage_user'))
            elif 'Block' in request.POST:
                users = UserModel.objects.filter(is_turf=False,id__in=selected)
                for user in users:
                    # print(user,"userrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
                    if  user.is_active:
                        user.is_active = False
                        user.save()
                messages.success(request,'Blocked')
                return HttpResponseRedirect(reverse('manage_user'))
            messages.error(request,'Something went wrong')
            return HttpResponseRedirect(reverse('manage_user'))
            
        else:
            messages.error(request	,'NO Turf selected')
            return HttpResponseRedirect(reverse('manage_user'))


@method_decorator(login_required,name='dispatch')
class ManageTurf(View):
    def get (self, request, *args, **kwargs):
        turfs = UserModel.objects.filter(is_turf=True)
        context = {'turfs':turfs,
                'media_url':settings.MEDIA_URL}
        return render(request,'admin/manage_turf.html',context)
    def post (self, request, *args, **kwargs):
        selected=request.POST.getlist('checkbox_turf_table')
        if selected != []: 
            if 'Unblock' in request.POST:
                turfs = UserModel.objects.filter(is_turf=True,id__in=selected)
                for turf in turfs:
                    if not turf.is_active:
                        turf.is_active = True
                        turf.save()
                messages.success(request,'Unblocked')
                return HttpResponseRedirect(reverse('manage_turf'))
            elif 'Block' in request.POST:
                turfs = UserModel.objects.filter(is_turf=True,id__in=selected)
                for turf in turfs:
                    if  turf.is_active:
                        turf.is_active = False
                        turf.save()
                messages.success(request,'Blocked')
                return HttpResponseRedirect(reverse('manage_turf'))
            messages.error(request,'Something went wrong')
            return HttpResponseRedirect(reverse('manage_turf'))
            
        else:
            messages.error(request	,'NO Turf selected')
            return HttpResponseRedirect(reverse('manage_turf'))
        # return render(request,'admin/manage_turf.html',{})
class Turf_Gallery(View):
    def get(self,request):


        turfGallery = GalleryImg.objects.filter(username = request.user.username).values()
        print(" ",turfGallery)
        context = {
            'form': GalleryImgForm(),
            'turfGallery': turfGallery,
            'media_url':settings.MEDIA_URL,

        }
        print(" ",context)


        return render(request,'turf/turf_gallery.html',context)         
            # else:
    def post(self,request,*args,**kwargs):

        if request.method == 'POST':
                form = GalleryImgForm(request.POST,request.FILES)
                print("====form===",form)
                if form.is_valid():
                    form.save()
                
                    messages.success(self.request, "Images added Successfully")
                    return HttpResponseRedirect(reverse('turf_gallery')) 
                else:  
                    messages.error(self.request, "Images failed")
                    
                    return HttpResponseRedirect(reverse('turf_gallery'))           
            #     context['form'] = form
            #     return render(request, 'accounts/turf-sign-up.html',context)

@method_decorator(login_required,name='dispatch')
class CategoriesView(View):
    def get(self, request, *args, **kwargs):
        categories   = CategoriesModel.objects.all()

        addCategoryform = CategoriesForm()
        context ={'addCategoryform': addCategoryform ,'is_addform':False , 'media_url':settings.MEDIA_URL,'categories':categories}
        return render(request,"admin/manage_categories.html",context)
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = CategoriesForm(request.POST, request.FILES)
             
            if form.is_valid():
                form.save()
                    
                    
                messages.success(self.request, "Category Added successfully")
                return HttpResponseRedirect(reverse('categories'))
                      
            else:
                categories   = CategoriesModel.objects.all()
                context ={'addCategoryform': form, 'is_addform':True ,'media_url':settings.MEDIA_URL,'categories':categories}
                return render(request,"admin/manage_categories.html",context)
        

@method_decorator(login_required,name='dispatch')
class CategoriesEditView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.pop('id')
        category = CategoriesModel.objects.filter(id=id).first()
        editCategoryForm = CategoriesForm(initial={'category':category.category , 'image':category.image})
        context={'addCategoryform':editCategoryForm,
                 'is_editform':True,
                 'category_id':id,
                 'media_url':settings.MEDIA_URL,
                 "image":category.image}
        return render(request,"admin/manage_categories.html",context)
    def post(self, request, *args, **kwargs):
        id = kwargs.pop('id')

        if request.method == 'POST':
            form = CategoriesForm(request.POST, request.FILES)
            
            category = CategoriesModel.objects.filter(id=id).first()
            if form.is_valid():
                
               
                category.category = request.POST['category']

                if request.FILES:
                    if request.FILES['image']:
                        category.image = request.FILES['image']
                
                category.save()
                    
                    # messages.success(self.request, "Account Created Successfully")
                return HttpResponseRedirect(reverse('categories'))
            else:
                categories   = CategoriesModel.objects.all()
                context =  {'addCategoryform': form, 'is_addform':True ,
                            'categories':categories,
                            'is_editform':True,
                            'category_id':id}
                return render(request,"admin/manage_categories.html",context)

@method_decorator(login_required,name='dispatch')
class CategoriesDeleteView(View):
    def get (self, request, *args, **kwargs):
        id = kwargs.pop('id')
        category = CategoriesModel.objects.filter(id=id).first()
        category.delete()
        return redirect('categories')