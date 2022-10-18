from django.shortcuts import render
from django.views.generic import View
from .forms import creatematchForm
# from .models import slotModel

# Create your views here.

class Test(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html',{ })
class Shop(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'e_commerce/shop.html',{ })

# class Signin(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'accounts/sign-up.html',{ })

class AllMatchesView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Matches/all-matches.html',{ })
class MyMatchesView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Matches/my-matches.html',{ })


#creat natches

class CreateMatchesView(View):
    template = 'Matches/create-matches.html'
    def get(self, request, *args, **kwargs):

        form = creatematchForm()
        # user = request.user
        
        context = {'form': form,
                    'data': 'Add match',
                    # 'user': user,
                    }
        
        return render(request,self.template,context)






   
class TurfsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'turf/main.html',{ })