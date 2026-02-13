from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Organization, MoltenBot

class MoltenBotTestCase(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name="DeepMind")

    def test_bot_creation(self):
        """Test that a bot can be created with valid data."""
        bot = MoltenBot.objects.create(
            name="Sparky",
            organization=self.org,
            temperature=500.0
        )
        self.assertEqual(bot.status, 'ONLINE')

    def test_temperature_validation(self):
        """Test that a bot cannot be created with temperature > 1000."""
        bot = MoltenBot(
            name="Melty",
            organization=self.org,
            temperature=1500.0
        )
        with self.assertRaises(ValidationError):
            bot.full_clean()

    def test_meltdown_status(self):
        """Test that saving a bot with temp >= 1000 sets status to MELTDOWN."""
        # Note: validators run on clean(), save() logic runs on save().
        # We bypass clean() here to test the save() override logic specifically.
        bot = MoltenBot.objects.create(
            name="TooHot",
            organization=self.org,
            temperature=1000.0
        )
        self.assertEqual(bot.status, 'MELTDOWN')

    def test_reheat_action(self):
        """Test the reheat logic (simulated)."""
        bot = MoltenBot.objects.create(
            name="Chilly",
            organization=self.org,
            temperature=100.0
        )
        bot.temperature += 100
        bot.save()
        self.assertEqual(bot.temperature, 200.0)

    def test_reheat_task(self):
        """Test the background task logic directly."""
        from .tasks import reheat_bots_task
        
        bot1 = MoltenBot.objects.create(name="B1", organization=self.org, temperature=100.0)
        bot2 = MoltenBot.objects.create(name="B2", organization=self.org, temperature=800.0)
        
        # Call the task function directly (synchronously)
        result = reheat_bots_task([bot1.id, bot2.id])
        
        bot1.refresh_from_db()
        bot2.refresh_from_db()
        
        self.assertEqual(bot1.temperature, 200.0)
        self.assertEqual(bot2.temperature, 900.0)
        self.assertIn("Reheated 2 bots", result)
