from datetime import datetime

from django.db import models
from django.utils import timezone

from svc.models import BaseModel, Mechanic


JOB_STATUS = (
    ("Pending", "Pending"),
    ("Completed", "Completed"),
    ("Cancelled", "Cancelled"),
)


class Job(BaseModel):
    job_no = models.CharField(unique=True)
    mechanic = models.ForeignKey(Mechanic, on_delete=models.SET_NULL, null=True)
    status = models.CharField(choices=JOB_STATUS, null=True, blank=True, default=0)
    license_plate = models.CharField(null=True, blank=True)
    job_completion_time = models.DateTimeField(null=True, blank=True)
    total_service_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_item_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    job_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.mechanic} - {self.job_no}"

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
        if self.total_item_cost or self.total_service_cost:
            self.job_amount = self.total_item_cost + self.total_service_cost  # NOQA
        else:
            self.job_amount = 0.0
        super(Job, self).save(*args, **kwargs)


