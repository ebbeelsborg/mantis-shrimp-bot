from django.urls import path, include

from config.admin_site import site

urlpatterns = [
    path("admin/", site.urls),
    path("", include("apps.dashboard.urls")),
    path("api/v1/", include("api.v1.urls")),
]
