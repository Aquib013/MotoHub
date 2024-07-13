from django.db import models
from django.db.models import F, Sum
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from svc.models import BaseModel, Job, Item


class JobItem(BaseModel):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    item_quantity = models.PositiveIntegerField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)


@receiver(pre_save, sender=JobItem)
def update_item_quantity(sender, instance, **kwargs):
    if instance.pk:
        # If the item already exists, get the previous quantity
        previous_item = JobItem.objects.get(pk=instance.pk)
        previous_quantity = previous_item.item_quantity
    else:
        previous_quantity = 0

    item = instance.item
    quantity_difference = instance.item_quantity - previous_quantity
    item.item_quantity_in_stock = F('item_quantity_in_stock') - quantity_difference
    item.save()


@receiver(post_delete, sender=JobItem)
def restore_item_quantity(sender, instance, **kwargs):
    item = instance.item
    if item:
        item.item_quantity_in_stock = F('item_quantity_in_stock') + instance.item_quantity
        item.save()


@receiver(post_save, sender=JobItem)
@receiver(post_delete, sender=JobItem)
def update_total_item_cost(sender, instance, **kwargs):
    job = instance.job
    total_item_cost = job.jobitem_set.aggregate(total_cost=Sum("item_price"))["total_cost"] or 0.0
    job.total_item_cost = total_item_cost
    job.save()
