"""
Custom AdminSite that adds MongoEngine document admin URLs.
"""
from django.contrib import admin
from django.urls import path

from apps.core.admin import (
    organization_changelist,
    mantis_shrimp_bot_changelist,
    execution_changelist,
)


class MantisShrimpBotAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path("core/organization/", self.admin_view(organization_changelist), name="organization_changelist"),
            path("core/mantis_shrimp_bot/", self.admin_view(mantis_shrimp_bot_changelist), name="mantis_shrimp_bot_changelist"),
            path("core/execution/", self.admin_view(execution_changelist), name="execution_changelist"),
        ]
        return custom + urls


site = MantisShrimpBotAdminSite()

# Register Django's built-in models (User, Group) with our site
from django.contrib.auth.models import User, Group
site.register(User, admin.ModelAdmin)
site.register(Group, admin.ModelAdmin)
