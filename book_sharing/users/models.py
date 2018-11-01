from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):

    GENDER_CHOICES = (
        ('M', 'MALE'),
        ('F','FEMALE'),
        ('O','OTHER'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField()
    phone_number = models.DecimalField(max_digits=10, decimal_places=0)
    birth_date = models.DateField()
    address = models.TextField(max_length=200)
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
    )

    def __str__(self):
        return self.user.username
