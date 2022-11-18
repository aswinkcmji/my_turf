from django.shortcuts import render
from django.urls import path
from django.conf.urls import url
from .views import *
from django.contrib.auth import views as auth_views

# Create your views here.


urlpatterns = [
    path('register/', Signup.as_view(), name="register"),
    path('register_turf/', SignupTurf.as_view(), name="register_turf"),
    path('login/', LoginPage.as_view(redirect_authenticated_user=True), name="login"),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/',User_ProfileView.as_view(),name='user-profile'),
    path('error404/',Error404View.as_view(),name='404'),
    path('error403/',Error403View.as_view(),name='403'),
]