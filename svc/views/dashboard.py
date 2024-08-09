from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView
from svc.views.insights import get_daily_insights


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()

        # Get insights
        insights = get_daily_insights(today)

        # Update context with insights
        context.update(insights)
        context['today'] = timezone.now()

        return context
