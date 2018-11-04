from django.shortcuts import render, redirect, get_object_or_404
from users.models import UserProfile
from .models import UsersBook, Book
from .forms import BookForm
from django.db.models import Q
from users.views import get_no_followers
from difflib import SequenceMatcher


# Create your views here.


def home(request):
    if request.user.is_authenticated:
        print(request.user)
        books = Book.objects.all()

        return render(request, 'book_search/gallery.html', {'user': request.user, 'books': books,
                                                            'fno': get_no_followers(request.user)})
    else:
        return render(request, 'book_search/gallery.html', {'user': 'Signin'})


def add_book(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            form = BookForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                isbn = form.data['isbn']
                book = Book.objects.get(isbn=isbn)
                if book:
                    book.availability += book.availability

            book = Book.objects.filter(isbn=form.data['isbn'])[0]
            user = get_object_or_404(UserProfile, user=request.user)
            user_book = UsersBook.objects.create(taken_user=user, owner_user=user, book=book)
            user_book.save()
            return render('/mybooks')
        else:
            form = BookForm()
            return render(request, 'book_search/add_book.html', {'form': form})
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

    THRESHOLD = .4

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
