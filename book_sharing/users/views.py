from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile

# Create your views here.

from django.contrib.auth import authenticate, login, logout
from .forms import ProfileForm, UserForm
from django.contrib.auth.models import User


def user_profile(request):

    if request.user.is_authenticated:

        user = get_object_or_404(User, username=request.user.username)
        profile = UserProfile.objects.filter(user=user)

        if profile is None:
            redirect('/user/register_profile')

        profile = get_object_or_404(UserProfile, user=user)

        if request.method == 'POST':
            form = ProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
            return render(request, 'login/profile.html', {'form': form, 'user': user.username})
        else:
            form = ProfileForm(instance=profile)
            return render(request, 'login/profile.html', {'form': form, 'user': user.username})
    else:

        return redirect('/user/signin')


def sign_in(request):

    if request.method == 'POST':
        form = UserForm(request.POST)

        user = authenticate(request, username=form.data['username'], password=form.data['password'])

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login/login.html', {'user': 'Signin','form': form, 'msg':'Please, Try Again.'})
    else:
        form = UserForm()
        return render(request, 'login/login.html', {'user': 'signin', 'form':form, 'msg':'Sign in'})


def sign_out(request):
    logout(request)
    return redirect('/')


def register_user(request):

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = User.objects.create_user(username=username, password=password)
            user.save()

            user1 = authenticate(request, username=username, password=password)

            login(request, user=user1)

            return redirect('/user/register_profile')
        else:

            return render(request, 'login/register.html', {'form': form})

    else:
        form = UserForm()
        return render(request, 'login/register.html', {'form': form})


def register_profile(request):
    user = get_object_or_404(User, username=request.user.username)

    if request.method == 'POST':

        form = ProfileForm(request.POST, instance=request.user)

        if form.is_valid():

            email = form.cleaned_data['email']
            gender = form.cleaned_data['gender']
            ph_no = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            dob = form.cleaned_data['birth_date']

            profile = UserProfile.objects.create(user=user, gender=gender, phone_number=ph_no,
                                                 address=address, birth_date=dob, email=email)
            profile.save()

            return redirect('/')

        else:
            return render(request, 'login/register_profile.html', {'form': form, 'user': user.username})

    else:

        form = ProfileForm(instance=user)
        return render(request, 'login/register_profile.html', {'form': form, 'user': user.username})
