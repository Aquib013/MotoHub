from django.urls import path
from svc.views.signup import SignUpView

Signup_urlpatterns = [path("signup", SignUpView.as_view(), name="signup")]
