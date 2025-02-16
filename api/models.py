from django.db import models

from django.contrib.auth.models import User
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view


from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    birthday = models.DateField(null=True, blank=True)


class Cat(models.Model):
    name = models.CharField(max_length=100)  # Aggiungiamo un nome al gatto (opzionale)
    age = models.IntegerField()  # Età del gatto
    color = models.CharField(max_length=50)  # Colore del gatto
    breed = models.CharField(max_length=100)  # Razza del gatto

    def __str__(self):
        return self.name
