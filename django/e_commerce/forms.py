from django import forms
from .models import CartModel, ProductsModel ,BillingAddressModel


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


class billingAddressForm(forms.ModelForm):

  state_choices = [("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry")]

  username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
  firstname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
  contactnumber = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control','max': 9999999999,'min':1000000000}))
  houseno = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
  landmark = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
  location = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
  state = forms.ChoiceField(choices=state_choices,widget=forms.Select(attrs={'class': 'form-control'}))
  pincode = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control','max': 999999,'min':99999 }))

  class Meta:
    model = BillingAddressModel
    fields = '__all__'
