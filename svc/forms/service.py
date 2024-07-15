from django import forms

from svc.models import Service, Job


class ServiceForm(forms.ModelForm):
    job_hidden = forms.CharField(widget=forms.HiddenInput(), required=True)

    class Meta:
        model = Service
        fields = ["name", "service_type", "vehicle", "total_run", "quantity", "unit_service_cost"]

    def __init__(self, *args, **kwargs):
        job = kwargs.pop('job', None)
        super().__init__(*args, **kwargs)
        if job:
            self.fields['job_hidden'].initial = job.pk   # NOQA
            self.fields['job'] = forms.CharField(initial=job, disabled=True, required=False)
            self.fields['job'].label = 'Job'
