"""
Django settings. Loads base + environment-specific settings.
Set DJANGO_ENV to 'development', 'staging', or 'production'.
"""
import os

from .base import *

env_name = os.environ.get("DJANGO_ENV", "development")
if env_name == "production":
    from .production import *  # noqa: F401, F403
elif env_name == "staging":
    from .staging import *  # noqa: F401, F403
else:
    from .development import *  # noqa: F401, F403
