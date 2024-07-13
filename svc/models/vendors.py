from decimal import Decimal
from django.db import models
from django.db.models import Sum, Max
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from svc.models import BaseModel


class Vendor(BaseModel):
    firm_name = models.CharField()
    vendor_name = models.CharField()
    vendor_contact_no = models.CharField(unique=True)
    vendor_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_payment_date = models.DateTimeField(null=True, blank=True)
    last_payment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_purchase_date = models.DateTimeField(null=True, blank=True)

    def update_vendor(self):
        # Calculate and update vendor_balance based on related PurchaseOrders
        total_po_amount = self.purchase_order.aggregate(total=Sum('po_amount'))['total'] or Decimal('0.00')  # NOQA
        last_purchase = self.purchase_order.aggregate(last_date=Max("created_at"))['last_date']  # NOQA
        self.last_purchase_date = last_purchase
        self.vendor_balance = total_po_amount

        self.save()

    def __str__(self):
        return self.firm_name


class VendorPayment(BaseModel):
    vendor = models.ForeignKey(Vendor, related_name="vendor_payments", on_delete=models.CASCADE)
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.vendor}-{self.pay_amount}"


# @receiver(post_save, sender=VendorPayment)
# def update_vendor_balance(sender, instance, **kwargs):
#     pay_amount = instance.pay_amount
#     instance.vendor.vendor_balance -= pay_amount
#     instance.vendor.last_payment_amount = instance.pay_amount
#     instance.vendor.last_payment_date = instance.created_at
#     instance.vendor.save()
#
#
# @receiver(post_delete, sender=VendorPayment)
# def update_vendor_balance(sender, instance, **kwargs):
#     pay_amount = instance.pay_amount
#     instance.vendor.vendor_balance += pay_amount
#     instance.vendor.save()
