from django.urls import path
from svc.views.job import JobCreateView, JobListView, JobDetailView, JobUpdateView, JobDeleteView
from svc.views.services import ServiceCreateView, ServiceUpdateView

job_url_patterns = [
    path("jobs/create-job/", JobCreateView.as_view(), name="create_job"),
    path('job/<int:pk>/add-service/', ServiceCreateView.as_view(), name='add_service'),
    path("jobs/", JobListView.as_view(), name="jobs"),
    path("jobs/<int:pk>/", JobDetailView.as_view(), name="job_detail"),
    path('service/<int:pk>/edit/', ServiceUpdateView.as_view(), name='edit_service'),
    path("jobs/<int:pk>/edit/", JobUpdateView.as_view(), name="job_edit"),
    path("jobs/<int:pk>/delete/", JobDeleteView.as_view(), name="job_delete"),
]
