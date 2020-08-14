from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    balance = models.FloatField(default=0)


class Animal(models.Model):
    KINDS = [
        ('CT', 'Cat'),
        ('HH', 'Hedgehod')
    ]
    kind = models.CharField(choices=KINDS, max_length=2)
    name = models.CharField(max_length=123)
    breed = models.CharField(max_length=123)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='animals')


class Lot(models.Model):
    animal = models.ForeignKey('Animal', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField()


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name='bids')
    price = models.FloatField()
