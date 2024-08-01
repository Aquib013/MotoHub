from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DeleteView

from svc.forms import JobItemForm
from svc.models import JobItem, Job


class JobItemAddView(CreateView):
    model = JobItem
    form_class = JobItemForm
    template_name = 'job/job_item/add_item.html'

    def form_valid(self, form):
        job_id = self.kwargs['pk']
        job = get_object_or_404(Job, pk=job_id)
        job_item = form.save(commit=False)
        job_item.job = job
        job_item.save()
        messages.success(self.request, f"Item '{job_item.item}' successfully added to Job #{job.job_no}")

        return redirect('job_detail', pk=job_id)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            if field == '__all__':
                for error in errors:
                    messages.error(self.request, f"Error: {error}")
            else:
                for error in errors:
                    messages.error(self.request, f"{field.capitalize()}: {error}")
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['job'] = get_object_or_404(Job, pk=self.kwargs['pk'])
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = get_object_or_404(Job, pk=self.kwargs['pk'])
        return context


class JobItemEditView(UpdateView):
    model = JobItem
    form_class = JobItemForm
    template_name = 'job/job_item/add_item.html'
    context_object_name = 'job_item'

    def form_valid(self, form):
        job_item = form.save()
        messages.success(self.request, f"Item '{job_item.item}' successfully updated for Job #{job_item.job.job_no}")
        return redirect('job_detail', pk=job_item.job.pk)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            if field == '__all__':
                for error in errors:
                    messages.error(self.request, f"Error: {error}")
            else:
                for error in errors:
                    messages.error(self.request, f"{field.capitalize()}: {error}")
        return super().form_invalid(form)

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
