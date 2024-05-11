from django.urls import path

from . import views

app_name = "cards"

urlpatterns = [
    path("", views.card_list, name="card_list"),
    path("create/", views.create_card, name="create_card"),
    path("<int:pk>/", views.card_detail, name="card_detail"),
    path("<int:pk>/update/", views.update_card, name="update_card"),
    path("<int:pk>/delete/", views.delete_card, name="delete_card"),
    path("<int:pk>/illustration/", views.card_illustrations, name="card_illustration"),
    path(
        "<int:pk>/illustration/create/",
        views.create_card_illustration,
        name="create_card_illustration",
    ),
    path(
        "<int:pk>/illustration/<int:illustration_id>/",
        views.card_illustration_detail,
        name="card_illustration_detail",
    ),
    path("illustrations/", views.illustration_list, name="illustration_list"),
    path("op/", views.op_list, name="op_list"),
    path("op/<int:pk>/", views.op_detail, name="op_detail"),
    path("deck_color/", views.deck_color_list, name="deck_color_list"),
    path("deck_color/<int:pk>/", views.deck_color_detail, name="deck_color_detail"),
]
