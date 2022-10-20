from django.urls import URLPattern, path
from .views import  E_commercePage
from dashboard.views import AddStockView

urlpatterns = [
    path('', E_commercePage.as_view(), name="shop"),
    # path('addstock/', AddStockView.as_view(), name="addstock"),
    # path('liststock/', ListStock.as_view(), name="liststock")
]