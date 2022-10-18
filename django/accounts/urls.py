from django.shortcuts import render
from django.urls import path
from django.conf.urls import url
from .views import LoginPage ,Signup
from django.contrib.auth import views as auth_views

# Create your views here.


urlpatterns = [
    path('register/', Signup.as_view(), name="register"),
    path('', LoginPage.as_view(redirect_authenticated_user=True), name="login"),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),

]