import uuid
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=False)
    password = models.CharField(max_length=255, blank=False)
    username = models.CharField(max_length=255, unique=True, blank=False)

    is_superuser = models.BooleanField(_("Is admin"), default=False)
    is_staff = models.BooleanField(_("Is staff"), default=False)
    is_active = models.BooleanField(_("Is active"), default=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
