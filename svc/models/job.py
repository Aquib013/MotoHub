from datetime import datetime
from decimal import Decimal

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from svc.models import BaseModel, Customer

JOB_STATUS = (
    ("Pending", "Pending"),
    ("Completed", "Completed"),
    ("Cancelled", "Cancelled"),
)


class Job(BaseModel):
    job_no = models.CharField(unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    status = models.CharField(choices=JOB_STATUS, null=True, blank=True, default=0)
    license_plate = models.CharField(null=True, blank=True)
    job_completion_time = models.DateTimeField(null=True, blank=True)
    total_service_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_item_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    job_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.customer} - {self.job_no}"

    @staticmethod
    def unique_job_no():
        date = datetime.now().date().strftime("%d%m%Y")
        today_job_no = Job.objects.filter(
            created_at__date=datetime.now().date()
        ).count()
        job_no = f"{date}-{today_job_no + 1:03d}"
        return job_no

    def save(self, *args, **kwargs):
        if not self.job_no:
            self.job_no = self.unique_job_no()
        if self.status == 'Completed' and self.job_completion_time is None:
            self.job_completion_time = timezone.now()
        item_cost = Decimal(self.total_item_cost) if self.total_item_cost else Decimal(0)             # NOQA
        service_cost = Decimal(self.total_service_cost) if self.total_service_cost else Decimal(0)    # NOQA

        self.job_amount = item_cost + service_cost
        super(Job, self).save(*args, **kwargs)


@receiver(post_save, sender=Job)
def update_customer_data(sender, instance, **kwargs):
    customer = instance.customer
    last_billed_date = instance.created_at
    last_billed_amount = instance.job_amount
    customer.last_billed_date = last_billed_date
    customer.last_billed_amount = last_billed_amount
    customer.save()
