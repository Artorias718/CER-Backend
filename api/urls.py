from django.urls import path, include
from .views import *

urlpatterns = [
    path("api/", home),
    path("me/", UserDetailView.as_view(), name="user-detail"),
    path("api/cats/", CatListAPIView.as_view(), name="cat-list"),
]
