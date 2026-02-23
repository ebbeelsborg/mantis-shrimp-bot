"""
Main API v1 URL configuration.
"""
from django.urls import path, include

urlpatterns = [
    path("", include("apps.core.api_urls")),
]
