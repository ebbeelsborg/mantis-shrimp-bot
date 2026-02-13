from django.contrib import admin
from django.utils.html import format_html
from .models import Organization, MoltenBot, Execution
from .tasks import reheat_bots_task

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')

@admin.action(description='Shut down selected bots (Direct)')
def shutdown_bots(modeladmin, request, queryset):
    queryset.update(status='OFFLINE')

@admin.action(description='Reheat selected bots (+100C) [Async]')
def reheat_bots(modeladmin, request, queryset):
    # Pass IDs to Celery, not objects
    bot_ids = list(queryset.values_list('id', flat=True))
    reheat_bots_task.delay(bot_ids)
    modeladmin.message_user(request, f"Started background job to reheat {len(bot_ids)} bots.")

@admin.register(MoltenBot)
class MoltenBotAdmin(admin.ModelAdmin):
    list_display = ('name', 'colored_temperature', 'status', 'organization')
    list_filter = ('status', 'organization')
    actions = [shutdown_bots, reheat_bots]

    def colored_temperature(self, obj):
        color = 'blue'
        if obj.temperature > 500:
            color = 'orange'
        if obj.temperature > 800:
            color = 'red'
        return format_html('<span style="color: {}; font-weight: bold;">{}°C</span>', color, obj.temperature)
    colored_temperature.short_description = 'Core Temp'

@admin.register(Execution)
class ExecutionAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'bot', 'started_at', 'success')
