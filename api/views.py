from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.models import SocialAccount


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


User = get_user_model()


@csrf_exempt  # Disabilita CSRF per test (in produzione usa un sistema più sicuro)
def google_authenticate(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            token = data.get("token")

            # Verifica il token con Google
            google_response = requests.get(
                f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
            )
            google_data = google_response.json()

            # Log della risposta di Google

            if "error_description" in google_data:
                return JsonResponse({"error": "Token non valido"}, status=400)

            email = google_data["email"]
            name = google_data.get("name", "")
            profile_picture_url = google_data.get("picture", None)
            print(profile_picture_url)
            # Controlla se l'utente esiste, altrimenti lo crea
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "username": email,
                    "first_name": name,
                    "profile_picture_url": profile_picture_url,
                },
            )

            # Log della creazione dell'utente
            print(f"User created or found: {user}")

            # Genera un token di autenticazione
            token, _ = Token.objects.get_or_create(user=user)
            print(f"\n TOKEN: {token} \n")
            return JsonResponse(
                {
                    "token": token.key,
                    "email": user.email,
                    "profile_picture_url": user.profile_picture_url,
                },
                status=200,
            )

        except Exception as e:
            # Stampa l'errore per capire cosa va storto
            print(f"Error during authentication: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Metodo non consentito"}, status=405)


class UserProfileView(APIView):

    authentication_classes = [TokenAuthentication]  # Usa TokenAuthentication
    permission_classes = [
        IsAuthenticated
    ]  # Solo gli utenti autenticati possono accedere

    def get(self, request):
        # Ottieni l'utente autenticato
        print(f"Authenticated user: {request}")  # Verifica se l'utente è autenticato

        print("Request Headers:", request.headers)  # Stampa gli header della richiesta
        print(
            "Request Method:", request.method
        )  # Stampa il metodo della richiesta (GET, POST, ecc.)
        print("Request User:", request.user)  # Stampa l'utente autenticato
        print(
            "Request Body:", request.data
        )  # Stampa i dati del corpo della richiesta (se ci sono)

        # Se vuoi stampare anche la URL richiesta
        print("Request Path:", request.path)

        # Se vuoi stampare i parametri della query (ad esempio per GET)
        print("Request GET Parameters:", request.GET)
        print("Request GET PP:", request.user.profile_picture_url)

        user = request.user
        # Restituisci i dettagli dell'utente come risposta JSON
        return Response(
            {
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "profile_picture_url": (
                    user.profile_picture_url
                    if hasattr(user, "profile_picture_url")
                    else None
                ),
            }
        )


class CampagnaListCreateView(APIView):
    def get(self, request):
        """
        Recupera tutte le campagne.
        """
        campagne = Campagna.objects.all()  # Recupera tutte le campagne dal database
        serializer = CampagnaSerializer(campagne, many=True)  # Serializza i dati
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Crea una nuova campagna.
        """
        serializer = CampagnaSerializer(
            data=request.data
        )  # Passa i dati in ingresso al serializer
        if serializer.is_valid():  # Verifica se i dati sono validi
            serializer.save()  # Salva la nuova campagna nel database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CampagnaDetailView(APIView):
    def get(self, request, pk):
        """
        Recupera i dettagli di una singola campagna.
        """
        try:
            campagna = Campagna.objects.get(pk=pk)  # Recupera la campagna con l'ID (pk)
            serializer = CampagnaSerializer(
                campagna
            )  # Serializza i dati della campagna
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Campagna.DoesNotExist:
            return Response(
                {"error": "Campagna non trovata!"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        """
        Aggiorna una campagna esistente con l'ID specificato.
        """
        try:
            campagna = Campagna.objects.get(pk=pk)  # Recupera la campagna con l'ID (pk)
            serializer = CampagnaSerializer(
                campagna, data=request.data
            )  # Serializza con i dati aggiornati
            if serializer.is_valid():  # Verifica se i dati sono validi
                serializer.save()  # Salva la campagna aggiornata
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Campagna.DoesNotExist:
            return Response(
                {"error": "Campagna non trovata!"}, status=status.HTTP_404_NOT_FOUND
            )

    def patch(self, request, pk):
        """
        Aggiorna parzialmente una campagna esistente con l'ID specificato.
        """
        try:
            campagna = Campagna.objects.get(pk=pk)  # Recupera la campagna con l'ID (pk)
            serializer = CampagnaSerializer(
                campagna, data=request.data, partial=True
            )  # Aggiornamento parziale
            if serializer.is_valid():  # Verifica se i dati sono validi
                serializer.save()  # Salva le modifiche parziali
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Campagna.DoesNotExist:
            return Response(
                {"error": "Campagna non trovata!"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        """
        Elimina una campagna esistente con l'ID specificato.
        """
        try:
            campagna = Campagna.objects.get(pk=pk)  # Recupera la campagna con l'ID (pk)
            campagna.delete()  # Elimina la campagna dal database
            return Response(
                {"message": "Campagna eliminata con successo!"},
                status=status.HTTP_204_NO_CONTENT,  # Status 204 indica che la cancellazione è avvenuta senza contenuto di risposta
            )
        except Campagna.DoesNotExist:
            return Response(
                {"error": "Campagna non trovata!"}, status=status.HTTP_404_NOT_FOUND
            )
