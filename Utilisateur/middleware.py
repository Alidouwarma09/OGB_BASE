from datetime import timedelta

from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from Model.models import Parametre


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


class BlocageMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        urls_exclues = [
            reverse('Utilisateur:Connexion'),
            reverse('Utilisateur:page_blocage'),
        ]
        if any(request.path.startswith(url) for url in urls_exclues):
            return self.get_response(request)
        parametre = Parametre.objects.first()
        if parametre and parametre.blocage_global:
            if request.user.is_authenticated:
                if request.user.roles != "ADMIN":
                    return redirect(reverse('Utilisateur:page_blocage'))
            else:
                return redirect(reverse('Utilisateur:Connexion'))

        return self.get_response(request)
