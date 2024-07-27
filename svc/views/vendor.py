from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView

from svc.forms import VendorForm, VendorPaymentForm
from svc.models import Vendor, VendorPayment, PurchaseOrder


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendor = get_object_or_404(Vendor, pk=self.kwargs['pk'])
        context['vendor'] = vendor
        return context

    def form_valid(self, form):
        vendor = get_object_or_404(Vendor, pk=self.kwargs['pk'])
        form.instance.vendor = vendor
        vendor.vendor_balance -= form.instance.pay_amount
        vendor.last_payment_date = timezone.now()
        vendor.last_payment_amount = form.instance.pay_amount
        vendor.save()
        messages.success(self.request, "Payment Added successfully.")

        return super().form_valid(form)


class VendorPaymentHistoryView(DetailView):
    model = VendorPayment
    template_name = 'vendor/vendor_payment_history.html'
    context_object_name = 'vendors'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendor = get_object_or_404(Vendor, pk=self.kwargs["pk"])
        context['vendor'] = vendor
        return context


class VendorPurchaseOrdersView(DetailView):
    model = Vendor
    template_name = "vendor/vendor_pos.html"
    context_object_name = "vendor"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['purchase_orders'] = self.object.purchase_orders.all()
        return context


class VendorPurchaseOrderDetailView(DetailView):
    model = PurchaseOrder
    template_name = 'vendor/vendor_po_detail.html'
    context_object_name = "po"

    def get_object(self, queryset=None):
        vendor_id = self.kwargs.get('vendor_pk')
        po_id = self.kwargs.get('po_pk')
        return get_object_or_404(PurchaseOrder, vendor__id=vendor_id, id=po_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vendor'] = self.object.vendor
        context['po_items'] = self.object.purchase_order_item.all()
        return context
