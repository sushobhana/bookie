from django.shortcuts import render, redirect, get_object_or_404
from users.models import UserProfile
from .models import UsersBook, Book
from .forms import BookForm


# Create your views here.


def home(request):
    if request.user.is_authenticated:
        print(request.user)
        return render(request, 'book_search/gallery.html', {'user': request.user})
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
