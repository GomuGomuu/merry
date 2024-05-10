from django.db import models

from api.core.models.base_model import BaseModel


class Op(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class DeckColor(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ArtType(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Type(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Card(BaseModel):
    name = models.CharField(max_length=100)
    is_dom = models.BooleanField(default=False)
    cost = models.PositiveIntegerField()
    power = models.PositiveIntegerField()
    counter_value = models.PositiveIntegerField()
    crew = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    op = models.ForeignKey(Op, on_delete=models.PROTECT)
    deck_color = models.ManyToManyField(DeckColor, related_name="deck_colors")
