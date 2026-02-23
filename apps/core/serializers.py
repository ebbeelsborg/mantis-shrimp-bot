"""
Serializers for MongoEngine documents (API responses).
"""
from rest_framework import serializers
from .models import MantisShrimpBot, Execution


class MantisShrimpBotSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    name = serializers.CharField()
    organization = serializers.SerializerMethodField()
    model_version = serializers.CharField()
    temperature = serializers.FloatField()
    status = serializers.CharField()
    formatted_status = serializers.CharField()

    def get_id(self, obj):
        return str(obj.id)

    def get_organization(self, obj):
        return str(obj.organization.name) if obj.organization else None


class ExecutionSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    bot_name = serializers.SerializerMethodField()
    task_name = serializers.CharField()
    started_at = serializers.DateTimeField()
    success = serializers.BooleanField()

    def get_id(self, obj):
        return str(obj.id)

    def get_bot_name(self, obj):
        return obj.bot.name if obj.bot else None
