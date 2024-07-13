from django.urls import path

from svc.views.purchase_order import (PurchaseOrderListView, PurchaseOrderCreateView, PurchaseOrderDetailView,
                                      PurchaseOrderUpdateView, PurchaseOrderDeleteView)
from svc.views.purchase_order_item import PurchaseOrderItemCreateView, PurchaseOrderItemUpdateView

purchase_order_url_patterns = [
    path('purchase-orders/', PurchaseOrderListView.as_view(), name='purchase-orders'),
    path('purchase-orders/create/', PurchaseOrderCreateView.as_view(), name='purchase-order-create'),
    path('purchase-orders/<int:pk>/', PurchaseOrderDetailView.as_view(), name='purchase-order-detail'),
    path('purchase-orders/<int:pk>/update/', PurchaseOrderUpdateView.as_view(), name='purchase-order-update'),
    path('purchase-orders/<int:pk>/delete/', PurchaseOrderDeleteView.as_view(), name='purchase-order-delete'),
    path('purchase-orders/<int:pk>/items/add/', PurchaseOrderItemCreateView.as_view(), name='add-item'),
    path('purchase-orders/items/<int:pk>/edit/', PurchaseOrderItemUpdateView.as_view(), name='edit-item'),

]
