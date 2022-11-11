from curses import meta
import datetime
from multiprocessing.sharedctypes import Value
from tkinter import E
from turtle import color
from unicodedata import category
from django import forms
from django.utils.dateparse import parse_datetime


from django.forms import ModelForm
from .models import TurfScheduleModel, TurfGallery, CategoriesModel


class TurfScheduleForm(ModelForm):
    # CHOICES_category = [('1', '1'),
    #      ('2', '2'),
    #      ('3', '3'), ]
    category = forms.ModelChoiceField(queryset=CategoriesModel.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    user = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Username/phone/email..."}))
    start = forms.CharField(widget=forms.DateTimeInput(attrs={
                            'class': 'form-control ', 'placeholder': 'Start date', 'type': 'datetime-local'}))
    end = forms.CharField(widget=forms.DateTimeInput(attrs={
                          'class': 'form-control ', 'placeholder': 'End date', 'type': 'datetime-local'}))

    CHOICES_color = [('0', 'red'),
         ('1', 'green'),
         ('2', 'blue'),
         ('3', 'orange'),
         ('4', 'gray'), ]
    color = forms.ChoiceField(choices=CHOICES_color,widget=forms.RadioSelect(
        attrs={'class': 'form-control', 'placeholder': 'colour'}))


    class Meta:
        model = TurfScheduleModel
        fields = ('category', 'user', 'start', 'end', 'color', 'turf')

    def clean_start(self, *args, **kwargs):
        start = self.cleaned_data.get("start")
        try:
            parse_datetime(start)
            year= parse_datetime(start).year
        except:
            raise forms.ValidationError("Not a valid date")
        else:
            if not 1800<parse_datetime(start).year<2500:
                raise forms.ValidationError("Choose a Valide Date")

        return start
    def clean_end(self, *args, **kwargs):
        end = self.cleaned_data.get("end")
        start = self.cleaned_data.get("start")
        
        
        try:
            parse_datetime(end)
            parse_datetime(start)
            year= parse_datetime(start).year
            year= parse_datetime(end).year
        except:
            raise forms.ValidationError("Not a valid date")
        else:
            if not parse_datetime(start)< parse_datetime(end):
                raise forms.ValidationError("Choose a date after start date")
            if not 1800<parse_datetime(end).year<2500:
                raise forms.ValidationError("Choose a year= parse_datetime(start).year Date")

        return end

    def clean_user(self, *args, **kwargs):
        user = self.cleaned_data.get("user")
        if " - " in user:
            raise forms.ValidationError('"Cannot Contain " - "')
        return user

class GalleryImgForm(ModelForm):
    username = forms.CharField(required=False)
    image = forms.ImageField(required=False,widget=forms.FileInput(attrs={'class':"form-control" }))
    caption = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Caption'}), help_text='Caption') 


    class Meta:
        model = TurfGallery
        fields = ('username','image','caption')


class DashboardHeader(ModelForm):
    username = forms.CharField(required=True)
    isheader = forms.ImageField(required=True,widget=forms.FileInput(attrs={'class':"form-control" }))

    class Meta:
        model = TurfGallery
        fields = ('username','isheader')
    
    # def save(self,request):
    #     updategallery = TurfGallery.objects.filter( username = request.user.username ).exclude(isheader="").exists()
    #     print("updategallery---",updategallery)
    #     print("self---",self.cleaned_data)
        # # table = TurfGallery(self.cleaned_data)

        # if updategallery:
        #     table.save()
        # else:
        #     table.update()



class CategoriesForm(ModelForm):
    category = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    image=forms.ImageField(required=False,widget=forms.FileInput(attrs={'class':"form-control" }))

    def clean_category(self, *args, **kwargs):
        category = self.cleaned_data.get("category")
        category_in_db = CategoriesModel.objects.filter(category=category).first()

        if category_in_db :
            raise forms.ValidationError('This category already exists')
        return category

    class Meta:
        model = CategoriesModel 
        fields = '__all__'


class CategoriesEditForm(ModelForm):
    category = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    image=forms.ImageField(required=False,widget=forms.FileInput(attrs={'class':"form-control" }))

    # def clean_category(self, *args, **kwargs):
    #     category = self.cleaned_data.get("category")
    #     category_in_db = CategoriesModel.objects.filter(category=category).first()

    #     if category_in_db :
    #         raise forms.ValidationError('This category already exists')
    #     return category

    class Meta:
        model = CategoriesModel 
        fields = '__all__'