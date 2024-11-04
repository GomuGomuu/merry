from django.urls import path
from . import views

urlpatterns = [
    path("collection/", views.get_collection, name="get_default_collection"),
    path(
        "collection/<int:collection_id>/", views.get_collection, name="get_collection"
    ),
    path("collections/", views.collections, name="add_illustration_to_collection"),
    path("manage-illustration/", views.manage_illustration_on_vault, name="manage_illustration_on_vault"),
]
