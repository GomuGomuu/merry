from django.urls import path

from . import views

app_name = "project"

urlpatterns = [path("test/", views.project_test, name="project_test")]
