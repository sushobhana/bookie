from django.db import models
from users.models import UserProfile

# Create your models here.
class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

class Tags(models.Model):

    name = models.CharField(
        max_length=20,
    )

    def __str__(self):
        return self.name

class Book(models.Model):

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    edition = models.IntegerField()
    tags = models.ManyToManyField(Tags)
    description = models.CharField(max_length=300)
    isbn = models.CharField(primary_key=True, max_length=300, default='0000')
    rating = IntegerRangeField(min_value=0, max_value=10)

    def __str__(self):
        return self.title

class UsersBook(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = IntegerRangeField(default=1, min_value=0)

    def __str__(self):
        return self.book.title
