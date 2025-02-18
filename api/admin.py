from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


# Register your models here.
@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "age",
        "color",
        "breed",
    )  # Le colonne da visualizzare nell'admin
    search_fields = ("name", "color", "breed")  # Campi su cui poter cercare nell'admin


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "birthday",
        "profile_picture_url",
    )  # Cosa mostrare nella lista
    list_filter = ("birthday",)  # Filtra per data di nascita
    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )  # Aggiungi i campi per la ricerca
    ordering = ("username",)  # Ordinamento per nome utente
    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {"fields": ("birthday", "profile_picture_url")},
        ),  # Aggiungi questi campi al modulo di creazione/modifica
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {"fields": ("birthday", "profile_picture_url")},
        ),  # Aggiungi questi campi al modulo di aggiunta
    )


# Registra il CustomUser con l'admin
admin.site.register(CustomUser, CustomUserAdmin)
