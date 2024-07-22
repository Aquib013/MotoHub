from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from svc.forms.customer import CustomerForm
from svc.models import Customer


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
