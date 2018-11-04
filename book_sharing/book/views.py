from django.shortcuts import render, redirect, get_object_or_404
from users.models import UserProfile
from .models import UsersBook, Book
from .forms import BookForm
from django.db.models import Q
from django.contrib.auth.models import User
from users.views import get_no_followers
from difflib import SequenceMatcher


# Create your views here.


def home(request):
    if request.user.is_authenticated:
        print(request.user)
        books = Book.objects.all().order_by('-rating')[0: 15]

        return render(request, 'book_search/gallery.html', {'user': request.user, 'books': books,
                                                            'fno': get_no_followers(request.user)})
    else:
        return render(request, 'book_search/gallery.html', {'user': 'Signin'})


def owners(request):
    isbn = request.GET.get('isbn')
    book = Book.objects.get(isbn=isbn)
    user = UserProfile.objects.get(user=request.user)

    owner = UsersBook.objects.filter(owner_user=user).filter(book=book)

    if owner:
        return redirect(mybooks)

    owner = UsersBook.objects.filter(taken_user=user).filter(book=book)

    if owner:
        return redirect(requests)

    owners = UsersBook.objects.filter(book=book)
    return render(request, 'book_search/owners.html', {'owners': owners})


def requests(request):
    owner = UserProfile.objects.get(user=request.user)
    pending_request = UsersBook.objects.filter(owner_user=owner, pending_request=1)
    your_request = UsersBook.objects.filter(taken_user=owner, pending_request=1)
    your_books = UsersBook.objects.filter(taken_user=owner, pending_request=0)
    books = []
    for book in your_books:
        if book.taken_user != book.owner_user:
            books.append(book)

    return render(request, 'book_search/requests.html',
                  {'pending_request': pending_request,
                   'your_request': your_request, 'your_books': books})


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
        owner = UserProfile.objects.get(user=owner)
        book = request.GET.get('isbn')
        book = Book.objects.get(isbn=book)
        requester = UserProfile.objects.get(user=request.user)

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
            book = Book.objects.get(isbn=isbn)
            user = UserProfile.objects.get(user=request.user)

            books = Book.objects.filter(isbn=isbn)
            text = 'successful'

            owner = UsersBook.objects.filter(owner_user=user).filter(book=book)

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
            books = Book.objects.filter(isbn=isbn)
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
    fulltext = request.GET.get('query')

    if fulltext is None:
        return redirect('/')

    titles = Book.objects.values('title')
    authors = Book.objects.values('author')
    tags = Book._meta.get_field('tags').choices
    query = []
    p_query = []

    THRESHOLD = .7

    titles = [x['title'] for x in titles]
    authors = [x['author'] for x in authors]
    tags = [x[0] for x in tags]
    print(tags)

    for title in titles:
        print(title, fulltext)
        score = SequenceMatcher(None, title.lower(), fulltext.lower()).ratio()
        if score == 1:
            # Perfect Match for name
            p_query += Book.objects.filter(Q(title=title))
        elif score >= THRESHOLD:
            query += (Book.objects.filter(Q(title=title)))

    for author in authors:
        print(author, fulltext)
        score = SequenceMatcher(None, author.lower(), fulltext.lower()).ratio()
        if score == 1:
            # Perfect Match for name
            p_query += Book.objects.filter(Q(author=author))

        elif score >= THRESHOLD:
            query += (Book.objects.filter(Q(author=author)))

    for tag in tags:
        print(tag, fulltext)
        score = SequenceMatcher(None, tag.lower(), fulltext.lower()).ratio()
        if score == 1:
            # Perfect Match for name
            p_query += Book.objects.filter(Q(tags=[tag]))
        elif score >= .3:
            for book in Book.objects.all():
                if tag in book.tags:
                    query.append(book)

    if len(p_query) > 0:
        query = p_query

    query = set(query)

    text = ''
    if not query:
        text = 'No Results found :( Try with some more characters'
        return render(request, 'book_search/gallery.html', {'user': request.user, 'text': text,
                                                            'fno': get_no_followers(request.user)})
    else:

        return render(request, 'book_search/gallery.html', {'user': request.user, 'books': query, 'text': text,
                                                            'fno': get_no_followers(request.user)})


def mybooks(request):
    if request.user.is_authenticated:
        user = UserProfile.objects.get(user=request.user)
        books = UsersBook.objects.filter(owner_user=user)
        books = [x.book for x in books]
        return render(request, 'book_search/gallery.html', {'user': request.user, 'books': books,
                                                            'text': 'successful',
                                                            'fno': get_no_followers(request.user)})
    else:
        return redirect('/user/signin')
