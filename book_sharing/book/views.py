from django.shortcuts import render
from .models import Book
from django.db.models import Q
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        print(request.user)
        books = Book.objects.all()[:2]
        return render(request, 'book_search/gallery.html', {'user': request.user, 'books': books})
    else:
        return render(request, 'book_search/gallery.html', {'user': 'Signin'})

def search(request):
    query = request.GET.get('query')
    books = Book.objects.filter(Q(title__icontains = query) | Q(author__icontains = query) | Q(publisher__icontains = query))
    if str(query) == "*":
        books = Book.objects.all()[:2]
    text = 'succesful'
    if len(books) == 0:
        text = 'Nothing matches your Query :('
    return render(request, 'book_search/gallery.html', { 'user' : request.user , 'books': books, 'text': text})
