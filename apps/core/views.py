"""
API views for MongoEngine documents.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import MantisShrimpBot, Execution
from .serializers import MantisShrimpBotSerializer, ExecutionSerializer


class MantisShrimpBotViewSet(viewsets.ViewSet):
    """List and retrieve bots."""

    def list(self, request):
        bots = MantisShrimpBot.objects.all()
        serializer = MantisShrimpBotSerializer(bots, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            bot = MantisShrimpBot.objects.get(id=pk)
        except MantisShrimpBot.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MantisShrimpBotSerializer(bot)
        return Response(serializer.data)


class ExecutionViewSet(viewsets.ViewSet):
    """List and retrieve executions (read-only)."""

    def list(self, request):
        executions = Execution.objects.all()[:100]
        serializer = ExecutionSerializer(executions, many=True)
        return Response({"results": serializer.data})

    def retrieve(self, request, pk=None):
        try:
            execution = Execution.objects.get(id=pk)
        except Execution.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ExecutionSerializer(execution)
        return Response(serializer.data)
