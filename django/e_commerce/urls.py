from django.urls import URLPattern, path
from .views import  DeleteStock, E_commercePage
from dashboard.views import AddStockView

urlpatterns = [
    path('', E_commercePage.as_view(), name="shop"),
    path('deletestock/<int:id>/',DeleteStock.as_view(),name='deletestock'),
    # path('addstock/', AddStockView.as_view(), name="addstock"),
]