import uuid
from datetime import date

from api.card.models import CardIllustration, Card, Op, DeckColor, Crew
from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms

from api.card.models.card import SideEffect
from api.core.utils import slugify


class CardIllustrationForm(forms.ModelForm):
    class Meta:
        model = CardIllustration
        fields = "__all__"

    def save(self, commit=True):
        instance = super().save(commit=False)
        image_extension = instance.src.file.content_type.split("/")[-1]
        instance.slug = f"{date.today()}-{uuid.uuid4()}-{slugify(instance.code)}"
        instance.src.name = f"{instance.slug}.{image_extension}"
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class CardIllustrationInline(admin.TabularInline):
    model = CardIllustration
    extra = 0
    readonly_fields = ("image_preview",)
    form = CardIllustrationForm

    def image_preview(self, obj):
        if obj.src:
            return mark_safe(
                '<img src="{}" style="max-height: 100px; max-width: 100px;" />'.format(
                    obj.src.url
                )
            )
        return "-"

    image_preview.short_description = "Image Preview"

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if not obj:
            return fieldsets
        return (
            (
                None,
                {
                    "fields": (
                        "image_preview",
                        "code",
                        "src",
                        "art_type",
                        "is_alternative_art",
                    )
                },
            ),
        )


class CardIllustrationAdmin(admin.ModelAdmin):
    list_display = ["card", "art_type", "is_alternative_art"]
    search_fields = ["card", "art_type", "is_alternative_art"]


admin.site.register(CardIllustration, CardIllustrationAdmin)


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = "__all__"

    # apply slugify to the name field to generate the slug and save it
    prepopulated_fields = {"slug": ("name",)}

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.slug = slugify(instance.name)
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class CardAdmin(admin.ModelAdmin):
    list_display = ["name", "crews", "colors", "op", "is_dom", "type"]
    inlines = [CardIllustrationInline]
    search_fields = ["name", "description"]
    list_filter = ["op", "is_dom", "deck_color", "type"]

    readonly_fields = ("slug",)

    form = CardForm

    def crews(self, obj):
        return "/".join([crew.name for crew in obj.crew.all()])

    crews.short_description = "Crews"

    def colors(self, obj):
        return "/".join([color.name for color in obj.deck_color.all()])

    colors.short_description = "Colors"


admin.site.register(Card, CardAdmin)


@admin.register(Op)
class OpAdmin(admin.ModelAdmin):
    pass


@admin.register(DeckColor)
class DeckColorAdmin(admin.ModelAdmin):
    pass


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    pass


@admin.register(SideEffect)
class SideEffectAdmin(admin.ModelAdmin):
    pass
