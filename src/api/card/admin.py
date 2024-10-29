import logging
import uuid
from datetime import date

from django.contrib.admin import SimpleListFilter
from django.db.models import Count
from django.urls import reverse

from api.card.models import CardIllustration, Card, Op, DeckColor, Crew, Price
from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms

from api.card.models.card import SideEffect
from api.card.services.exporter import generate_data_cards_for_gemini
from api.card.services.import_card import (
    import_card,
    import_card_illustrations,
)
from api.card.services.update_card import update_illustration_type
from api.core.utils import slugify

logger = logging.getLogger(__name__)


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
            url = reverse("admin:card_cardillustration_change", args=[obj.pk])
            return mark_safe(
                '<a href="{}"><img src="{}" style="max-height: 100px; max-width: 100px;" /></a>'.format(
                    url, obj.src.url
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


class HasThumbnailFilter(SimpleListFilter):
    title = "Has Thumbnail"
    parameter_name = "has_thumbnail"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Yes"),
            ("no", "No"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(src__contains="-")
        if self.value() == "no":
            return queryset.exclude(src__contains="-")
        return queryset


@admin.register(CardIllustration)
class CardIllustrationAdmin(admin.ModelAdmin):
    list_display = ["thumbnail", "code", "card", "art_type", "is_alternative_art"]
    search_fields = ["code", "card__name"]
    list_filter = ["art_type", "is_alternative_art", HasThumbnailFilter]
    fields = [
        "code",
        "thumbnail",
        "src",
        "art_type",
        "is_alternative_art",
        "card",
        "external_link",
        "visual_description",
    ]

    readonly_fields = ("code", "thumbnail")

    actions = [
        "update_price",
        "update_illustration_type_action",
        "export_as_json_for_gemini",
    ]

    def thumbnail(self, obj):
        if obj.src:
            return mark_safe(
                '<img src="{}" style="max-height: 200px; max-width: 200px;" />'.format(
                    obj.src.url
                )
            )
        return "-"

    thumbnail.short_description = "Thumbnail"

    def update_price(self, request, queryset):
        from api.card.services.update_price import update_card_price

        for illustration in queryset:
            try:
                illustration_price = update_card_price(illustration)
                self.message_user(
                    request,
                    f"Price for {illustration} updated to {illustration_price}",
                    level="SUCCESS",
                )
            except Exception as e:
                raise e

    update_price.short_description = "Update Price"

    def update_illustration_type_action(self, request, queryset):
        update_illustration_type()

    update_illustration_type_action.short_description = "Update Illustration Type"

    def export_as_json_for_gemini(self, request, queryset):
        generate_data_cards_for_gemini()

    export_as_json_for_gemini.short_description = "Export as JSON for Gemini"


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


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "crews",
        "colors",
        "op",
        "is_dom",
        "type",
        "illustrations_count",
    ]
    inlines = [CardIllustrationInline]
    search_fields = ["name", "slug"]
    list_filter = ["op", "is_dom", "deck_color", "type"]

    readonly_fields = ("slug",)

    form = CardForm
    actions = [
        "import_cards_action",
        "import_cards_illustrations_action",
        "update_card_effects_action",
    ]

    def import_cards_action(self, request, queryset):
        import_card()

    import_cards_action.short_description = "Import Cards"

    def import_cards_illustrations_action(self, request, queryset):
        import_card_illustrations()

    import_cards_illustrations_action.short_description = "Import Cards Illustrations"

    def update_card_effects_action(self, request, queryset):
        from api.card.services.update_card import update_card_effects

        update_card_effects()

    update_card_effects_action.short_description = "Update Card Effects"

    def crews(self, obj):
        return "/".join([crew.name for crew in obj.crew.all()])

    crews.short_description = "Crews"

    def colors(self, obj):
        return "/".join([color.name for color in obj.deck_color.all()])

    colors.short_description = "Colors"

    # Adicione o campo que calcula a contagem de ilustrações
    def illustrations_count(self, obj):
        return obj.illustrations_count

    illustrations_count.short_description = "Number of Illustrations"
    illustrations_count.admin_order_field = (
        "illustrations_count"  # Permite ordenar por essa coluna
    )

    # Modifique o queryset para incluir a contagem de ilustrações
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(illustrations_count=Count("illustrations"))


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


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ["price", "date", "card_illustration"]
    readonly_fields = ["date", "card_illustration", "price"]
    search_fields = ["card_illustration__code"]
    list_filter = ["date", "card_illustration__card__op__name"]
