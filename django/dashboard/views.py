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
from e_commerce.models import ProductsModel,CheckoutModel
from django.conf import settings  
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import GalleryImgForm, TurfScheduleForm, CategoriesForm, CategoriesEditForm, TurfPasswordChangeForm
from django.utils.dateparse import parse_datetime
from .models import TurfGallery, TurfScheduleModel , CategoriesModel
from User.models import MatchModel,TournamentModel
from django.db.models import Sum
from accounts.forms import TurfEditForm
from django.contrib.auth import update_session_auth_hash





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
                if int(request.POST.get('quantity')) > 1 :
                    form.save()  
                    messages.success(request,"Stock was successfully added...")
                    return redirect(reverse('addstock')) 
                else:
                    messages.error(request,"Quantity must be greater than 1 !")

            else:  
                
                form = addStockForm()  
        
            return render(request, 'e_commerce/addProduct.html',{'form':form})
class Turf_Dashboard(View):
    def get(self,request):

        
        turfDetails = UserModel.objects.filter(username = request.user.username  ).values()
        header = TurfGallery.objects.filter( username = request.user.username ,isheader = True)
        count = TurfGallery.objects.filter(isheader = True).count()
        category = UserModel.objects.filter(username = request.user.username  ).values_list('category')
        editForm = UserModel.objects.filter(username = request.user.username, is_turf = True).count()
        categories= CategoriesModel.objects.all()
        passform=TurfPasswordChangeForm(request.user)

        print('========count ==',editForm)
        print('@@@@@@catergory@@@@@@@',category)
        print('category',category.__dict__)
        a=None
        for i in category:
            for j in i:
                a=j
        image = CategoriesModel.objects.filter(id__in = a )

     
        
        context = {
            'form': GalleryImgForm(),
            'turfDetails': turfDetails,
            'media_url':settings.MEDIA_URL,
            'header' : header,
            'count' :   count,
            'image': image,
            'editForm' : TurfEditForm(),
            'categories':categories,
            'passform':passform,
           

        }
        print("========form4======")
        


        return render(request,'turf/turf_dashboard.html',context)
    def post(self,request,*args,**kwargs):

        if request.method == 'POST':
                form = GalleryImgForm(request.POST,request.FILES)
                # count = TurfGallery.objects.filter( username = request.user.username).values_list('isheader')
                
                # print("=============count===========",count)

                print("====form11111111111===",form)
                if form.is_valid():
                    form.save(request)
                    
                    messages.success(self.request, "Images added Successfully")
                    return HttpResponseRedirect(reverse('turf_dash')) 
                else:  
                    messages.error(self.request, "Images failed")
                    
                    return HttpResponseRedirect(reverse('turf_dash')) 



@method_decorator(login_required,name='dispatch')
class TurfSchedule(View):
    def get(self,request):
        if request.user.is_turf:
            turf_schedule   = TurfScheduleModel.objects.filter(turf=request.user)

            addScheduleform = TurfScheduleForm(initial={'turf':request.user})
            context ={'addScheduleform': addScheduleform ,'is_addform':False , 'turf_schedule':turf_schedule}
            return render(request,"turf/schedule.html",context)
        else:
            return redirect('403')
    def post(self, request, *args, **kwargs):
        if request.user.is_tur:
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
        else:
            return redirect('404')

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
        categories = CategoriesModel.objects.all()
        categories_dict={}
        for category in categories:
            categories_dict[str(category.id)]=category.category
        context = {'turfs':turfs,
                'media_url':settings.MEDIA_URL,
                'categories_dict':categories_dict}
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


        turfGallery = TurfGallery.objects.filter(username = request.user.username, isheader=False).values()
        
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
        editCategoryForm = CategoriesEditForm(initial={'category':category.category , 'image':category.image})
        context={'addCategoryform':editCategoryForm,
                 'is_editform':True,
                 'category_id':id,
                 'media_url':settings.MEDIA_URL,
                 "image":category.image}
        return render(request,"admin/manage_categories.html",context)
    def post(self, request, *args, **kwargs):
        id = kwargs.pop('id')

        if request.method == 'POST':
            form = CategoriesEditForm(request.POST, request.FILES)
            
            category = CategoriesModel.objects.filter(id=id).first()
            if form.is_valid():
                

                category_in_db = CategoriesModel.objects.filter(category=request.POST['category']).first()
                if  category_in_db :
                    if request.POST['category'] != category.category:
                        messages.error(request,"Category allready exists")
                        categories   = CategoriesModel.objects.all()
                        context =  {'addCategoryform': form, 'is_addform':True ,
                            'categories':categories,
                            'is_editform':True,
                            'category_id':id,
                            'media_url':settings.MEDIA_URL,
                            "image":category.image}
                        return render(request,"admin/manage_categories.html",context)

                else:
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
                            'category_id':id,
                            'media_url':settings.MEDIA_URL,
                            "image":category.image}
                return render(request,"admin/manage_categories.html",context)

