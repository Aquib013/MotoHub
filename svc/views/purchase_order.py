from django.db import transaction
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from svc.models import PurchaseOrder
from svc.forms import PurchaseOrderForm


class PurchaseOrderListView(ListView):
    model = PurchaseOrder
    template_name = 'purchase_order/purchase_order_list.html'
    context_object_name = "purchase_orders"


class PurchaseOrderCreateView(CreateView):
    model = PurchaseOrder
    form_class = PurchaseOrderForm
    template_name = 'purchase_order/purchase_order_form.html'
    success_url = reverse_lazy('purchase-orders')


class PurchaseOrderDetailView(DetailView):
    model = PurchaseOrder
    template_name = 'purchase_order/purchase_order_detail.html'


class PurchaseOrderUpdateView(UpdateView):
    model = PurchaseOrder
    fields = ['vendor']
    template_name = 'purchase_order/purchase_order_form.html'
    success_url = reverse_lazy('purchase-orders')


class PurchaseOrderDeleteView(DeleteView):
    model = PurchaseOrder
    template_name = 'purchase_order/purchase_order_confirm_delete.html'
    success_url = reverse_lazy('purchase-orders')


