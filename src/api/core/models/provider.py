from django.apps import apps
from django.db import models


class AbstractProvider(models.Model):
    name = models.CharField(max_length=30, unique=True)
    app_label = models.CharField(max_length=50)

    class Meta:
        abstract = True

    @property
    def app_config(self):
        return apps.get_app_config(self.app_label)

    @property
    def module(self):
        return self.app_config.module

    def get_model(self, model_name):
        return self.app_config.get_model(model_name)

    def __str__(self) -> str:
        return self.name
