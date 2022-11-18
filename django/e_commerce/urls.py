from django.urls import URLPattern, path
from .views import  *
from dashboard.views import AddStockView

urlpatterns = [
    path('', E_commercePage.as_view(), name="shop"),
    path('deletecart/<int:id>/',DeleteCartItem.as_view(),name='deletecart'),
    path('checkout/', Checkout.as_view(), name="checkout"),
    path('order/<int:id>/', OrderView.as_view(), name="order"),
    path('outofstock/', OutOfStock.as_view(), name="outOfStock"),
    path('stockdetails/', StockTable.as_view(), name="stocktable"),
    path('deletestock/<int:id>/',DeleteStock.as_view(),name='deletestock'),
    path('cart/',CartDetailsView.as_view(),name='cartdetails'),
    path('puchasehistory/',PurchaseHistoryView.as_view(),name='puchasehistory'),
    path('updateorderstatus/<int:id>/',UpdateOrderStatusView.as_view(),name='updateorderstatus'),
    path('orderdetails/<int:id>/',OrderDetailsView.as_view(),name='orderdetails'),



]

htmx_urlpatterns = [

    path('filterhl/',HtoL_Filter.as_view(),name='htol_filter'),
    path('filterlh/',LtoH_Filter.as_view(),name='ltoh_filter'),
    path('filteraz/',AtoZ_Filter.as_view(),name='atoz_filter'),
    path('filterlt/',Latest_Filter.as_view(),name='latest_filter'),
    path('searchProduct/',SearchProduct.as_view(),name='searchProduct'),

]

urlpatterns += htmx_urlpatterns