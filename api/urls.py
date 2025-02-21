from django.urls import path, include
from .views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="CER APIs",
        default_version="v1",
        description="API documentation for CER project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("api/", home),
    path("me/", UserDetailView.as_view(), name="user-detail"),
    path("api/authenticate/", google_authenticate, name="google_authenticate"),
    path("api/profile/", UserProfileView.as_view(), name="user_profile"),
    path("api/campagne/", CampagnaListCreateView.as_view(), name="campaigns"),
    path(
        "api/campagne/<int:pk>/", CampagnaDetailView.as_view(), name="campagna-detail"
    ),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
