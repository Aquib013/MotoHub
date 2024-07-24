from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        exempt_paths = [
            reverse('login'),
            reverse('signup'),  # Add the URL name for your signup page
            # Add any other paths you want to exempt
        ]

        if not request.user.is_authenticated and request.path not in exempt_paths:
            return redirect(f'{reverse("login")}?next={request.path}')

        response = self.get_response(request)
        return response
