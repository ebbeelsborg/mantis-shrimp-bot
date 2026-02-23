from django.urls import path
from .views import DashboardView, BotDetailView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('bots/<str:bot_id>/', BotDetailView.as_view(), name='bot_detail'),
]
