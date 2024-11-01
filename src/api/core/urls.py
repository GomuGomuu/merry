from django.contrib import admin
from django.urls import include, path
from . import views
from django.conf.urls.static import static
from api.authentication import urls as authentication_urls
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings

urlpatterns = [
    path("health_check/", views.health_check, name="health_check"),
    path("ping/", views.ping, name="ping"),
    path("admin/", admin.site.urls),
    path("auth/", include(authentication_urls)),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("docs/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("cards/", include("api.card.urls")),
    path("exchange/", include("api.exchange.urls")),
    path("recognition/", include("api.recognition.urls")),
    path("collection/", include("api.collection.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
