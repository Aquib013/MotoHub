from django import forms

from svc.models import Job, JobItem


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["mechanic", "license_plate", "status"]


class JobItemForm(forms.ModelForm):
    job_hidden = forms.CharField(widget=forms.HiddenInput(), required=True)

    class Meta:
        model = JobItem
        fields = ["item", "item_quantity", "item_unit_price"]

    def __init__(self, *args, **kwargs):
        job = kwargs.pop('job', None)
        super().__init__(*args, **kwargs)
        if job:
            self.fields['job_hidden'].initial = job.pk  # NOQA
            self.fields['job'] = forms.CharField(initial=job, disabled=True, required=False)
            self.fields['job'].label = 'Job'

    def clean_item_quantity(self):
        item = self.cleaned_data.get('item')
        item_quantity = self.cleaned_data.get('item_quantity')
        if item and item.item_quantity_in_stock < item_quantity:
            raise forms.ValidationError(
                f"Insufficient stock for {item.item}. Available quantity is {item.item_quantity_in_stock}.")
        return item_quantity

    def clean_item_price(self):
        item = self.cleaned_data.get('item')
        item_unit_price = self.cleaned_data.get('item_unit_price')
        if item and item_unit_price < item.cost_price:
            raise forms.ValidationError(f"Item price cannot be less than the cost price ({item.cost_price}).")
        return item_unit_price
