from django.shortcuts import render, redirect

# Create your views here.

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def user_profile(request):
    if request.user.is_authenticated:
        return render(request, 'login/profile.html', {'user': User.objects.filter(username=request.user)[0]})
    else:
        return redirect('/user/signin')


def sign_in(request):

    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request, 'login/success.html', {})
        else:
            return render(request, 'login/failed.html', {})
    else:
        return render(request, 'login/login.html', {})


def sign_out(request):
    logout(request)
    return redirect('/')
