from django.urls import URLPattern, path
from django.conf.urls import url
from .views import Test, Signin


urlpatterns = [
    path('', Test.as_view(), name="register"),
    path('login/', Signin.as_view(), name="sign-in"),
]