from time import time
from django import forms
from django.forms import ModelForm
from .models import RequestModel


class RequestForm(ModelForm):
    category = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly':'true'}))
    date = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly':'true'}))
    time = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly':'true'}))
    creator= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly':'true'}))
    locality=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly':'true'}))
    status=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly':'true'}))
    
