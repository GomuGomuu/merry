from django.core.management.base import BaseCommand

from api.card.services.update_card import update_illustration_visual_description


class Command(BaseCommand):
    help = "Update visual description of illustrations"

    def handle(self, *args, **options):
        update_illustration_visual_description()
