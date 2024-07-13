from django import forms
from svc.models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_brand', 'item', 'item_size', "item_type", 'item_for_vehicle', 'item_quantity_in_stock',
                  'item_MRP', 'discount_percentage', 'net_price']

    def clean(self):
        cleaned_data = super().clean()
        discount_percentage = cleaned_data.get("discount_percentage")
        net_price = cleaned_data.get("net_price")

        if discount_percentage and net_price:
            raise forms.ValidationError("Please enter any one of 'net price' or 'discount percentage'.")
        elif not discount_percentage and not net_price:
            raise forms.ValidationError("Please enter either 'net price' or 'discount percentage'.")

        return cleaned_data
