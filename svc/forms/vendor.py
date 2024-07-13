from django import forms

from svc.models import Vendor
from svc.models.vendors import VendorPayment


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ["firm_name", "vendor_name", "vendor_contact_no"]


class VendorPaymentForm(forms.ModelForm):
    class Meta:
        model = VendorPayment
        fields = ['pay_amount']
