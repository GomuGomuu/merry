from typing import Any

from django.contrib.auth.base_user import BaseUserManager
from django.db import IntegrityError


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username: str, password: str, name: str, **extra_fields: Any):
        if name is None:
            raise TypeError("Users must have an name")
        if username is None:
            raise TypeError("Users must have a username")
        try:
            user = self.model(username=username, name=name, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)

        except IntegrityError:
            raise ValueError("User already exists")

        return user

    def create_superuser(self, username: str, password: str, **extra_fields: Any):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        return self.create_user(username, password, name="Superuser", **extra_fields)

    def get_all_users(self):
        return self.all()
