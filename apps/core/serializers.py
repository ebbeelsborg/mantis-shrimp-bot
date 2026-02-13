from rest_framework import serializers
from .models import MoltenBot, Execution

class MoltenBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoltenBot
        fields = '__all__'

class ExecutionSerializer(serializers.ModelSerializer):
    bot_name = serializers.CharField(source='bot.name', read_only=True)
    
    class Meta:
        model = Execution
        fields = ['id', 'bot_name', 'task_name', 'started_at', 'success']
