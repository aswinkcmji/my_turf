from django.urls import URLPattern, path
from django.conf.urls import url
from .views import HomeView,AllMatchesView,MyMatchesView,CreateMatchesView,TurfsView


urlpatterns = [
    # path('login/', Signin.as_view(), name="sign-in"),
    path('turfs/', TurfsView.as_view(), name="turfs"),
    path('matches/', AllMatchesView.as_view(), name="matches"),
    path('my-matches/', MyMatchesView.as_view(), name="my-matches"),
    path('create-matches/', CreateMatchesView.as_view(), name="create-matches"),
    path('home/', HomeView.as_view(), name="home"),
  
]