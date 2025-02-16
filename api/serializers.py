from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = ["id", "name", "age", "color", "breed"]  # I campi che vogliamo esporre
