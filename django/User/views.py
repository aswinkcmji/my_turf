from django.shortcuts import render,redirect
from django.views.generic import View
from .forms import *
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from .models import *

# from .models import slotModel

# Create your views here.

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html',{ })

class AllMatchesView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Matches/all-matches.html',{ })
class MyMatchesView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Matches/my-matches.html',{ })

#create matches
class CreateMatches(View):
    template = 'Matches/create-matches.html'
    def get(self, request, *args, **kwargs):

        a = createMatchForm()
        user = request.user
        
        print("-------------------------------------------------------------------------")
        context = { 'form': a,
                    'data': 'Create Matches',
                    'user': user,
                    }
        
        return render(request,self.template,context)
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
                a = createMatchForm(request.POST)
                print("////////////////////////////////////////////////////////////////////")
                if a.is_valid():
                    a.save()
                    print(a,"++++++++++++++++++++++++++++++=")
                    print("***************************************************************")

                    messages.success(request, 'Form submission successful')
                    print('a')
                    return redirect('my-matches')
                else:
                    print("=============================================================")

                    messages.warning(request, 'Form submission failed')
                    print("....................................................................")

                    return redirect('my-matches')
                    
        else:   
            form = createMatchForm()
            return render(request, self.template, {'form': form, 'title':'create here'})




    #  def get(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #        context = {'form': form,
    #                 'data': 'Add match',
    #                 'user': user,
    #                 }
    #     return render(request, 'Matches/create-matches.html',context)

    #  def post(self, request, *args, **kwargs):
    #         if request.method == 'POST':
    #             form = creatematchForm(request.POST)
    #             if form.is_valid():
    #                 form.save()
    #                 messages.success(self.request, "Match Created Successfully")
    #                 return HttpResponseRedirect(reverse('my-matches'))
                        
    #             else:
    #                     context ={}
    #                     context['form'] = form
    #                     return render(request, 'accounts/sign-up.html',context)











    # template = 'Matches/create-matches.html'
    # def get(self, request, *args, **kwargs):

    #     form = creatematchForm()
    #     # user = request.user
    #     print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",form.options)
    #     context = {'form': form,
    #                 'data': 'Add match',
    #                 # 'user': user,
    #                 }
        
    #     return render(request,self.template,context)






class TurfsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'turf/main.html',{ })