@method_decorator(login_required,name='dispatch')
class CategoriesDeleteView(View):
    def get (self, request, *args, **kwargs):
        id = kwargs.pop('id')
        category = CategoriesModel.objects.filter(id=id).first()
        category.delete()
        return redirect('categories')




@method_decorator(login_required,name='dispatch')
class AdminDashboardView(View):
    def get (self, request, *args, **kwargs):
        if request.user.is_superuser:
            total_users=UserModel.objects.all().exclude(is_turf=1).count()
            total_turfs=UserModel.objects.filter(is_turf=1).count()
            total_matches=MatchModel.objects.all().count()
            total_tournaments=TournamentModel.objects.all().count()
            totalprice=CheckoutModel.objects.all().values_list('quantity','price')
            # print(totalprice)
            totalAmount = 0
            for i in totalprice:
                totalAmount =totalAmount+(i[0]*i[1])
            total_price=totalAmount
            total_products=ProductsModel.objects.all().count()
            total_orders_placed=CheckoutModel.objects.all().count()
            total_completed_matches=MatchModel.objects.filter(status="Completed").count()
            total_cancelled_matches=MatchModel.objects.filter(status="Cancelled").count()
            total_completed_tournaments=TournamentModel.objects.filter(status="Completed").count()
            total_cancelled_tournaments=TournamentModel.objects.filter(status="Cancelled").count()
            categories_list=CategoriesModel.objects.all()
            categories_count=CategoriesModel.objects.all().count()
            categories_in_matches=[]
            categories_in_tournaments=[]
            print(type(categories_count))
            for i in range(int(categories_count)):
                 categories_in_matches.append(MatchModel.objects.filter(category=categories_list[i]).count())
                 print(categories_list[i]   )
            for i in range(int(categories_count)):
                 categories_in_tournaments.append(TournamentModel.objects.filter(category=categories_list[i]).count())
                 print(categories_list[i])
            print(categories_in_matches)
            distinct_dates=CheckoutModel.objects.all().values_list('date',flat=True).distinct().exclude(date=None).order_by('date')
            print(distinct_dates)
            date_list=[]
            price_list=[]
            print(distinct_dates,distinct_dates[0],int(distinct_dates.count()))
            for i in range(int(distinct_dates.count())):
                totalAmount = 0
                print(i)
                date_list.append(distinct_dates[i].strftime("%d/%m/%Y"))
                totalprice=CheckoutModel.objects.filter(date=distinct_dates[i]).values_list('quantity','price')
                print(totalprice)
                for i in totalprice:
                     totalAmount =totalAmount+(i[0]*i[1])
                price_list.append(totalAmount)
            print(date_list)
            print(price_list)
            now = datetime.now()

            timestamp = datetime.timestamp(now)
            print("timestamp =", timestamp)
            context={
                'total_users':total_users,
                'total_turfs':total_turfs,
                'total_matches':total_matches,
                'total_price':total_price,
                'total_products':total_products,
                'total_orders_placed':total_orders_placed,
                'total_completed_matches':total_completed_matches,
                'total_cancelled_matches':total_cancelled_matches,
                'categories_list':categories_list,
                'categories_in_matches':categories_in_matches,
                'date_list':date_list,
                'price_list':price_list,
                'total_tournaments':total_tournaments,
                'total_completed_tournaments':total_completed_tournaments,
                'total_cancelled_tournaments':total_cancelled_tournaments,
                'categories_in_tournaments':categories_in_tournaments
            }
            return render(request,"admin/dashboard.html",context)
        else:
            return render(request,"errors/error403.html",{})



class DeleteGalleryImage(View):
    def get(self, request,id, *args,**kwargs):
        item = TurfGallery.objects.get(id=id)
        item.delete()
        messages.success(request, 'Image Deleted')

        return HttpResponseRedirect(reverse('turf_gallery'))

class GalleryUpdate(View):
 

    def post(self, request, *args, **kwargs):

        if request.method == 'POST':  
            form = GalleryImgForm(request.POST, request.FILES)
            if form.is_valid(): 
                if request.FILES :
                    updatedRecord = TurfGallery.objects.get(id=request.POST['image_id'])

                    updatedRecord.image = request.FILES['image']

                    updatedRecord.caption = request.POST['caption']

                    updatedRecord.save()

                    messages.success(request, 'Image updated Successfully')
                    
                    return HttpResponseRedirect(reverse('turf_gallery')) 
                else:
                    updatedRecord = TurfGallery.objects.get(id=request.POST['image_id'])

                    updatedRecord.caption = request.POST['caption']

                    updatedRecord.save()

                    messages.success(request, 'Image updated Successfully')
                    
                    return HttpResponseRedirect(reverse('turf_gallery'))

            else:  
                print(form.errors)

                messages.error(request, 'failed')
                
                
            return HttpResponseRedirect(reverse('turf_gallery'))
        

