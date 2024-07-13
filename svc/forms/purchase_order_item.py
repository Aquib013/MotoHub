from django import forms

from svc.models import PurchaseOrderItem


class PurchaseOrderItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderItem
        fields = ["item", "item_MRP", "quantity", "discount_percentage", "net_price"]

    def clean(self):
        cleaned_data = super().clean()
        discount_percentage = cleaned_data.get("discount_percentage")
        net_price = cleaned_data.get("net_price")

        if discount_percentage and net_price:
            raise forms.ValidationError("Please enter any one of 'net price' or 'discount percentage'.")
        elif not discount_percentage and not net_price:
            raise forms.ValidationError("Please enter either 'net price' or 'discount percentage'.")

        return cleaned_data
