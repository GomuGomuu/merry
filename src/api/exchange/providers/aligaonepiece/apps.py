from django.apps import AppConfig


class AligaonepieceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.exchange.providers.aligaonepiece"
    label = "exchange_aligaonepiece"
    verbose_name = "Exchange A Liga One Piece"

    def ready(self) -> None:
        from . import service  # noqa

        return super().ready()
