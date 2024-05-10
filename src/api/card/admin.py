from api.card.models import CardImage, Card, Type
from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms


class CardImageForm(forms.ModelForm):
    class Meta:
        model = CardImage
        fields = "__all__"
        widgets = {
            "tags": forms.CheckboxSelectMultiple(),
        }


class CardImageInline(admin.TabularInline):
    model = CardImage
    extra = 0
    readonly_fields = ("image_preview",)
    form = CardImageForm

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
        return ((None, {"fields": ("image_preview", "src", "tag")}),)


class CardImageAdmin(admin.ModelAdmin):
    list_display = ["card", "tag"]
    search_fields = ["card", "tag"]


admin.site.register(CardImage, CardImageAdmin)


class CardAdmin(admin.ModelAdmin):
    list_display = ["name", "crews", "created_at", "updated_at"]
    inlines = [CardImageInline]
    search_fields = ["name", "description"]
    list_filter = ["op", "is_dom", "deck_color", "type"]

    def crews(self, obj):
        print(obj.crew.all())
        return "/".join([crew.name for crew in obj.crew.all()])

    crews.short_description = "Crews"


admin.site.register(Card, CardAdmin)


class TypeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


admin.site.register(Type, TypeAdmin)
