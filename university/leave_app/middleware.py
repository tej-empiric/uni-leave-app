from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
from .backends import EmailBackend


class CustomAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is going to the admin login page
        if request.path.startswith("/admin/"):
            # Use the built-in ModelBackend for admin authentication
            request.backend = ModelBackend()
        else:
            # Use your custom EmailBackend for regular user authentication
            request.backend = EmailBackend()

        return self.get_response(request)
