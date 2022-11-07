from django.urls import URLPattern, path
from django.conf.urls import url
from .views import *

urlpatterns = [
    # path('login/', Signin.as_view(), name="sign-in"),
    path('turfs/', TurfsView.as_view(), name="turfs"),
    path('matches/', AllMatchesView.as_view(), name="matches"),
    path('my-matches/', MyMatchesView.as_view(), name="my-matches"),
    path('create-matches/', CreateMatchesView.as_view(), name="create-matches"),
    path("requested-matches/cancel/<int:id>",CancelRequestView.as_view(), name="join"),
    path('requested-matches/', RequestedMatchesView.as_view(), name="requested-matches"),
    path('matches-history/', MatchHistoryView.as_view(), name="match-history"),
    path('', HomeView.as_view(), name="home"),
    path('matches/join/<int:id>',JoinMatchView.as_view(),name="join"),
    path("my-matches/edit/<int:id>",EditMatchesView.as_view(),name="edit"),
    path('requests/',RequestsView.as_view(), name="requests"),
    path('matches/join/<int:id>',JoinMatchView.as_view(),name="join"),
    path("matches-history/cancel/<int:id>",CancelMatchView.as_view(),name="cancelmatch"),
    path("my-matches/cancel/<int:id>",CancelMatchView.as_view(),name="cancelmatch"),
    path('create-tournament/', CreateTournamentView.as_view(), name="create-tournament"),
    path('all-tournaments/', AllTournamentView.as_view(), name="all-tournaments"),
    path('my-tournaments/', MyTournamentView.as_view(), name="my-tournaments"),
    path("my-tournaments/edit/<int:id>",EditTournamentView.as_view(),name="edit"),
    path('requested-tournaments/',RequestedTournamentView.as_view(), name="requested-tournaments"),
    path('all-tournaments/tournament-join/<int:id>',JoinTournamentView.as_view(),name="tournament-join"),





]

