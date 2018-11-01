from django.shortcuts import render

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        print(request.user)
        return render(request, 'book_search/gallery.html', {'user': request.user})
    else:
        return render(request, 'book_search/gallery.html', {'user': 'Signin'})
