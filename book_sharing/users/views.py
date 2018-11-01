from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile

# Create your views here.

from django.contrib.auth import authenticate, login, logout
from .forms import ProfileForm, UserForm


def user_profile(request):
    if request.user.is_authenticated:
        user = get_object_or_404(UserProfile, user=request.user)

        if request.method == 'POST':
            form = ProfileForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
            return render(request, 'login/profile.html', {'form': form, 'user':user.user.username})
        else:
            form = ProfileForm(instance=user)
            return render(request, 'login/profile.html', {'form': form, 'user':user.user.username})
    else:
        return redirect('/user/signin')


def sign_in(request):

    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login/failed.html', {})
    else:
        return render(request, 'login/login.html', {'user':'signin'})


def sign_out(request):
    logout(request)
    return redirect('/')
