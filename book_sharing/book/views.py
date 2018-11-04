from django.shortcuts import render, redirect, get_object_or_404
from users.models import UserProfile
from .models import UsersBook, Book
from .forms import BookForm
from django.db.models import Q
from django.contrib.auth.models import User
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


def owners(request):

     isbn = request.GET.get('isbn')
     book = Book.objects.get(isbn = isbn)
     user = UserProfile.objects.get(user = request.user)

     owner = UsersBook.objects.filter( owner_user=user).filter(book=book)

     if owner:
        return redirect(mybooks)

     owner = UsersBook.objects.filter( taken_user=user).filter(book=book)

     if owner:
       return redirect(requests)

     owners = UsersBook.objects.filter(book = book)
     return render(request, 'book_search/owners.html', {'owners': owners})


def requests(request):
    owner = UserProfile.objects.get(user=request.user)
    pending_request = UsersBook.objects.filter(owner_user=owner, pending_request=1)
    your_request = UsersBook.objects.filter(taken_user=owner, pending_request=1)
    your_books = UsersBook.objects.filter(taken_user=owner, pending_request=0)

    return render(request, 'book_search/requests.html', {'pending_request': pending_request, 'your_request': your_request,'your_books': your_books})


def grant(request):
    owner = request.GET.get('owner')
    owner = User.objects.get(username=owner)
    owner = UserProfile.objects.get(user=owner)

    book = request.GET.get('isbn')
    book = Book.objects.get(isbn=book)

    requester = request.GET.get('requester')
    requester = User.objects.get(username=requester)
    requester = UserProfile.objects.get(user=requester)

    userbook = UsersBook.objects.get(owner_user=owner, book=book, taken_user=requester)
    userbook.pending_request = 0
    book.availability -= 1
    userbook.save()
    book.save()

    return redirect(mybooks)


def deny(request):
    owner = request.GET.get('owner')
    owner = User.objects.get(username=owner)
    owner = UserProfile.objects.get(user=owner)

    book = request.GET.get('isbn')
    book = Book.objects.get(isbn=book)

    requester = request.GET.get('requester')
    requester = User.objects.get(username=requester)
    requester = UserProfile.objects.get(user=requester)

    userbook = UsersBook.objects.get(owner_user=owner, book=book, taken_user=requester)
    userbook.pending_request = 0
    userbook.taken_user = owner
    userbook.save()
    book.save()

    return redirect(mybooks)


def return_book(request):
    owner = request.GET.get('owner')
    owner = User.objects.get(username=owner)
    owner = UserProfile.objects.get(user=owner)

    book = request.GET.get('isbn')
    book = Book.objects.get(isbn=book)

    requester = request.GET.get('requester')
    requester = User.objects.get(username=requester)
    requester = UserProfile.objects.get(user=requester)

    userbook = UsersBook.objects.get(owner_user=owner, book=book, taken_user=requester)
    userbook.pending_request = 0
    userbook.taken_user = owner
    book.availability += 1
    userbook.save()
    book.save()

    return redirect(requests)

def requestbook(request):
    if request.user.is_authenticated:
        owner = request.GET.get('owner')
        owner = User.objects.get(username=owner)
        owner = UserProfile.objects.get( user=owner )
        book = request.GET.get('isbn')
        book = Book.objects.get(isbn = book)
        requester = UserProfile.objects.get(user = request.user)

        userbook = UsersBook.objects.get(owner_user=owner, book=book, taken_user=owner)
        if userbook:
            # print(userbook)
            userbook.taken_user = requester
            userbook.pending_request = 1
            userbook.save()

        return redirect(requests)

    else:
        return redirect('/user/signin')


def add_book(request):
    if request.user.is_authenticated:

        if request.GET.get('isbn') == None and request.GET.get('q') != None:
            isbn = request.GET.get('q')
            book = Book.objects.get(isbn = isbn)
            user = UserProfile.objects.get(user = request.user)

            books = Book.objects.filter( isbn = isbn)
            text = 'successful'

            owner = UsersBook.objects.filter( owner_user=user).filter(book=book)

            if owner:
                return render(request, 'book_search/add_book.html', {'books': books, 'text': text})


            book.availability += 1
            book.save()
            usersBook = UsersBook(owner_user=user, book=book, taken_user=user, pending_request=0)
            usersBook.save()

            return render(request, 'book_search/add_book.html', {'books': books, 'text': text})

        elif request.GET.get('isbn') == None and request.GET.get('q') == None:
            text = 'successful'
            books = None
        else:
            isbn = request.GET.get('isbn')
            books = Book.objects.filter( isbn = isbn)
            text = 'successful'
            if len(books) == 0:
                text = 'failure'

        return render(request, 'book_search/add_book.html', {'books': books, 'text': text})

    else:
        return redirect('/user/signin')

def add_book_form(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            form = BookForm(request.POST)
            if form.is_valid():
                form.save()

            book = Book.objects.filter(isbn=form.data['isbn'])[0]
            user = get_object_or_404(UserProfile, user=request.user)
            user_book = UsersBook.objects.create(taken_user=user, owner_user=user, book=book)
            user_book.save()
            return redirect(mybooks)
        else:
            form = BookForm()
            return render(request, 'book_search/add_book_form.html', {'form': form})
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

def mybooks(request):
    if request.user.is_authenticated:
        user = UserProfile.objects.get(user = request.user)
        books = UsersBook.objects.filter(owner_user=user)
        books = [x.book for x in books]
        return render(request, 'book_search/gallery.html', {'user': request.user, 'books': books,
                                                            'text': 'successful', 'fno': get_no_followers(request.user)})
    else:
        return redirect('/user/signin')
