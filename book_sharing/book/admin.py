from django.contrib import admin
from .models import Tags, Book, UsersBook

# Register your models here.
admin.site.register(Book)
admin.site.register(Tags)
admin.site.register(UsersBook)
