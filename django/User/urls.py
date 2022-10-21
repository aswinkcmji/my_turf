from django.urls import URLPattern, path
from django.conf.urls import url
from .views import HomeView,AllMatchesView,MyMatchesView,CreateMatchesView,TurfsView,CancelRequestView,RequestedMatchesView,MatchHistoryView  



urlpatterns = [
    # path('login/', Signin.as_view(), name="sign-in"),
    # path('shop/', Shop.as_view(), name="shop"),
    path('turfs/', TurfsView.as_view(), name="turfs"),
    path('matches/', AllMatchesView.as_view(), name="matches"),
    path('my-matches/', MyMatchesView.as_view(), name="my-matches"),
    path('create-matches/', CreateMatchesView.as_view(), name="create-matches"),
    path("requested-matches/cancel/<int:id>",CancelRequestView.as_view(), name="join"),
    path('requested-matches/', RequestedMatchesView.as_view(), name="requested-matches"),
     path('matches-history/', MatchHistoryView.as_view(), name="match-history"),
    path('home/', HomeView.as_view(), name="home"),
  
]