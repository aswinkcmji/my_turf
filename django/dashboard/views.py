from django.shortcuts import render
from django.views.generic import View

# Create your views here.

class Turf_Dashboard(View):
    def get(self,request):
        return render(request,"turf/turf_dashboard.html",{})