class DashboardImageUpdate(View):
    def post(self, request, *args, **kwargs):

        if request.method == 'POST':  
            form = GalleryImgForm(request.POST, request.FILES)
            if form.is_valid(): 

                print("request.POST",request.POST)
                # print("request.POST['image_id']",request.POST['image_id'])
                if request.FILES :

                    updatedRecord = TurfGallery.objects.get(isheader=True)
                    print(updatedRecord)

                    updatedRecord.image = request.FILES['image']

                    updatedRecord.save()

                    messages.success(request, 'Image Updated Successfully')
                    
                    return HttpResponseRedirect(reverse('turf_dash'))  
                  

            else:  
                messages.error(request, 'failed')
                return HttpResponseRedirect(reverse('turf_dash'))

class dashDataUpdate(View):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':  
            editForm = TurfEditForm(request.POST, request.FILES)
            # print ("========editForm=====",editForm)
            # print("RRRRRRRRRRRRRRRRRRR",request.POST['category'])
            if editForm.is_valid(): 

                if request.FILES :

                    updatedRecord = UserModel.objects.get(id=request.POST['details_id'])

                    updatedRecord.avatar = request.FILES['avatar']
                    
                    updatedRecord.username = request.POST['username']

                    updatedRecord.turf_name = request.POST['turf_name']

                    updatedRecord.email = request.POST['email']
                    
                    updatedRecord.phone = request.POST['phone']

                    updatedRecord.location = request.POST['location']

                    updatedRecord.landmark = request.POST['landmark']

                    # updatedRecord.category = request.POST['category']

                    updatedRecord.save()

                    messages.success(request, 'Details Updated Successfully')
                    
                    return HttpResponseRedirect(reverse('turf_dash'))  
                
                else :

                    updatedRecord = UserModel.objects.get(id=request.POST['details_id'])
                    

                    updatedRecord.turf_name = request.POST['turf_name']
                    
                    updatedRecord.username = request.POST['username']

                    updatedRecord.email = request.POST['email']
                    
                    updatedRecord.phone = request.POST['phone']

                    updatedRecord.location = request.POST['location']

                    updatedRecord.landmark = request.POST['landmark']

                    # updatedRecord.category = request.POST['category']

                    updatedRecord.save()

                    messages.success(request,"Saved successfully")
                    return HttpResponseRedirect(reverse('turf_dash'))  

            else:  
                print("-----------------------1111---------------------",editForm.errors)
                messages.error(request,"Updation failed")
                return HttpResponseRedirect(reverse('turf_dash'))
            
        


class DeleteTurfHead(View):
    def get(self, request, *args,**kwargs):
        item = TurfGallery.objects.get(isheader=True)
        item.delete()
        messages.success(request, 'Image Deleted')

        return HttpResponseRedirect(reverse('turf_dash'))




class TurfPasswordChange(View):
    def post(self, request, *args, **kwargs):
            if request.method == 'POST':
                if 'change_pass' in request.POST:
                    passform=TurfPasswordChangeForm(request.user,request.POST)   
                    print(passform)
                    if passform.is_valid():
                        print("########################  form is valid ############")
                        user = passform.save()

                        update_session_auth_hash(request, user) # Important!

                        messages.success(request, 'Your password was successfully updated!')

                        return HttpResponseRedirect(reverse('turf_dash')) 
                    else:
                        
                        messages.error(request, 'Same as Old Password.. Choose New One')
                        return HttpResponseRedirect(reverse('turf_dash')) 




class TurfCategoryUpdate(View):
    def post(self, request, *args, **kwargs):
            if request.method == 'POST':
                form = TurfEditForm(request.POST,request.FILES)
                if form.is_valid():
                    print(request.POST.get('category'),"wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww")
                    if request.POST.get('category') == "" or request.POST.get('category') == "[]":

                        user_obj=form.save(commit=False)
                        user_obj.save()
                    
                    messages.success(self.request, "Updated Successfully")
                    return HttpResponseRedirect(reverse('turf_dash'))
                else:
                    messages.error(request, 'Updation Failed!!')
                    return HttpResponseRedirect(reverse('turf_dash'))




class DeleteTurfCategory(View):
    def get(self, request,id, *args,**kwargs):
        item = CategoriesModel.objects.get(id=id)
        item.delete()
        messages.success(request, 'Category Removed')
        return HttpResponseRedirect(reverse('turf_dash'))