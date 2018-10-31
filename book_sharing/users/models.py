from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    phone_number = models.DecimalField(max_digits=10, decimal_places=0)
    birth_date = models.DateField()
    address = models.TextField(max_length=100)
    gender = models.CharField(max_length=2)

    def __str__(self):
        return self.user.username
