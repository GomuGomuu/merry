from api.card.models.card import Card
from api.core.models.image import AbstractImage
from django.db import models
from api.core.utils import slugify


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)


class CardImage(AbstractImage):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="images")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="tag")

    def __str__(self):
        return self.card.name
