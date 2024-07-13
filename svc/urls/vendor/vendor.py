from django.urls import path
from svc.views.vendor import (
    VendorListView,
    VendorCreateView, VendorUpdateView, VendorDeleteView, VendorPaymentCreateView, VendorPaymentHistoryView,
)

vendor_url_patterns = [
    path("vendors", VendorListView.as_view(), name="vendors"),
    path("vendors/add", VendorCreateView.as_view(), name="add_vendor"),
    path("vendor/edit/<int:pk>", VendorUpdateView.as_view(), name="edit_vendor"),
    path("vendor/delete/<int:pk>", VendorDeleteView.as_view(), name="delete_vendor"),
    path("vendor/<int:pk>/payment", VendorPaymentCreateView.as_view(), name="vendor-payment"),
    path("vendor/<int:pk>/payments", VendorPaymentHistoryView.as_view(), name="vendor-payment-history"),

]
