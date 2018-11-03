from django.shortcuts import render, redirect, get_object_or_404
from users.models import UserProfile
from .models import UsersBook, Book
from .forms import BookForm
from django.db.models import Q
from users.views import get_no_followers


# Create your views here.


def home(request):
    if request.user.is_authenticated:
        print(request.user)
        books = Book.objects.all()

        return render(request, 'book_search/gallery.html', {'user': request.user, 'books': books,
                                                            'fno':get_no_followers(request.user)})
    else:
        return render(request, 'book_search/gallery.html', {'user': 'Signin'})


def add_book(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            form = BookForm(request.POST)
            if form.is_valid():
                form.save()
            book = Book.objects.filter(isbn=form.data['isbn'])[0]
            user = get_object_or_404(UserProfile, user=request.user)
            user_book = UsersBook.objects.create(taken_user=user, owner_user=user, book=book)
            user_book.save()
            return render(request, 'book_search/add_book.html', {'form': form})
        else:
            form = BookForm()
            return render(request, 'book_search/add_book.html', {'form': form})
    else:
        return redirect('/user/signin')


def search(request):
    query = request.GET.get('query')
    tag = request.GET.get('tag')
    author = request.GET.get('author')

    if query is None and tag is None and author is None:
        return redirect('/')

    list_books = []

    if query != '*' and query is not None:
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query)
                                    | Q(publisher__icontains=query))
    else:
        query = '*'

    if query == '*':
        books = Book.objects.all()

    if tag is not None:
        for book in books:
            if tag in book.tags:
                list_books.append(book)

    if author is not None:
        for book in books:
            if author == book.author:
                list_books.append(book)

    if tag is None and author is None:
        list_books = books

    text = 'successful'
    if len(books) == 0:
        text = 'No Results found :('

    return render(request, 'book_search/gallery.html', {'user': request.user, 'books': list_books, 'text': text,
                                                        'fno': get_no_followers(request.user)})
