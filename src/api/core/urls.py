from django.contrib import admin
from django.urls import include, path
from . import views

from api.authentication import urls as authentication_urls
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("health_check/", views.health_check, name="health_check"),
    path("admin/", admin.site.urls),
    path("auth/", include(authentication_urls)),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("docs/schema/", SpectacularAPIView.as_view(), name="schema"),
]
