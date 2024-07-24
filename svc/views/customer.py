from decimal import Decimal

from django.db.models import Sum, Case, When, F, DecimalField
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from svc.forms.customer import CustomerForm
from svc.models import Customer, Job


class CustomerListView(ListView):
    model = Customer
    template_name = "customer/customers_list.html"
    context_object_name = "customers"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     print(context['customers'])  # Print the customers to the console
    #     # return context


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = "customer/customer_form.html"
    success_url = reverse_lazy("customers")


class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = "customer/customer_form.html"
    success_url = reverse_lazy("customers")


class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = "customer/customer_confirm_delete.html"
    success_url = reverse_lazy("customers")


class CustomerJobsView(DetailView):
    model = Customer
    template_name = 'customer/customer_jobs.html'
    context_object_name = 'customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.object
        jobs = customer.job_set.all()  # Use the reverse relation

        # Calculate dues and balance
        job_calculations = jobs.aggregate(
            total_dues=Sum(Case(
                When(job_amount__gt=F('paid_amount'), then=F('job_amount') - F('paid_amount')),
                default=0,
                output_field=DecimalField()
            )),
            total_balance=Sum(Case(
                When(paid_amount__gt=F('job_amount'), then=F('paid_amount') - F('job_amount')),
                default=0,
                output_field=DecimalField()
            ))
        )

        total_dues = job_calculations['total_dues'] or Decimal('0.00')
        total_balance = job_calculations['total_balance'] or Decimal('0.00')

        if total_dues == total_balance:
            total_dues = Decimal("0")
            total_balance = Decimal("0")

        # Update customer dues and balance
        customer.dues = total_dues
        customer.balance = total_balance
        customer.save()

        context.update({
            'jobs': jobs,
            'total_dues': total_dues,
            'total_balance': total_balance,
        })
        return context
