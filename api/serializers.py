from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class CampagnaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campagna
        fields = "__all__"
