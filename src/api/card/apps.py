from django.apps import AppConfig

from django.db.models.signals import post_migrate

from api.core.utils import slugify


def create_default_data(sender, **kwargs):
    from api.card.models.card import SideEffect

    side_effects = [
        "Rush",
        "Blocker",
        "Main",
        "Active:Main",
        "On Play",
        "On KO",
        "Double Attack",
        "Once per Turn",
        "Your Turn",
        "Opponent's Turn",
        "End of your turn",
        "Return DON",
        "Return to Hand",
        "Trash DON",
        "Trash from Hand",
        "Trash this",
    ]

    if not SideEffect.objects.exists():
        SideEffect.objects.bulk_create(
            [
                SideEffect(name=side_effect, slug=slugify(side_effect))
                for side_effect in side_effects
            ]
        )


class CardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.card"

    def ready(self):
        post_migrate.connect(create_default_data, sender=self)
