from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext as _


from .forms import RegistrationForm,CustomProfileForm
from .models import FilaUser,Profile#,FilaSub


def index(request):
    return HttpResponse("homepage")
def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print(request)
        if form.is_valid():
            print(request.POST)
            form.save()

            return redirect(reverse('formular'))

        else:

            return render(request,'registration/register.html',{'form':form})

    else:
        form = RegistrationForm()

    return render(request,'registration/register.html',{'form':form})

@login_required
def formular(request):

    user = request.user
    form = CustomProfileForm(instance=user.userprofile)

    if request.method == 'POST':

        form = CustomProfileForm(request.POST,request.FILES,instance=user.userprofile)
        print(form.errors)
        if form.is_valid():
            form.save()

            messages.success(request, _("Your profile information has been updated successfully."), fail_silently=True)
            return redirect(reverse('login'))#render(request,'registration/profile.html')#redirect(reverse('login'))
        else:
            return render(request,'registration/formular.html',{'form':form})
    else:
        form = CustomProfileForm(instance=user.userprofile)

    return render(request,'registration/formular.html',{'form':form})

@login_required
def view_profile(request):

    user = request.user
    return render(request,'registration/profile.html',{'user':user})
