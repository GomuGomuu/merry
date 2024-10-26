from django.urls import path
from . import views

urlpatterns = [
    path("", views.card_recognition, name="card_recognition"),
]
