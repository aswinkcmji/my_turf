from django import forms

from .models import creatematchModel


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
    date = forms.DateField()
    time = forms.TimeField()
    nos = forms.IntegerField()                                                               #nos = number of slots
    class Meta:
        model = creatematchModel
        fields = ('category', 'location', 'date', 'time', 'nos')

