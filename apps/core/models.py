"""
MongoEngine documents for Mantis Shrimp Bot (NoSQL).
"""
from mongoengine import (
    Document,
    StringField,
    FloatField,
    DateTimeField,
    BooleanField,
    ReferenceField,
)
from mongoengine.errors import ValidationError
from django.utils import timezone


def validate_temperature(value):
    if value > 1000:
        raise ValidationError(f"Temperature {value}°C is too high! Bot will melt.")


class Organization(Document):
    name = StringField(max_length=100, required=True)
    created_at = DateTimeField(default=timezone.now)

    meta = {"collection": "organizations"}

    def __str__(self):
        return self.name


class MantisShrimpBot(Document):
    STATUS_CHOICES = ("ONLINE", "OFFLINE", "MELTDOWN")
    STATUS_DISPLAY = {
        "ONLINE": "Online",
        "OFFLINE": "Offline",
        "MELTDOWN": "Meltdown",
    }

    name = StringField(max_length=100, required=True)
    organization = ReferenceField(Organization, reverse_delete_rule=2)  # CASCADE
    model_version = StringField(max_length=50, default="1.0")
    temperature = FloatField(help_text="Core temperature in Celsius. Max 1000°C.")
    status = StringField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ONLINE",
    )
    formatted_status = StringField(max_length=100, blank=True)

    meta = {"collection": "mantis_shrimp_bots", "ordering": ["name"]}

    def clean(self):
        validate_temperature(self.temperature)

    def save(self, *args, **kwargs):
        if self.temperature >= 1000:
            self.status = "MELTDOWN"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.temperature}°C)"


class Execution(Document):
    bot = ReferenceField(MantisShrimpBot, reverse_delete_rule=2)  # CASCADE
    task_name = StringField(max_length=200, required=True)
    started_at = DateTimeField(default=timezone.now)
    completed_at = DateTimeField(null=True)
    success = BooleanField(default=True)

    meta = {"collection": "executions", "ordering": ["-started_at"]}
