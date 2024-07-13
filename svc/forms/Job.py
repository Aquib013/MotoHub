from django import forms

from svc.models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["mechanic", "license_plate", "status"]




