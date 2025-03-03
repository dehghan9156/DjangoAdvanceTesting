from django.urls import path, include
from .. import views
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from ..views import RegistrationApiView

from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    path("register/", views.RegistrationApiView.as_view(), name="register"),
    path("token/login/", views.TokenLoginApiView.as_view(), name="token_login"),
    path("token/logout/", views.TokenLogoutApiView.as_view(), name="token_logout"),
    path("jwt/create/", views.CustomTokenObtainPairView.as_view(), name="token_create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path(
        "change-password/", views.ChangePasswordView.as_view(), name="change_password"
    ),
    path("send_email/", views.SendEmailView.as_view(), name="send_email"),
    path(
        "confirm-user/<str:token>/",
        views.ConfirmUserView.as_view(),
        name="confirm-user",
    ),
]
