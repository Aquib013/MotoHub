from django.utils import timezone
from django.views.generic import TemplateView
from svc.views.insights import get_insights


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        period = self.request.GET.get('period', 'daily')
        selected_date = self.request.GET.get('date')

        if selected_date:
            selected_date = timezone.datetime.strptime(selected_date, "%Y-%m-%d").date()
        else:
            selected_date = timezone.now().date()

        # Get insights
        insights = get_insights(selected_date, period)

        # Update context with insights
        context.update(insights)
        context['today'] = timezone.now()
        context['selected_date'] = selected_date
        context['period'] = period

        return context
