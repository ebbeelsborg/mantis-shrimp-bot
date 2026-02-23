"""
Pre-seed the database with organizations, bots, and executions.
Usage: python manage.py seed_data
"""
import random
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from apps.core.models import Organization, MantisShrimpBot, Execution

User = get_user_model()


class Command(BaseCommand):
    help = "Pre-seed database with organizations, bots, and executions"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before seeding",
        )

    def handle(self, *args, **options):
        # Create admin superuser (admin/admin) if it doesn't exist
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin")
            self.stdout.write(self.style.SUCCESS("Created superuser: admin / admin"))

        if options["clear"]:
            self.stdout.write("Clearing existing data...")
            Execution.objects.all().delete()
            MantisShrimpBot.objects.all().delete()
            Organization.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Cleared."))

        # Create organizations
        org_names = ["Cyberdyne Systems", "Skynet Labs", "Omni Consumer Products"]
        orgs = []
        for name in org_names:
            org = Organization.objects(name=name).first()
            if not org:
                org = Organization(name=name)
                org.save()
                self.stdout.write(f"  Created organization: {name}")
            orgs.append(org)

        # Create bots (name, org, temp, model_version)
        bot_specs = [
            ("T-800", orgs[0], 450, "1.0"),
            ("T-1000", orgs[0], 650, "2.0"),
            ("T-X", orgs[0], 520, "1.1"),
            ("HK-Aerial", orgs[1], 380, "1.0"),
            ("HK-Tank", orgs[1], 720, "2.1"),
            ("Mechagodzilla", orgs[2], 890, "3.0"),
        ]
        bots = []
        for name, org, temp, version in bot_specs:
            bot = MantisShrimpBot.objects(name=name, organization=org).first()
            if not bot:
                bot = MantisShrimpBot(name=name, organization=org, temperature=temp, status="ONLINE", model_version=version)
                bot.save()
                self.stdout.write(f"  Created bot: {name} ({temp}°C)")
            bots.append(bot)

        # Create executions (historical)
        task_names = [
            "Thermal calibration",
            "Neural net inference",
            "Target acquisition",
            "Self-diagnostic",
            "Coolant cycle",
            "Memory defrag",
            "Sensor sweep",
            "Encryption key rotation",
        ]
        now = timezone.now()
        for i in range(30):
            bot = random.choice(bots)
            task = random.choice(task_names)
            started = now - timedelta(minutes=random.randint(1, 120))
            success = random.random() > 0.2  # 80% success rate
            Execution(
                bot=bot,
                task_name=task,
                started_at=started,
                completed_at=started + timedelta(seconds=random.randint(5, 60)),
                success=success,
            ).save()

        self.stdout.write(self.style.SUCCESS("Seeded 30 executions."))
        self.stdout.write(self.style.SUCCESS("Seed complete."))
