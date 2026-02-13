from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import MoltenBot, Execution
from .serializers import MoltenBotSerializer, ExecutionSerializer

class MoltenBotViewSet(viewsets.ModelViewSet):
    queryset = MoltenBot.objects.all()
    serializer_class = MoltenBotSerializer

class ExecutionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Execution.objects.all()
    serializer_class = ExecutionSerializer
