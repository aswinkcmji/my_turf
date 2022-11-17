from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views import View
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.views import LoginView# from wallet.models import Wallet
from .models import *
from django.conf import settings
from dashboard.models import CategoriesModel



class Signup(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:  
            context ={}
            context['form'] = SignUpForm()
            return render(request, 'accounts/sign-up.html',context)
        else:
            return HttpResponseRedirect(reverse('home'))
        
    def post(self, request, *args, **kwargs):
            if request.method == 'POST':
                form = SignUpForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(self.request, "Account Created Successfully")
                    return HttpResponseRedirect(reverse('login'))
                      
                else:
                    context ={}
                    context['form'] = form
                    return render(request, 'accounts/sign-up.html',context)


class SignupTurf(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            categories= CategoriesModel.objects.all()
            context ={"categories":categories}
            context['form'] = SignUpTurfForm()
            return render(request, 'accounts/turf-sign-up.html',context)
        else:
            return HttpResponseRedirect(reverse('home'))
        
    def post(self, request, *args, **kwargs):
            if request.method == 'POST':
                form = SignUpTurfForm(request.POST,request.FILES)
                if form.is_valid():
                    print(request.POST.get('category'),"wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww")
                    if request.POST.get('category') == "" or request.POST.get('category') == "[]":
                        SignUpTurfForm.category= list
                    form.save()
                    
                    messages.success(self.request, "Account Created Successfully")
                    return HttpResponseRedirect(reverse('login'))
                      
                else:
                    categories= CategoriesModel.objects.all()
                    context ={"categories":categories}
                    context['form'] = form
                    return render(request, 'accounts/turf-sign-up.html',context)



class LoginPage(LoginView):
    
    
    template_name = 'accounts/sign-in.html'
    def get(self, request, *args, **kwargs):
        context ={}
        context['form'] = LoginForm()
        return render(request, self.template_name, context)
        
    def post(self, request, *args, **kwargs):
        username_form=request.POST['username']
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            is_turf = UserModel.objects.get(username=username_form).is_turf
            login(request, user)
            if is_turf:
                return HttpResponseRedirect(reverse('turf_dash'))
            else:
                return HttpResponseRedirect(reverse('home'))
        else: 
            messages.error(request, 'Incorrect username or password')
        return HttpResponseRedirect(reverse('login'))


class User_ProfileView(View):
    template_name = 'accounts/user_profile.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            data={
                "first_name":request.user.first_name,
                "last_name":request.user.last_name,
                "email":request.user.email,
                "phone":request.user.phone,
                "location":request.user.location,
                "age":request.user.age,
                "gender":request.user.gender
            }
            print(data,request.user.id)
            form=UpdateProfileForm(data)
            print(form)
            return render(request,self.template_name,{"form":form})
        else:
           return HttpResponseRedirect(reverse('login')) 
    def post(self, request, *args, **kwargs):
            if request.method == 'POST':
                form=UpdateProfileForm(request.POST)
                if form.is_valid():
                    print("Kiki")
                    user_obj=UserModel.objects.get(id=request.user.id)
                    print(user_obj)
                    user_obj.first_name=form.cleaned_data['first_name'] 
                    user_obj.last_name=form.cleaned_data['last_name'] 
                    user_obj.email=form.cleaned_data['email']
                    user_obj.phone=form.cleaned_data['phone']
                    user_obj.location=form.cleaned_data['location']
                    user_obj.age=form.cleaned_data['age']
                    user_obj.gender=form.cleaned_data['gender']
                    user_obj.save()
                    return HttpResponseRedirect(reverse('user-profile'))
                else:
                    print("###### Form not valid ################")
                    print(form)
                    return render(request,self.template_name,{"form":form})