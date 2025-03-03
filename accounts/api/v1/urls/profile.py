from django.urls import path, include
from .. import views
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("", views.ProfileView.as_view(), name="profile"),
]
