from django.urls import URLPattern, path
from django.conf.urls import url
<<<<<<< HEAD
from .views import HomeView,Shop,AllMatchesView,MyMatchesView,CreateMatches,TurfsView
=======
from .views import HomeView,AllMatchesView,MyMatchesView,CreateMatchesView,TurfsView
>>>>>>> 1d48d9d1bbe3fda2651df667d4a6cbf8dcf51744


urlpatterns = [
    # path('login/', Signin.as_view(), name="sign-in"),
    path('turfs/', TurfsView.as_view(), name="turfs"),
    path('matches/', AllMatchesView.as_view(), name="matches"),
    path('my-matches/', MyMatchesView.as_view(), name="my-matches"),
    path('create-matches/', CreateMatches.as_view(), name="create-matches"),
    path('home/', HomeView.as_view(), name="home"),
  
]