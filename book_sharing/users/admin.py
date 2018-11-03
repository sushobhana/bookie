from django.contrib import admin
from .models import UserProfile, UserFollowers
from .forms import ProfileForm
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(UserFollowers)
