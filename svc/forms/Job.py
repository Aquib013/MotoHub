from django import forms

from svc.models import Job, JobItem, Customer


class JobForm(forms.ModelForm):
    add_payment = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label="Add Payment")

    class Meta:
        model = Job
        fields = ["customer", "license_plate", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['customer'] = forms.ModelChoiceField(
            queryset=Customer.objects.all(),
            widget=forms.Select(attrs={'class': 'form-control'}),
            empty_label="Select a customer"
        )
        self.fields['license_plate'].widget.attrs.update({
            'placeholder': 'Enter vehicle number',
        })
        self.fields['add_payment'].widget.attrs.update({'class': 'payment-field',
                                                        'placeholder': 'Enter the Amount Paid'})

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        add_payment = cleaned_data.get('add_payment')
        if status == 'Completed' and add_payment is None:
            raise forms.ValidationError({
                'add_payment': 'This field is required when the job status is completed.'
            })
        return cleaned_data


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

    def clean(self):
        cleaned_data = super().clean()
        item = cleaned_data.get("item")
        item_quantity = cleaned_data.get("item_quantity")
        item_unit_price = cleaned_data.get("item_unit_price")

        if item and item_quantity is not None:
            if item_quantity > item.item_quantity_in_stock:
                raise forms.ValidationError(f"Quantity exceeds available stock."
                                            f"Max available: {item.item_quantity_in_stock}")

        if item and item_unit_price is not None:
            if item_unit_price < item.cost_price:
                raise forms.ValidationError(f"Price must be greater than cost price: {item.cost_price}")

        return cleaned_data
