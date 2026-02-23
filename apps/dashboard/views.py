from django.http import Http404
from django.views.generic import TemplateView

from apps.core.models import MantisShrimpBot, Execution


class DashboardView(TemplateView):
    template_name = "dashboard.html"


class BotDetailView(TemplateView):
    template_name = "bot_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            bot = MantisShrimpBot.objects.get(id=kwargs["bot_id"])
        except (MantisShrimpBot.DoesNotExist, Exception):
            raise Http404("Bot not found")
        executions = Execution.objects(bot=bot).order_by("-started_at")[:100]
        total = len(executions)
        success_count = sum(1 for e in executions if e.success)
        success_rate = (success_count / total * 100) if total > 0 else 0
        context["bot"] = bot
        context["executions"] = executions
        context["success_rate"] = round(success_rate, 1)
        context["total_tasks"] = total
        context["success_count"] = success_count
        return context
