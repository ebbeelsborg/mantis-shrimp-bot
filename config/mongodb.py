"""
MongoDB connection setup for MongoEngine.
Called from Django's AppConfig.ready().
"""
from django.conf import settings
import mongoengine


def connect_mongodb():
    """Connect MongoEngine to MongoDB. Idempotent for same alias."""
    mongoengine.connect(
        db=settings.MONGODB_NAME,
        host=settings.MONGODB_HOST,
        alias="default",
    )
