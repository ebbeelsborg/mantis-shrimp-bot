"""
API views for MongoEngine documents.
"""
from rest_framework import status
from rest_framework.viewsets import ViewSet

from core.responses import success_response, error_response
from .models import MantisShrimpBot, Execution
from .serializers import MantisShrimpBotSerializer, ExecutionSerializer


class MantisShrimpBotViewSet(ViewSet):
    """List and retrieve bots."""

    def list(self, request):
        bots = MantisShrimpBot.objects.all()
        serializer = MantisShrimpBotSerializer(bots, many=True)
        return success_response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            bot = MantisShrimpBot.objects.get(id=pk)
        except MantisShrimpBot.DoesNotExist:
            return error_response(
                "Bot not found",
                error_code="NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = MantisShrimpBotSerializer(bot)
        return success_response(serializer.data)


class ExecutionViewSet(ViewSet):
    """List and retrieve executions (read-only)."""

    def list(self, request):
        executions = Execution.objects.all()[:100]
        serializer = ExecutionSerializer(executions, many=True)
        return success_response({"results": serializer.data})

    def retrieve(self, request, pk=None):
        try:
            execution = Execution.objects.get(id=pk)
        except Execution.DoesNotExist:
            return error_response(
                "Execution not found",
                error_code="NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer = ExecutionSerializer(execution)
        return success_response(serializer.data)
