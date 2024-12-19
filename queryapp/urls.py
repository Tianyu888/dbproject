from django.urls import path
from .views import natural_language_query,index

urlpatterns = [
    path("", index, name="index"),  # Default page
    path("query/", natural_language_query, name="natural_language_query"),
]