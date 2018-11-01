from django.shortcuts import render
from .models import Book
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        print(request.user)
        books = Book.objects.all()
        return render(request, 'book_search/gallery.html', {'user': request.user, 'books': books})
    else:
        return render(request, 'book_search/gallery.html', {'user': 'Signin'})
