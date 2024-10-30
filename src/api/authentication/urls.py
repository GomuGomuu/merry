from django.urls import path

from . import views

app_name = "authentication"

urlpatterns = [
    path("users/", views.list_users, name="list_users"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("token/refresh/", views.RefreshTokenView.as_view(), name="token_refresh"),
]
