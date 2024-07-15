from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView, DeleteView

from svc.forms import ServiceForm
from svc.models import Service, Job


class ServiceCreateView(FormView):
    model = Service
    form_class = ServiceForm
    template_name = 'services/service_form.html'

    def form_valid(self, form):
        job_id = self.kwargs['pk']
        job = get_object_or_404(Job, pk=job_id)
        service = form.save(commit=False)
        service.job = job
        service.save()
        return redirect('job_detail', pk=job_id)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['job'] = get_object_or_404(Job, pk=self.kwargs['pk'])
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = get_object_or_404(Job, pk=self.kwargs['pk'])
        return context


class ServiceUpdateView(UpdateView):
    model = Service
    fields = ["name", "service_type", "vehicle", "total_run", "unit_service_cost"]
    template_name = 'services/edit_service.html'

    def get_success_url(self):
        return reverse_lazy('job_detail', kwargs={'pk': self.object.job.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = self.object.job
        return context


class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'services/service_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('job_detail', kwargs={'pk': self.object.job.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = self.object.job
        return context
