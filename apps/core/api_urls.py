from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MoltenBotViewSet, ExecutionViewSet

router = DefaultRouter()
router.register(r'bots', MoltenBotViewSet)
router.register(r'executions', ExecutionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
