from django.urls import URLPattern, path
from django.conf.urls import url
from .views import Test, Signin , Shop, Turfs


urlpatterns = [
    path('home/', Test.as_view(), name="home"),
    path('login/', Signin.as_view(), name="sign-in"),
    path('shop/', Shop.as_view(), name="shop"),
    path('turfs/', Turfs.as_view(), name="turfs"),
]