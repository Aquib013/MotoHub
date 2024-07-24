from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DeleteView

from svc.forms import JobItemForm
from svc.models import JobItem, Job


class JobItemCreateView(CreateView):
    model = JobItem
    form_class = JobItemForm
    template_name = 'job/job_item/add_item.html'

    def form_valid(self, form):
        job_id = self.kwargs['pk']
        job = get_object_or_404(Job, pk=job_id)
        job_item = form.save(commit=False)
        job_item.job = job
        job_item.save()
        return redirect('job_detail', pk=job_id)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['job'] = get_object_or_404(Job, pk=self.kwargs['pk'])
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = get_object_or_404(Job, pk=self.kwargs['pk'])
        return context


class JobItemUpdateView(UpdateView):
    model = JobItem
    fields = ["item", "item_quantity", "item_unit_price"]
    template_name = 'job/job_item/edit_item.html'

    def get_success_url(self):
        return reverse_lazy('job_detail', kwargs={'pk': self.object.job.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = self.object.job
        return context


class JobItemDeleteView(DeleteView):
    model = JobItem
    template_name = 'job/job_item/delete_item.html'

    def get_success_url(self):
        job_id = self.object.job.pk
        return reverse_lazy('job_detail', kwargs={'pk': job_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = self.object.job
        return context
