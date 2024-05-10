import logging

from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


def create_admin():
    from django.contrib.auth import get_user_model

    User = get_user_model()

    if not User.objects.exists():
        User.objects.create_superuser("admin", password="gomugomu")


class Command(BaseCommand):
    help = "Initialize development structure"

    def handle(self, *args, **options):
        logger.warning("Initializing development structure")

        logger.warning("Creating admin user")
        create_admin()
