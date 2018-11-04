from django.contrib import admin
from .models import Book, UsersBook

# Register your models here.
admin.site.register(Book)
admin.site.register(UsersBook)
