from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from svc.models import BaseModel, Job, Vehicle

SERVICE_TYPE = (
    ("Machining", "Machining"),
    ("Workshop", "Workshop")
)


class Service(BaseModel):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    name = models.CharField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    service_type = models.CharField(choices=SERVICE_TYPE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.job_no}- {self.name}"  # NOQA


@receiver(post_save, sender=Service)
@receiver(post_delete, sender=Service)
def update_total_service_cost(sender, instance, **kwargs):
    job = instance.job
    total_cost = job.service_set.aggregate(total_cost=Sum("cost"))["total_cost"] or 0.0
    job.total_service_cost = total_cost
    job.save()
