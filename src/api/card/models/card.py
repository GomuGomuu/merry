from django.db import models

from api.core.models.base_model import BaseModel
from api.core.utils import slugify


class Op(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class DeckColor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Crew(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class SideEffect(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Card(BaseModel):
    # rare choices
    COMMON = "C"
    UNCOMMON = "UC"
    RARE = "R"
    SUPER_RARE = "SR"
    SECRET_RARE = "SCR"
    LEADER = "L"
    RARE_CHOICES = [
        (COMMON, "Common"),
        (UNCOMMON, "Uncommon"),
        (RARE, "Rare"),
        (SUPER_RARE, "Super Rare"),
        (SECRET_RARE, "Secret Rare"),
        (LEADER, "Leader"),
    ]

    TYPE_CHOICES = [
        ("Leader", "Leader"),
        ("Character", "Character"),
        ("Stage", "Stage"),
        ("Event", "Event"),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    is_dom = models.BooleanField(default=False)
    cost = models.PositiveIntegerField()
    power = models.PositiveIntegerField()
    counter_value = models.PositiveIntegerField()
    crew = models.ManyToManyField(Crew, related_name="crews")
    effect = models.TextField(blank=True)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    op = models.ForeignKey(Op, on_delete=models.PROTECT)
    deck_color = models.ManyToManyField(DeckColor, related_name="deck_colors")
    rare = models.CharField(max_length=3, choices=RARE_CHOICES)
    trigger = models.CharField(max_length=100, blank=True)
    side_effects = models.ManyToManyField(SideEffect, related_name="side_effects")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def crew_str(self):
        return "/".join([crew.name for crew in self.crew.all()])

    @property
    def has_trigger(self):
        return self.trigger != ""

    @property
    def has_rush(self):
        return self.side_effects.filter(name="Rush").exists()

    @property
    def has_blocker(self):
        return self.side_effects.filter(name="Blocker").exists()

    @property
    def has_alternative_art(self):
        return self.illustrations.filter(is_alternative_art=True).exists()
