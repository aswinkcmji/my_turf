from django import forms

from .models import *


# choices=OPTIONS


class createMatchForm(forms.ModelForm):

    options =[
        ("1", "Cricket"),
        ("2", "Football"),
        ("3", "Baseball"),
        ("4", "Badminton"),
        ("5","Tennis"),
    ]


    category= forms.ChoiceField(choices=options)
    location= forms.CharField(max_length=1000)
    date = forms.CharField()
    time = forms.CharField()
    slots = forms.IntegerField()                                                              
    class Meta:
        model = createMatchModel
        fields = ('category', 'location', 'date', 'time', 'slots')

