from time import time
from django import forms
from django.forms import ModelForm

from .models import RequestModel,creatematchModel,MatchModel

class RequestForm(ModelForm):
    category = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly':'true'}))
    date = forms.DateField(widget=forms.DateInput(attrs={'readonly':'true','type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'readonly':'true','type': 'time'}))
    username= forms.CharField(widget=forms.HiddenInput(attrs={'class': 'form-control','readonly':'true'}))
    locality=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly':'true'}))
    status=forms.CharField(widget=forms.HiddenInput())
    # match_id= forms.ModelMultipleChoiceField(queryset=RequestModel.objects.all())
    phoneno=forms.IntegerField(widget=forms.HiddenInput())
    class Meta():
        model = RequestModel
        # exclude = '__all__'
        fields =('category','date','time','username','locality','status','phoneno')
# choices=OPTIONS


class creatematchForm(ModelForm):

    options =[
        ("Cricket", "Cricket"),
        ("Football", "Football"),
        ("Baseball", "Baseball"),
        ("Badminton", "Badminton"),
        ("Tennis", "Tennis"),
        ("Volleyball","Volleyball"),
        ("Basketball","Basketball")
    ]


    category= forms.ChoiceField(choices=options)
    # location= forms.CharField(max_length=1000)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time','step' : '1'}))
    slots = forms.IntegerField()#nos = number of slots           
    creator= forms.CharField(widget=forms.HiddenInput(attrs={'class': 'form-control','readonly':'true'}))
    locality=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',}))
    status=forms.CharField(widget=forms.HiddenInput())
    slot_available=forms.IntegerField(widget=forms.HiddenInput())
    class Meta:
        model = MatchModel
        fields = '__all__'

