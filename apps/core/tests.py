from django.test import TestCase
from mongoengine.errors import ValidationError

from .models import Organization, MantisShrimpBot


class MantisShrimpBotTestCase(TestCase):
    def setUp(self):
        self.org = Organization(name="DeepMind")
        self.org.save()

    def test_bot_creation(self):
        """Test that a bot can be created with valid data."""
        bot = MantisShrimpBot(
            name="Sparky",
            organization=self.org,
            temperature=500.0,
        )
        bot.save()
        self.assertEqual(bot.status, "ONLINE")

    def test_temperature_validation(self):
        """Test that a bot cannot be created with temperature > 1000."""
        bot = MantisShrimpBot(
            name="Melty",
            organization=self.org,
            temperature=1500.0,
        )
        with self.assertRaises(ValidationError):
            bot.clean()
            bot.save()

    def test_meltdown_status(self):
        """Test that saving a bot with temp >= 1000 sets status to MELTDOWN."""
        bot = MantisShrimpBot(
            name="TooHot",
            organization=self.org,
            temperature=1000.0,
        )
        bot.save()
        self.assertEqual(bot.status, "MELTDOWN")

    def test_reheat_action(self):
        """Test the reheat logic (simulated)."""
        bot = MantisShrimpBot(
            name="Chilly",
            organization=self.org,
            temperature=100.0,
        )
        bot.save()
        bot.temperature += 100
        bot.save()
        bot.reload()
        self.assertEqual(bot.temperature, 200.0)

    def test_reheat_task(self):
        """Test the background task logic directly."""
        from .tasks import reheat_bots_task

        bot1 = MantisShrimpBot(name="B1", organization=self.org, temperature=100.0)
        bot1.save()
        bot2 = MantisShrimpBot(name="B2", organization=self.org, temperature=800.0)
        bot2.save()

        result = reheat_bots_task([str(bot1.id), str(bot2.id)])

        bot1.reload()
        bot2.reload()
        self.assertEqual(bot1.temperature, 200.0)
        self.assertEqual(bot2.temperature, 900.0)
        self.assertIn("Reheated 2 bots", result)
