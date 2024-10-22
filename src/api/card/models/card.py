from django.db import models

from api.core.models import AbstractImage
from api.core.models.base_model import BaseModel
from api.core.utils import slugify


class Op(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def to_json(self):
        return {"name": self.name, "slug": self.slug}

    def __str__(self):
        return self.name


class DeckColor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def to_json(self):
        return {"name": self.name}


class Crew(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def to_json(self):
        return {"name": self.name}

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class SideEffect(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def to_json(self):
        return {"name": self.name, "slug": self.slug}

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Atribute(AbstractImage):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    logo = models.ImageField(upload_to="atributes")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def to_json(self):
        return {
            "name": self.name,
            "slug": self.slug,
            "logo_url": self.logo.url,
        }


class Card(BaseModel):
    # rare choices
    COMMON = "C"
    UNCOMMON = "UC"
    RARE = "R"
    SUPER_RARE = "SR"
    SECRET_RARE = "SCR"
    LEADER = "L"
    SPECIAL_CARD = "SP CARD"
    SEC = "SEC"
    RARE_CHOICES = [
        (COMMON, "Common"),
        (UNCOMMON, "Uncommon"),
        (RARE, "Rare"),
        (SUPER_RARE, "Super Rare"),
        (SECRET_RARE, "Secret Rare"),
        (LEADER, "Leader"),
        (SPECIAL_CARD, "Special Card"),
        (SEC, "SEC"),
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
    rare = models.CharField(max_length=7, choices=RARE_CHOICES)
    trigger = models.CharField(max_length=100, null=True, blank=True)
    side_effects = models.ManyToManyField(SideEffect, related_name="side_effects")
    attribute = models.ForeignKey(
        Atribute,
        on_delete=models.PROTECT,
        related_name="atributes",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def to_json(self):
        return {
            "name": self.name,
            "slug": self.slug,
            "is_dom": self.is_dom,
            "cost": self.cost,
            "power": self.power,
            "counter_value": self.counter_value,
            "crew": [crew.to_json() for crew in self.crew.all()],
            "effect": self.effect,
            "type": self.type,
            "op": self.op.to_json(),
            "deck_color": [
                deck_color.to_json() for deck_color in self.deck_color.all()
            ],
            "rare": self.rare,
            "trigger": self.trigger,
            "side_effects": [
                side_effect.to_json() for side_effect in self.side_effects.all()
            ],
            "attribute": self.attribute.to_json() if self.attribute else None,
        }

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
