from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User


class LastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user = request.user
            user.last_activity = timezone.now()
            user.save()

        response = self.get_response(request)
        return response
