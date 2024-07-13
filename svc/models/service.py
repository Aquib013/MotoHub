from django.db import models

from svc.models import BaseModel, Job, Vehicle

SERVICE_TYPE = (
    ("Machining", "Machining"),
    ("Workshop", "Workshop")
)


class Service(BaseModel):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    name = models.CharField()
    cost = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    service_type = models.CharField(choices=SERVICE_TYPE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.job_no}- {self.name}"  # NOQA
