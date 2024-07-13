from django.views.generic import (
    CreateView,
    ListView,
    DeleteView,
    UpdateView,
    DetailView,
)

from django.urls import reverse_lazy
from svc.models import Job, Service
from svc.forms import JobForm


class JobCreateView(CreateView):
    model = Job
    form_class = JobForm
    template_name = "job/job_form.html"
    success_url = reverse_lazy("jobs")


class JobListView(ListView):
    model = Job
    template_name = "job/jobs.html"
    context_object_name = "jobs"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        jobs = context['jobs']
        context['show_completion_time'] = any(job.status == "Completed" for job in jobs)
        return context


class JobDetailView(DetailView):
    model = Job
    template_name = "job/job_detail.html"
    context_object_name = "job"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.filter(job=self.get_object())
        return context


class JobUpdateView(UpdateView):
    model = Job
    form_class = JobForm
    template_name = "job/job_edit.html"

    def get_success_url(self):
        return reverse_lazy('job_detail', kwargs={'pk': self.object.pk})


class JobDeleteView(DeleteView):
    model = Job
    template_name = "job/job_delete.html"
    success_url = reverse_lazy("jobs")
