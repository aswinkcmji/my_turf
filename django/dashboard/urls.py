from django.urls import URLPattern, path
from .views import Turf_Dashboard

urlpatterns = [
    path('', Turf_Dashboard.as_view(), name="turf_dash"),
]