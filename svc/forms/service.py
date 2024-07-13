from django import forms

from svc.models import Service, Job


#
#
# class ServiceForm(forms.ModelForm):
#     class Meta:
#         model = Service
#         fields = ["job", "name", "service_type", "vehicle", "cost"]
#
#     def __init__(self, *args, **kwargs):
#         job = kwargs.pop('job', None)
#         print(job)
#         super().__init__(*args, **kwargs)
#         if job:
#             self.fields['job'].initial = job
#             self.fields['job'].widget.attrs['readonly'] = True
#             self.fields['job'].widget.attrs['disabled'] = True  # Ensure it cannot be changed
#
#
# forms.py


class ServiceForm(forms.ModelForm):
    job_hidden = forms.CharField(widget=forms.HiddenInput(), required=True)

    class Meta:
        model = Service
        fields = ["name", "service_type", "vehicle", "cost"]

    def __init__(self, *args, **kwargs):
        job = kwargs.pop('job', None)
        super().__init__(*args, **kwargs)
        if job:
            self.fields['job_hidden'].initial = job.pk   # NOQA
            self.fields['job'] = forms.CharField(initial=job, disabled=True, required=False)
            self.fields['job'].label = 'Job'
