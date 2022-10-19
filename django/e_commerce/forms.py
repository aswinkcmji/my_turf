from django import forms
from .models import Products


class addStockForm( forms.ModelForm ):

  product_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
  price = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control','min':'1'}))
  quantity = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control','min':'1'}))
#   image_Link = forms.CharField(widget=forms.ImageField(attrs={'class': 'form-control'}))

  class Meta:
    model = Products
    fields = ('product_name','price','quantity','image_Link',)