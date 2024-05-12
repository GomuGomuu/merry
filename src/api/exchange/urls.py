from django.urls import path

from . import views

app_name = "exchange"

urlpatterns = [
    path("", views.provider_list, name="exchange_provider_list"),
    path("<int:illustration_id>/", views.price_history, name="price_history"),
    path(
        "<int:illustration_id>/available_exchanges/",
        views.available_exchanges,
        name="illustration_price_detail",
    ),
    path(
        "<int:illustration_id>/<int:provider_id>/",
        views.price_history,
        name="price_history_by_provider",
    ),
]
