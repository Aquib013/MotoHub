from django.db import models
from django.db.models import F
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from svc.models import BaseModel, PurchaseOrder, Item


class PurchaseOrderItem(BaseModel):
    purchase_order = models.ForeignKey(PurchaseOrder, related_name="purchase_order_item", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    item_MRP = models.DecimalField(max_digits=10, decimal_places=1)
    quantity = models.PositiveIntegerField(default=0)
    discount_percentage = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    net_price = models.PositiveIntegerField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=0)

    def save(self, *args, **kwargs):
        if self.discount_percentage is not None:
            discount_amount = (self.item_MRP * self.discount_percentage) / 100  # NOQA
            discounted_price = self.item_MRP - discount_amount  # NOQA
            self.unit_price = discounted_price
            self.total_amount = discounted_price * self.quantity  # NOQA
        else:
            self.unit_price = self.net_price
            self.total_amount = self.net_price * self.quantity  # NOQA
        super().save(*args, **kwargs)
        # Update the po_amount in the related PurchaseOrder
        self.purchase_order.po_amount = self.purchase_order.calculate_po_amount()  # NOQA
        self.purchase_order.save()  # NOQA

        # Reload the item to ensure F expression is applied correctly
        self.item.refresh_from_db()  # NOQA

        # Update the related Item instance
        # item = self.item
        # item.item_quantity_in_stock = F('item_quantity_in_stock') + self.quantity
        # item.item_MRP = self.item_MRP
        # item.discount_percentage = self.discount_percentage
        # item.net_price = self.net_price
        # item.cost_price = self.unit_price
        # item.save()  # NOQA


@receiver(pre_save, sender=PurchaseOrderItem)
def update_item_quantity(sender, instance, **kwargs):
    if instance.pk:
        # If the item already exists, get the previous quantity
        previous_item = PurchaseOrderItem.objects.get(pk=instance.pk)
        previous_quantity = previous_item.quantity
    else:
        previous_quantity = 0

    # Update the related Item instance with the difference in quantity
    item = instance.item
    quantity_difference = instance.quantity - previous_quantity
    item.item_quantity_in_stock = F('item_quantity_in_stock') + quantity_difference
    item.item_MRP = instance.item_MRP
    item.discount_percentage = instance.discount_percentage
    item.net_price = instance.net_price
    item.cost_price = instance.unit_price
    item.save()


@receiver(post_save, sender=PurchaseOrderItem)
def update_po_amount_on_save(sender, instance, **kwargs):
    instance.purchase_order.po_amount = instance.purchase_order.calculate_po_amount()
    instance.purchase_order.save()
    instance.purchase_order.vendor.update_vendor()


@receiver(post_delete, sender=PurchaseOrderItem)
def update_po_amount_on_delete(sender, instance, **kwargs):
    instance.purchase_order.po_amount = instance.purchase_order.calculate_po_amount()
    instance.purchase_order.save()
    instance.purchase_order.vendor.update_vendor()
