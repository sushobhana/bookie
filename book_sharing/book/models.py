from django.db import models

# Create your models here.


class Book(models.Model):

    def __str__(self):
        return self.title

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    edition = models.IntegerField()
    tags = None
    description = models.IntegerField(max_length=100)
    rating = None
