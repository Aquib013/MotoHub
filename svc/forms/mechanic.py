from django import forms
from svc.models.mechanic import Mechanic


class MechanicForm(forms.ModelForm):
    class Meta:
        model = Mechanic
        fields = ["mechanic_name", "mechanic_mob_no", "place"]
