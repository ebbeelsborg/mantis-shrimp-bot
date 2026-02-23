import random
from bson import ObjectId
from celery import shared_task
from django.utils import timezone

from .models import MantisShrimpBot, Execution


TASK_NAMES = [
    "Thermal calibration",
    "Neural net inference",
    "Target acquisition",
    "Self-diagnostic",
    "Coolant cycle",
    "Memory defrag",
    "Sensor sweep",
    "Encryption key rotation",
    "Payload encryption",
    "Threat assessment",
]


@shared_task
def create_and_process_task():
    """
    Auto-create a new task, have a random online bot pick it up and finish it
    with random success or failure. Runs every 3 seconds via Celery Beat.
    """
    online_bots = list(MantisShrimpBot.objects(status="ONLINE"))
    if not online_bots:
        return "No online bots available"

    bot = random.choice(online_bots)
    task_name = random.choice(TASK_NAMES)
    success = random.random() > 0.3  # 70% success rate

    started_at = timezone.now()
    Execution(
        bot=bot,
        task_name=task_name,
        started_at=started_at,
        completed_at=started_at,  # Instant completion for demo
        success=success,
    ).save()
    return f"Bot {bot.name} completed '{task_name}' ({'OK' if success else 'FAIL'})"


@shared_task
def reheat_bots_task(bot_ids):
    """
    Background task to reheat a list of bots.
    This avoids blocking the web server when processing thousands of bots.
    """
    object_ids = [ObjectId(oid) for oid in bot_ids]
    bots = list(MantisShrimpBot.objects(id__in=object_ids))
    updated_count = 0
    
    for bot in bots:
        # Business logic: Increase temp by 100, capped at 1000
        # We fetch and save individually to ensure the 'save()' method logic (meltdown check) runs.
        # For pure speed, we could use bulk_update, but we want the meltdown logic to trigger.
        bot.temperature = min(1000, bot.temperature + 100)
        bot.save()
        updated_count += 1
    
    return f"Reheated {updated_count} bots."
