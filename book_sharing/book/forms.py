form django import forms
form .models import Book

class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ('title', 'author', 'publisher', 'description', 'edition', 'tags', 'isbn', 'rating')
