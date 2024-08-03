from django import forms

from svc.models import Service, Job
from svc.models.service import MACHINING_CHOICES, WORKSHOP_CHOICES


class ServiceForm(forms.ModelForm):
    job_hidden = forms.CharField(widget=forms.HiddenInput(), required=True)

    class Meta:
        model = Service
        fields = ["service_type", "description", "vehicle", "quantity", "unit_service_cost"]

    def __init__(self, *args, **kwargs):
        job = kwargs.pop('job', None)
        super().__init__(*args, **kwargs)
        if job:
            self.fields['job_hidden'].initial = job.pk  # NOQA
            self.fields['job'] = forms.CharField(initial=job, disabled=True, required=False,
                                                 widget=forms.TextInput(attrs={'readonly': 'readonly'}))
            self.fields['job'].label = 'Job'

        if self.instance and self.instance.service_type:
            if self.instance.service_type == 'Machining':
                choices = MACHINING_CHOICES
            elif self.instance.service_type == 'Workshop':
                choices = WORKSHOP_CHOICES
            else:
                choices = [('', '---------')]

            self.fields['description'] = forms.ChoiceField(
                choices=choices,
                initial=self.instance.description
            )
        else:
            self.fields['description'] = forms.ChoiceField(
                choices=[('', '---------')],
                initial=''
            )

    def clean(self):
        cleaned_data = super().clean()
        service_type = cleaned_data.get('service_type')
        description = cleaned_data.get('description')

        if service_type == 'Machining':
            if description not in dict(MACHINING_CHOICES):
                raise forms.ValidationError('Invalid description for Machining service type')
        elif service_type == 'Workshop':
            if description not in dict(WORKSHOP_CHOICES):
                raise forms.ValidationError('Invalid description for Workshop service type')

        return cleaned_data
