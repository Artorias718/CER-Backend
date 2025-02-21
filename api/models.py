from django.db import models

from django.contrib.auth.models import User
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    birthday = models.DateField(null=True, blank=True)
    profile_picture_url = models.URLField(max_length=200, null=True, blank=True)


class Campagna(models.Model):
    name = models.CharField(max_length=200)  # Nome della campagna
    ente_promotore = models.CharField(max_length=200)  # Ente promotore
    description = models.TextField()  # Descrizione della campagna
    soglia_minima = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Soglia minima da raggiungere
    soglia_massima = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Soglia massima
    soglia_versata = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )  # Soldi raccolti finora
    ha_raggiunto_minimo = models.BooleanField(
        default=False
    )  # Flag per soglia minima raggiunta
    completata = models.BooleanField(default=False)  # Flag per campagna completata
    cover_image_url = models.URLField(
        max_length=500, blank=True
    )  # URL immagine di copertina

    def __str__(self):
        return self.name
