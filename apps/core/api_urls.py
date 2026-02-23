from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MantisShrimpBotViewSet, ExecutionViewSet

router = DefaultRouter()
router.register(r'bots', MantisShrimpBotViewSet, basename='bot')
router.register(r'executions', ExecutionViewSet, basename='execution')

urlpatterns = [
    path('', include(router.urls)),
]
