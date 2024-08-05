from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import F

from svc.models import BaseModel, Employee

EXPENSE_TYPE = [
    ("Employee Payment", "Employee Payment"),
    ("Other", "Other")
]


class Expense(BaseModel):
    expense_type = models.CharField(choices=EXPENSE_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    employee = models.ForeignKey(Employee, related_name="employee_payments",
                                 on_delete=models.SET_NULL, null=True)
    comment = models.TextField(null=True, blank=True)
    expense_title = models.CharField(null=True, blank=True)

    def __str__(self):
        return f"{self.expense_type}-{self.comment}"

    def save(self, *args, **kwargs):
        # Check if the expense is being created or updated
        is_new = self.pk is None
        super().save(*args, **kwargs)  # Save the expense first
        if is_new:
            self.update_employee_dues_advance()

    def update_employee_dues_advance(self):
        employee = self.employee
        emp_salary = employee.emp_salary  # NOQA
        amount = self.amount

        if amount > emp_salary:
            extra_amount = amount - emp_salary
            employee.emp_advance = F('emp_advance') + extra_amount
        else:
            due_amount = emp_salary - amount
            employee.emp_dues = F('emp_dues') + due_amount

        employee.save(update_fields=['emp_dues', 'emp_advance'])   # NOQA

        # Fetch updated values from the database
        employee.refresh_from_db(fields=['emp_dues', 'emp_advance'])  # NOQA

        # Settle advance and dues if they are equal
        if employee.emp_dues == employee.emp_advance:
            employee.emp_dues = 0
            employee.emp_advance = 0

        employee.save(update_fields=['emp_dues', 'emp_advance'])  # NOQA
