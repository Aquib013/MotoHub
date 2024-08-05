from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView

from svc.forms import EmployeeForm
from svc.models import Employee


class EmployeeCreateView(CreateView):
    model = Employee
    template_name = "employee/employee_form.html"
    form_class = EmployeeForm
    success_url = reverse_lazy("employees")


class EmployeeListView(ListView):
    model = Employee
    template_name = "employee/employees_list.html"
    context_object_name = "employees"
    ordering = ['-created_at']


class EmployeeDetailView(DetailView):
    model = Employee
    template_name = "employee/employee_detail.html"


class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = "employee/employee_form.html"
    success_url = reverse_lazy("employees")


class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = "employee/employee_confirm_delete.html"
    success_url = reverse_lazy("employees")


class EmployeePaymentHistoryView(DetailView):
    model = Employee
    template_name = "employee/employee_payments.html"
    context_object_name = 'employee'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = self.get_object()
        payments = employee.employee_payments.all().order_by('-created_at')
        context['payments'] = payments
        context['emp_dues'] = employee.emp_dues
        context['emp_advance'] = employee.emp_advance
        return context
