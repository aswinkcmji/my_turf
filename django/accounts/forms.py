from this import d
from tkinter import HIDDEN
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import HiddenInput
from .models import UserModel

class SignUpForm(UserCreationForm):
    
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Username"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'First Name'}), help_text='First name')
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Last Name'}), help_text='Last name')
    
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':"Email"}))
    phone = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Phone Number" , 'type':"tel" }))
    location = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Location"}))
    age = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':"Age" , 'min':"1"}))
    CHOICES=[('Male','Male'),
         ('Female','Female'),
         ('Other','Other'),]
    gender = forms.ChoiceField(required=True,choices=CHOICES, widget=forms.Select(attrs={'class': 'form-select','defualt':"Gender"}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'}))

    class Meta:
        model = UserModel
        fields = ('username','first_name', 'last_name', 'email', 'phone','location','age','gender','password1', 'password2')

    def clean_phone(self, *args, **kwargs):
        phone = self.cleaned_data.get("phone")
        if not len(str(phone)) <= 15 or not len(str(phone)) >= 7 or not phone >0:
            raise forms.ValidationError("Enter a valid phone number")
        return phone
    def clean_age(self, *args, **kwargs):
        age = self.cleaned_data.get("age")
        if not age >= 5 or not age <= 200:
            raise forms.ValidationError("Not a valid age")
        return age

class LoginForm(forms.Form):
 
    username = forms.CharField(max_length = 30 , widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Username"}))
    password = forms.CharField(max_length=15, widget = forms.PasswordInput(attrs={'class': 'form-control','placeholder':"Password"}))


class SignUpTurfForm(UserCreationForm):
    
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Username"}))
    turf_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Turf Name"}))
    
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':"Email"}))
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Phone Number" , 'type':"tel" }))
    location = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Location"}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'}))
    category = forms.CharField( required=True, widget=forms.HiddenInput(attrs={'id':"category-input",'raedonly':"true"}))

    is_turf=forms.BooleanField(widget=forms.CheckboxInput(attrs={'checked':"true" ,'hidden':"true" , 'readonly':"true"}))
    avatar=forms.ImageField(required=True,widget=forms.FileInput(attrs={'class':"form-control" }))
    landmark = forms.CharField( max_length=255, required=True,widget=forms.TextInput(attrs={'class':"form-control", 'placeholder':"Landmark"}))
    class Meta:
        model = UserModel
        fields = ('username','turf_name' ,'email', 'phone','location','password1', 'password2','is_turf','avatar','landmark','category')

