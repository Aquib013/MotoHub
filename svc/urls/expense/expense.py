# urls.py
from django.urls import path
from svc.views.expense import ExpenseListView, ExpenseDeleteView, ExpenseCreateUpdateView

expense_urlpatterns = [
    path('expense/create/', ExpenseCreateUpdateView.as_view(), name='expense_create'),
    path('expense/', ExpenseListView.as_view(), name='expense_list'),
    path('expense/edit/<int:pk>/', ExpenseCreateUpdateView.as_view(), name='expense_edit'),

    path('expenses/<int:pk>/delete/', ExpenseDeleteView.as_view(), name='expense_delete'),

    # path('expense/<int:pk>/update/', ExpenseUpdateView.as_view(), name='expense_update'),
    # other paths...
]
