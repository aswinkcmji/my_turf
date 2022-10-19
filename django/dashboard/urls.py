from django.urls import URLPattern, path
from .views import AddStockView
from .views import Turf_Dashboard

urlpatterns = [
    path('addstock/', AddStockView.as_view(), name="addstock"),
    # path('liststock/', ListStock.as_view(), name="liststock")
    path('', Turf_Dashboard.as_view(), name="turf_dash"),
]