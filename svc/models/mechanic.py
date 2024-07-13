from django.db import models
from .base import BaseModel
from ..constants.places import PLACE_CHOICES


class Mechanic(BaseModel):
    mechanic_name = models.CharField()
    mechanic_mob_no = models.CharField(unique=True)
    place = models.CharField(choices=PLACE_CHOICES)
    dues = models.FloatField(default=0)
    balance = models.FloatField(default=0)

    def __str__(self):
        return self.mechanic_name
