from django.urls import path

from . import views

app_name = "cards"

urlpatterns = [
    path("", views.card_list, name="card_list"),
    path("create/", views.create_card, name="create_card"),
    path("<int:pk>/", views.card_detail, name="card_detail"),
    path("<int:pk>/update/", views.update_card, name="update_card"),
    path("<int:pk>/delete/", views.delete_card, name="delete_card"),
    path("op/", views.op_list, name="op_list"),
    path("op/<int:pk>/", views.op_detail, name="op_detail"),
    path("deck_color/", views.deck_color_list, name="deck_color_list"),
    path("deck_color/<int:pk>/", views.deck_color_detail, name="deck_color_detail"),
    path("art_type/", views.art_type_list, name="art_type_list"),
    path("art_type/<int:pk>/", views.art_type_detail, name="art_type_detail"),
    path("type/", views.type_list, name="type_list"),
    path("type/<int:pk>/", views.type_detail, name="type_detail"),
]
