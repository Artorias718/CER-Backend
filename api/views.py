from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from .models import *
from .serializers import *


def home(request):
    return HttpResponse("This is the homepage")


class UserDetailView(APIView):
    permission_classes = [
        IsAuthenticated
    ]  # Solo gli utenti autenticati possono vedere i dati

    def get(self, request):
        user = request.user  # Ottieni l'utente che ha fatto la richiesta
        serializer = UserSerializer(user)
        return Response(serializer.data)


class CatListAPIView(APIView):
    def get(self, request):
        # Recupera tutti i gatti dal database
        cats = Cat.objects.all()

        # Serializza i dati
        serializer = CatSerializer(cats, many=True)

        # Restituisci i dati serializzati come risposta
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Crea una nuova istanza del serializzatore con i dati inviati nella richiesta
        serializer = CatSerializer(data=request.data)

        # Verifica che i dati siano validi
        if serializer.is_valid():
            # Salva il nuovo gatto nel database
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )  # Risposta con i dati del gatto creato
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )  # Risposta con gli errori di validazione
