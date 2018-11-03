from django.db import models
from users.models import UserProfile
from multiselectfield import MultiSelectField


# Create your models here.


class IntegerRangeField(models.IntegerField):

    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Tags(models.Model):

    select_choices = ('EDUCATIONAL', 'NON-EDUCATIONAL')
    select_choices = {(x, x) for x in select_choices}

    name = models.CharField(choices=select_choices, null=True, blank=True, max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    edition = models.IntegerField()

    select_choices = ('EDUCATIONAL', 'NON-EDUCATIONAL')
    select_choices = {(x, x) for x in select_choices}
    tags = MultiSelectField(choices=select_choices, null=True, blank=True, max_length=50)
    description = models.CharField(max_length=300)
    isbn = models.CharField(primary_key=True, max_length=300, default='0000')
    rating = IntegerRangeField(min_value=0, max_value=10, default=5)

    def __str__(self):
        return self.title


class UsersBook(models.Model):

    owner_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='creator')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    taken_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='hasbook',
                                   default=None, null=True)

    def __str__(self):
        return self.book.title