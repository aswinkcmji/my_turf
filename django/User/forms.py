from time import time
from django import forms
from django.forms import ModelForm

from .models import RequestModel

class RequestForm(ModelForm):
    category = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly':'true'}))
    date = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly':'true'}))
    time = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly':'true'}))
    username= forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly':'true'}))
    locality=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly':'true'}))
    status=forms.CharField()
    match_id=forms.IntegerField()
    phoneno=forms.IntegerField()
    class Meta():
        model = RequestModel
        fields = '__all__'