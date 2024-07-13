from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView

from svc.forms import VendorForm, VendorPaymentForm
from svc.models import Vendor, VendorPayment


class VendorCreateView(CreateView):
    model = Vendor
    template_name = "vendor/create_vendor.html"
    form_class = VendorForm
    success_url = reverse_lazy("vendors")


class VendorListView(ListView):
    model = Vendor
    template_name = "vendor/vendors_list.html"
    context_object_name = "vendors"


class VendorUpdateView(UpdateView):
    model = Vendor
    form_class = VendorForm
    template_name = "vendor/create_vendor.html"
    success_url = reverse_lazy("vendors")


class VendorDeleteView(DeleteView):
    model = Vendor
    template_name = "vendor/vendor_confirm_delete.html"
    success_url = reverse_lazy("vendors")


class VendorPaymentCreateView(CreateView):
    model = VendorPayment
    template_name = "vendor/vendor_payment.html"
    form_class = VendorPaymentForm
    success_url = reverse_lazy("vendors")

    def form_valid(self, form):
        vendor = get_object_or_404(Vendor, pk=self.kwargs['pk'])
        print(vendor)
        form.instance.vendor = vendor
        vendor.vendor_balance -= form.instance.pay_amount
        vendor.last_payment_date = timezone.now()
        vendor.last_payment_amount = form.instance.pay_amount
        vendor.save()
        return super().form_valid(form)


class VendorPaymentHistoryView(DetailView):
    model = VendorPayment
    template_name = 'vendor/vendor_payment_history.html'
    context_object_name = 'vendors'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendor = get_object_or_404(Vendor, pk=self.kwargs["pk"])
        print(vendor)
        context['vendor'] = vendor
        return context
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     vendor_payment = self.object  # Retrieve the VendorPayment instance
    #     vendor = vendor_payment.vendor  # Access the associated Vendor instance
    #
    #     # Optionally, you can use get_object_or_404 to ensure Vendor exists
    #     context['vendor'] = vendor  # Add vendor to context
    #
    #     return context
