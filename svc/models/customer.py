from django.db import models

from svc.models import BaseModel
from svc.constants.places import PLACE_CHOICES

CUSTOMER_CHOICE = (
    ("Mechanic", "Mechanic"),
    ("Non-Mechanic", "Non-Mechanic")
)


class Customer(BaseModel):
    customer_name = models.CharField()
    customer_mob_no = models.CharField(unique=True)
    customer_type = models.CharField(choices=CUSTOMER_CHOICE)
    place = models.CharField(choices=PLACE_CHOICES)
    dues = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.FloatField(default=0)
    last_billed_date = models.DateTimeField(null=True, blank=True)
    last_billed_amount = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)

    def __str__(self):
        return self.customer_name



