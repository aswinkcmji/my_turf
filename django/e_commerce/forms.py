from django import forms
from .models import CartModel, ProductsModel


class addStockForm( forms.ModelForm ):

  product_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
  price = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control','min':'1'}))
  quantity = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control','min':'1'}))
  class Meta:
    model = ProductsModel
    fields = '__all__'

class addToCartForm(forms.ModelForm):
  product_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
  username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
  image = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
  class Meta:
    model = CartModel
    fields = '__all__'