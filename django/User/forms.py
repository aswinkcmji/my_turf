from time import time
from django import forms
from django.forms import ModelForm

from .models import RequestModel,creatematchModel

class RequestForm(ModelForm):
    category = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly':'true'}))
    date = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly':'true'}))
    time = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly':'true'}))
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


class creatematchForm(forms.Form):

    options =[
        ("1", "Cricket"),
        ("2", "Football"),
        ("3", "Baseball"),
        ("4", "Badminton"),
        ("5", "Tennis"),
    ]


    category= forms.ChoiceField(choices=options)
    location= forms.CharField(max_length=1000)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    nos = forms.IntegerField()                                                               #nos = number of slots
    class Meta:
        model = creatematchModel
        fields = ('category', 'location', 'date', 'time', 'nos')

