from django.urls import URLPattern, path
from django.conf.urls import url
from .views import Test, Signin , Turfs



urlpatterns = [
    path('', Test.as_view(), name="base"),
    path('login/', Signin.as_view(), name="sign-in"),
    

    path('turfs/', Turfs.as_view(), name="turfs"),
]