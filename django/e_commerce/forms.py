from django import forms
from .models import ProductsModel


class addStockForm( forms.ModelForm ):

  product_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
  price = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control','min':'1'}))
  quantity = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control','min':'1'}))
  class Meta:
    model = ProductsModel
    fields = '__all__'