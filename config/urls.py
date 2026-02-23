from django.urls import path, include

from config.admin_site import site

urlpatterns = [
    path("admin/", site.urls),
    path('', include('apps.dashboard.urls')),
    path('api/', include('apps.core.api_urls')),
]
