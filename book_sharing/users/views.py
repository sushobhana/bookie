from django.shortcuts import render

# Create your views here.

from django.shortcuts import render


def user_login(request):
    return render(request, 'login/login.html', {})


def sign_in(request):
    user = request.POST['username']