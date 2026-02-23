"""
Custom admin for MongoEngine documents.
Uses Django admin styling and login.
"""
from bson import ObjectId
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.urls import path, reverse
from django.contrib import messages

from .models import Organization, MantisShrimpBot, Execution
from .tasks import reheat_bots_task


@staff_member_required
def organization_changelist(request):
    orgs = Organization.objects.all()
    return render(
        request,
        "admin/core/organization_changelist.html",
        {"organizations": orgs, "title": "Organizations"},
    )


@staff_member_required
def mantis_shrimp_bot_changelist(request):
    bots = MantisShrimpBot.objects.all()
    if request.method == "POST":
        action = request.POST.get("action")
        selected = request.POST.getlist("_selected_action")
        if action == "shutdown_bots" and selected:
            ids = [ObjectId(oid) for oid in selected]
            MantisShrimpBot.objects(id__in=ids).update(set__status="OFFLINE")
            messages.success(request, f"Shut down {len(selected)} bot(s).")
            return redirect("admin:mantis_shrimp_bot_changelist")
        if action == "reheat_bots" and selected:
            reheat_bots_task.delay(selected)
            messages.success(request, f"Started background job to reheat {len(selected)} bot(s).")
            return redirect("admin:mantis_shrimp_bot_changelist")
    return render(
        request,
        "admin/core/mantis_shrimp_bot_changelist.html",
        {"bots": bots, "title": "Mantis Shrimp Bots"},
    )


@staff_member_required
def execution_changelist(request):
    executions = Execution.objects.all()[:200]
    return render(
        request,
        "admin/core/execution_changelist.html",
        {"executions": executions, "title": "Executions"},
    )


def get_admin_urls():
    return [
        path("core/organization/", organization_changelist, name="organization_changelist"),
        path("core/mantis_shrimp_bot/", mantis_shrimp_bot_changelist, name="mantis_shrimp_bot_changelist"),
        path("core/execution/", execution_changelist, name="execution_changelist"),
    ]
