from pickle import NONE
from time import time
from django import forms
from django.forms import ModelForm
# from django.contrib.auth import authenticate
from .models import *

class RequestForm(ModelForm):
    category = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly':'true'}))
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','readonly':'true','type': 'date'}))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control','readonly':'true','type': 'time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control','readonly':'true','type': 'time'}))
    username= forms.CharField(widget=forms.HiddenInput(attrs={'class': 'form-control','readonly':'true'}))
    locality=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly':'true'}))
    status=forms.CharField(widget=forms.HiddenInput())
    # match_id= forms.ModelMultipleChoiceField(queryset=RequestModel.objects.all())
    phoneno=forms.IntegerField(widget=forms.HiddenInput())
    class Meta():
        model = RequestModel
        # exclude = '__all__'
        fields =('category','date','start_time','end_time','username','locality','status','phoneno')
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
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time','step' : '1'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time','step' : '1'}))
    slots = forms.IntegerField()#nos = number of slots           
    creator= forms.CharField(widget=forms.HiddenInput())
    locality=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',}))
    status=forms.CharField(widget=forms.HiddenInput())
    slot_available=forms.IntegerField(widget=forms.HiddenInput())
    class Meta:
        model = MatchModel
        fields = '__all__'
    
    def __init__(self,*args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(creatematchForm, self).__init__(*args, **kwargs)

    def clean(self):
        print("hasgfsdyfgsdhjfdg")
        self.cleaned_data = super().clean()
        slots=self.cleaned_data.get('slots')
        creator=self.cleaned_data.get('creator')
        status=self.cleaned_data.get('status')
        start_time=self.cleaned_data.get('start_time')
        end_time=self.cleaned_data.get('end_time')
        print(slots)
        if slots != None and slots >= 2:
            self.cleaned_data['slot_available']=slots-1
        else :
            self._errors['slots']=self.error_class(['No of slots can not be less than 2'])
        # self.cleaned_data['creator']=self.request.user.username
        if creator !=  self.request.user.username:
            self._errors['creator']=self.error_class([''])
        if status != "Upcoming":
            self._errors['status']=self.error_class([''])
        # self.cleaned_data['status']="Upcoming"
        if   start_time != None and end_time !=None :
                if start_time >= end_time:
                    self._errors['start_time']=self.error_class(['Start time can not be more than end time'])
        elif  start_time == None:
                self._errors['start_time']=self.error_class(['Start time must be time type'])
        elif  end_time == None:
                self._errors['end_time']=self.error_class(['End time must be time type'])
        print("khsfdagjfdghsuj",slots,self.cleaned_data['slot_available'])
        return self.cleaned_data



class updatematchform(ModelForm):
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
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time','step' : '1'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time','step' : '1'}))
    slots = forms.IntegerField()#nos = number of slots           
    creator= forms.CharField(widget=forms.HiddenInput())
    locality=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',}))
    status=forms.CharField(widget=forms.HiddenInput())
    slot_available=forms.IntegerField(widget=forms.HiddenInput())
    match_id=forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = MatchModel
        fields = '__all__'
    
    def __init__(self,*args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(updatematchform, self).__init__(*args, **kwargs)

    def clean(self):
        print("hasgfsdyfgsdhjfdg")
        self.cleaned_data = super().clean()
        slots=self.cleaned_data.get('slots')
        creator=self.cleaned_data.get('creator')
        status=self.cleaned_data.get('status')
        start_time=self.cleaned_data.get('start_time')
        end_time=self.cleaned_data.get('end_time')
        print("holaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",type(slots))
        if slots != None and slots >= 2:
            self.cleaned_data['slot_available']=slots-1
        else :
            self._errors['slots']=self.error_class(['No of slots can not be less than 2'])
        # self.cleaned_data['creator']=self.request.user.username
        if creator !=  self.request.user.username:
            self._errors['creator']=self.error_class([''])
        if status != "Upcoming":
            self._errors['status']=self.error_class([''])
        if   start_time != None and end_time !=None :
                if start_time >= end_time:
                    self._errors['start_time']=self.error_class(['Start time can not be more than end time'])
        elif  start_time == None:
                self._errors['start_time']=self.error_class(['Start time must be time type'])
        elif  end_time == None:
                self._errors['end_time']=self.error_class(['End time must be time type'])
        # self.cleaned_data['status']="Upcoming"
        print("khsfdagjfdghsuj",slots,self.cleaned_data['slot_available'])
        return self.cleaned_data

