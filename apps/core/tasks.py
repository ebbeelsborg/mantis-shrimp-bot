from celery import shared_task
from .models import MoltenBot

@shared_task
def reheat_bots_task(bot_ids):
    """
    Background task to reheat a list of bots.
    This avoids blocking the web server when processing thousands of bots.
    """
    bots = MoltenBot.objects.filter(id__in=bot_ids)
    updated_count = 0
    
    for bot in bots:
        # Business logic: Increase temp by 100, capped at 1000
        # We fetch and save individually to ensure the 'save()' method logic (meltdown check) runs.
        # For pure speed, we could use bulk_update, but we want the meltdown logic to trigger.
        bot.temperature = min(1000, bot.temperature + 100)
        bot.save()
        updated_count += 1
    
    return f"Reheated {updated_count} bots."
