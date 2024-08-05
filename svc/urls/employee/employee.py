from django.urls import path

from svc.views.employee import (EmployeeListView, EmployeeCreateView,
                                EmployeeUpdateView, EmployeeDetailView, EmployeeDeleteView, EmployeePaymentHistoryView)

employee_url_patterns = [
    path('employees/', EmployeeListView.as_view(), name='employees'),
    path('employee/create/', EmployeeCreateView.as_view(), name='create_employee'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path("employees/<int:pk>/payments", EmployeePaymentHistoryView.as_view(), name="employee-payments"),
    path('employees/<int:pk>/update/', EmployeeUpdateView.as_view(), name='employee_update'),
    path('employees/<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee_delete'),
]
