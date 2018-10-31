from django.contrib import admin
from .models import UserProfile
from .forms import ProfileForm
# Register your models here.

admin.site.register(UserProfile)
