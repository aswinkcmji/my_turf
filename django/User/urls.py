from django.urls import URLPattern, path
from django.conf.urls import url
from .views import *



urlpatterns = [
    # path('login/', Signin.as_view(), name="sign-in"),
    # path('turfs/', TurfsView.as_view(), name="turfs"),
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
    path("team/<int:id>",TeamView.as_view(),name="myteam"),
    path("tournament_team/<int:id>",TournamentTeamView.as_view(),name="teams"),
    path('create-tournament/', CreateTournamentView.as_view(), name="create-tournament"),
    path('all-tournaments/', AllTournamentView.as_view(), name="all-tournaments"),
    path('my-tournaments/', MyTournamentView.as_view(), name="my-tournaments"),
    path('requested-tournaments/',RequestedTournamentView.as_view(), name="requested-tournaments"),
    path("my-tournaments/edit/<int:id>",EditTournamentView.as_view(),name="edit"),
    path('tournament-requests/',TournamentRequestsView.as_view(), name="tournament-requests"),
    path('all-tournaments/a/<int:id>',JoinTournamentView.as_view(),name="a"),
    path('tournament-history/', TournamentHistoryView.as_view(), name="tournament-history"),
    path("requested-tournaments/cancel/<int:id>",CancelTournamentsRequestView.as_view(), name="a"),
    path("my-tournaments/cancel/<int:id>",CancelTournamentView.as_view(),name="canceltournament"),
    path("tournament-history/cancel/<int:id>",CancelTournamentView.as_view(),name="canceltournament"),
    path('createteam/',Createteamview.as_view(),name="create-team"),





    
    path('turfs_list/',TurfsListView.as_view(), name="turfs_list") , 
    path('turf_profile/<str:username>',TurfProfileView.as_view(), name="turf_profile"),


    # path('updatecurrentloc/<str:location',UpdateCurrentLocView.as_view(),name="update_current_location"),
    path('contact_us/',Contact_usView.as_view(),name="contact_us"), 
    path('messages-contactUs/',messagesView.as_view(),name="messages_conatct_us"), 
    path('messageView/<str:id>',messageViewView.as_view(),name="messages_view"), 
] 
 

htmx_urlpatterns = [
    path('like_turfComment/<int:id>',LikeTurfCommentView.as_view(), name="like_turfComment") , 
    path("add-TurfComment/<str:username>", AddTurfCommentView.as_view() ,name="add-TurfComment"),
    path("search-city/<str:feildname>",SearchCityView.as_view(),name="search-city"),
    path("search-matches/",SearchMatchView.as_view(),name="search-matches"),
    path("search-tournaments/",SearchTournamentView.as_view(),name="search-tournaments"),
    path('search_turf_list/',SearchTurfListView.as_view(), name="search_turf_list") , 

    path('starred_messages/',StarredMessagesView.as_view(),name="starred_messages"), 
    path('all_messages/',AllMessagesView.as_view(),name="all_messages"), 
    path('hidden_messages/',HiddenMessagesView.as_view(),name="hidden_messages"), 
    path('star_messages/<int:id>/<str:type>',StarMessagesView.as_view(),name="star_message"), 
    path('hide_messages/<int:id>',HideMessagesView.as_view(),name="hide_messages"), 
    path('delete_messages/<int:id>/<str:type>',DeleteMessagesView.as_view(),name="delete_messages"), 
    path('star_message_from_page/<int:id>/',StarMessageFromPageView.as_view(),name="star_message_from_page"), 
    path('delete_message_from_page/<int:id>/',DeleteMessageFromPageView.as_view(),name="delete_message_from_page"), 
]


urlpatterns+= htmx_urlpatterns