from django import forms

from svc.models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["emp_name", "emp_contact", "emp_aadhaar", "emp_salary", "emp_address"]
        widgets = {
            'emp_address': forms.Textarea(attrs={'rows': 2}),
        }
