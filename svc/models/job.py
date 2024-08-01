from datetime import datetime
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save, post_delete
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
    status = models.CharField(choices=JOB_STATUS, null=True, blank=True, default="Pending")
    license_plate = models.CharField(null=True, blank=True)
    job_completion_time = models.DateTimeField(null=True, blank=True)
    total_service_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_item_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    job_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True)

    def __str__(self):
        return f"{self.customer} - {self.job_no}"

    @staticmethod
    def unique_job_no():
        date = datetime.now().date().strftime("%d%m%Y")
        last_job = Job.objects.filter().order_by("-created_at").first()
        if last_job is None:
            last_job_id = 0
        else:
            last_job_id = last_job.id
        counter = last_job_id + 1
        job_no = f"{date}-{counter}"
        return job_no

    def save(self, *args, **kwargs):
        if not self.job_no:
            self.job_no = self.unique_job_no()
        if self.status == 'Completed' and self.job_completion_time is None:
            self.job_completion_time = timezone.now()
        elif self.status != "Completed":
            self.job_completion_time = None
        item_cost = Decimal(self.total_item_cost) if self.total_item_cost else Decimal(0)  # NOQA
        service_cost = Decimal(self.total_service_cost) if self.total_service_cost else Decimal(0)  # NOQA

        self.job_amount = item_cost + service_cost
        super(Job, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.status == "Completed" and self.paid_amount != self.job_amount:
            raise ValidationError("The job cannot be deleted as it has associated dues or balance !")
        super().delete(*args, **kwargs)


@receiver(post_save, sender=Job)
def update_customer_on_job_creation(sender, instance, created, **kwargs):
    if instance.status == 'Completed':
        customer = instance.customer
        customer.last_billed_amount = instance.job_amount
        customer.last_billed_date = instance.created_at
        customer.save()


@receiver(post_delete, sender=Job)
def update_customer_on_job_deletion(sender, instance, **kwargs):
    customer = instance.customer
    previous_job = Job.objects.filter(
            customer=customer,
            status="Completed"
        ).exclude(id=instance.id).order_by('-job_completion_time', '-created_at').first()

    if previous_job:
        customer.last_billed_amount = previous_job.job_amount
        customer.last_billed_date = previous_job.created_at
    else:
        customer.last_billed_amount = None
        customer.last_billed_date = None

    customer.save()
