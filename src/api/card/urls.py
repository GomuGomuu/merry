from django.urls import path, include

from . import views

app_name = "cards"

card_urls = [
    path("", views.card_detail, name="card_detail"),
    path("update/", views.update_card, name="update_card"),
    path("delete/", views.delete_card, name="delete_card"),
    path("illustration/", views.card_illustrations, name="card_illustration"),
    path(
        "illustration/create/",
        views.create_card_illustration,
        name="create_card_illustration",
    ),
    path(
        "illustration/<int:illustration_id>/",
        views.card_illustration_detail,
        name="card_illustration_detail",
    ),
]

urlpatterns = [
    path("", views.card_list, name="card_list"),
    path("create/", views.create_card, name="create_card"),
    path(
        "<str:slug>/",
        include(card_urls),
    ),
    path("illustrations/", views.illustration_list, name="illustration_list"),
    path("op/", views.op_list, name="op_list"),
    path("op/<int:pk>/", views.op_detail, name="op_detail"),
    path("deck_color/", views.deck_color_list, name="deck_color_list"),
    path("deck_color/<int:pk>/", views.deck_color_detail, name="deck_color_detail"),
]
