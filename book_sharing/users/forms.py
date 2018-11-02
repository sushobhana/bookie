from django import forms
from django.contrib.auth.models import User

from .models import UserProfile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('email', 'gender', 'address', 'phone_number', 'birth_date')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password')
