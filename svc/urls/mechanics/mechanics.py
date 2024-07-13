from django.urls import path
from svc.views.mechanic import (
    MechanicListView,
    MechanicCreateView,
    MechanicUpdateView,
    MechanicDeleteView,
)

mechanic_url_patterns = [
    path("mechanics", MechanicListView.as_view(), name="mechanics"),
    path("mechanics/add", MechanicCreateView.as_view(), name="add_mechanic"),
    path("edit/<int:pk>", MechanicUpdateView.as_view(), name="edit_mechanic"),
    path("delete/<int:pk>", MechanicDeleteView.as_view(), name="delete_mechanic"),
]
