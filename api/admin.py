from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


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


admin.site.register(CustomUser, CustomUserAdmin)


# Register your models here.


@admin.register(Campagna)
class CampagnaAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "ente_promotore",
        "soglia_minima",
        "soglia_massima",
        "soglia_versata",
        "ha_raggiunto_minimo",
        "completata",
    )
    search_fields = ("name", "ente_promotore")
    list_filter = ("completata", "ha_raggiunto_minimo")
