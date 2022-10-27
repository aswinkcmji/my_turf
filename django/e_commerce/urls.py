from django.urls import URLPattern, path
from .views import  Checkout, DeleteStock, E_commercePage
from dashboard.views import AddStockView

urlpatterns = [
    path('', E_commercePage.as_view(), name="shop"),
    path('deletestock/<int:id>/',DeleteStock.as_view(),name='deletestock'),
    path('checkout/', Checkout.as_view(), name="checkout"),
]