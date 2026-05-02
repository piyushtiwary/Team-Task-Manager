from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    SignupView,
    LoginView,
    MeView,
)

urlpatterns = [
    # API endpoints (under /api/auth/)
    path("signup/", SignupView.as_view(), name="api-signup"),
    path("login/", LoginView.as_view(), name="api-login"),
    path("me/", MeView.as_view(), name="api-me"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
