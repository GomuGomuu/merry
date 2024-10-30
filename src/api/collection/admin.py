from django.contrib import admin
from django.db.models import Subquery, Min, Count
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.utils.html import format_html
from django.shortcuts import redirect
from django.middleware.csrf import get_token

from api.collection.models import CollectionIllustration, Collection


@admin.register(CollectionIllustration)
class CollectionIllustrationAdmin(admin.ModelAdmin):
    search_fields = ["collection", "illustration__name"]
    list_display = ["collection", "illustration"]
    fields = ["collection", "illustration"]


class IllustrationInline(admin.TabularInline):
    model = CollectionIllustration
    extra = 0
    can_delete = False
    readonly_fields = [
        "thumbnail",
        "illustration",
        "quantity_buttons",
    ]

    def __init__(self, *args, **kwargs):
        self.request = None
        super().__init__(*args, **kwargs)

    def get_queryset(self, request):
        self.request = request
        qs = super().get_queryset(request)

        first_illustration_ids = CollectionIllustration.objects.values(
            "illustration"
        ).annotate(first_id=Min("id"))

        filtered_qs = qs.filter(
            id__in=Subquery(first_illustration_ids.values("first_id"))
        ).annotate(illustration_count=Count("illustration"))

        return filtered_qs

    def illustration(self, obj):
        return obj.illustration

    illustration.short_description = "Illustration"

    def illustration_count_display(self, obj):
        illustration_count = CollectionIllustration.objects.filter(
            collection=obj.collection, illustration=obj.illustration
        ).count()
        return illustration_count

    def thumbnail(self, obj):
        if obj.illustration.src:
            return mark_safe(
                '<img src="{}" style="max-height: 80px; max-width: 80px;" />'.format(
                    obj.illustration.src.url
                )
            )
        return "-"

    thumbnail.short_description = "Thumbnail"

    def quantity_buttons(self, obj):
        illustration_count = self.illustration_count_display(obj)
        csrf_token = get_token(self.request)

        hidden_fields = f"""
            <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}" />
            <input type="hidden" name="illustration_id" value="{obj.illustration.id}" />
            <input type="hidden" name="collection_id" value="{obj.collection.id}" />
        """

        return format_html(
            f"""
            <div id="quantity-buttons">
                <div style="display: flex; align-items: center;">
                    <form action="{reverse('admin:collection_collection_changelist')}" method="post" style="display:inline;">
                        {hidden_fields}
                        <input type="hidden" name="action" value="add" />
                        <button type="submit">+</button>
                    </form>
                    <span style="margin: 0 10px;">{illustration_count}</span>
                    <form action="{reverse('admin:collection_collection_changelist')}" method="post" style="display:inline;">
                        {hidden_fields}
                        <input type="hidden" name="action" value="remove" />
                        <button type="submit">-</button>
                    </form>
                </div>
            </div>
            """
        )

    quantity_buttons.short_description = "Quantidade"


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_filter = ["name"]
    search_fields = ["name", "user__name"]
    list_display = ["name", "user", "illustration_count"]
    fields = ["name", "user"]
    inlines = [IllustrationInline]

    def illustration_count(self, obj):
        return CollectionIllustration.objects.filter(collection=obj).count()

    illustration_count.short_description = "Contagem de Ilustrações"

    def changelist_view(self, request, extra_context=None):
        if request.method == "POST":
            action = request.POST.get("action")
            illustration_id = request.POST.get("illustration_id")
            collection_id = request.POST.get("collection_id")

            if action == "add":
                print(
                    f"Adicionando ilustração {illustration_id} à coleção {collection_id}"
                )
                CollectionIllustration.objects.create(
                    collection_id=collection_id, illustration_id=illustration_id
                )
            elif action == "remove":
                print(
                    f"Removendo ilustração {illustration_id} da coleção {collection_id}"
                )
                CollectionIllustration.objects.filter(
                    collection_id=collection_id, illustration_id=illustration_id
                ).last().delete()

            return redirect(request.path)

        return super().changelist_view(request, extra_context=extra_context)
