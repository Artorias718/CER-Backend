from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("api.urls")),  # include tutto quello che è nell urls.py di api
    path(
        "accounts/", include("allauth.urls")
    ),  # Questo include tutte le rotte di allauth
]
