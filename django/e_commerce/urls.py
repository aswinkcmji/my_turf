from django.urls import URLPattern, path
from .views import  Checkout,DeleteCartItem, DeleteStock, E_commercePage, OrderView, OutOfStock, StockTable
from dashboard.views import AddStockView

urlpatterns = [
    path('', E_commercePage.as_view(), name="shop"),
    path('deletecart/<int:id>/',DeleteCartItem.as_view(),name='deletecart'),
    path('checkout/', Checkout.as_view(), name="checkout"),
    path('order/<int:id>/', OrderView.as_view(), name="order"),
    path('outofstock/', OutOfStock.as_view(), name="outOfStock"),
    path('stockdetails/', StockTable.as_view(), name="stocktable"),
    path('deletestock/<int:id>/',DeleteStock.as_view(),name='deletestock'),
     path('deletestock/<int:id>/',DeleteStock.as_view(),name='deletestock'),
]