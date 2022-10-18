from django.urls import URLPattern, path
from .views import E_commercePage

urlpatterns = [
    path('', E_commercePage.as_view(), name="shop"),
]