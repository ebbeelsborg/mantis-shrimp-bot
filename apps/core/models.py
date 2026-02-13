from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_temperature(value):
    if value > 1000:
        raise ValidationError(f"Temperature {value}°C is too high! Bot will melt.")

class Organization(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class MoltenBot(models.Model):
    STATUS_CHOICES = [
        ('ONLINE', 'Online'),
        ('OFFLINE', 'Offline'),
        ('MELTDOWN', 'Meltdown'),
    ]

    name = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='bots')
    model_version = models.CharField(max_length=50, default="v1.0")
    temperature = models.FloatField(validators=[validate_temperature], help_text="Core temperature in Celsius. Max 1000°C.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ONLINE')
    formatted_status = models.CharField(max_length=100, blank=True) # To showcase signals or save overrides

    def save(self, *args, **kwargs):
        if self.temperature >= 1000:
            self.status = 'MELTDOWN'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.temperature}°C)"

class Execution(models.Model):
    bot = models.ForeignKey(MoltenBot, on_delete=models.CASCADE, related_name='executions')
    task_name = models.CharField(max_length=200)
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    success = models.BooleanField(default=True)

    class Meta:
        ordering = ['-started_at']
