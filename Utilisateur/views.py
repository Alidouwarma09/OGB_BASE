import json

from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from .forms import ConnexionForm, UserRegistrationForm


class Connexion(LoginView):
    template_name = 'connexion.html'
    form_class = ConnexionForm

    def get_success_url(self):
        role = self.request.user.roles
        if role == 'ADMIN':
            return reverse('Personnel:acceuil')
        elif role == 'GESTIONNAIRE':
            return reverse('Accueil')
        else:
            return reverse('Utilisateur:Connexion')

    def form_invalid(self, form):
        errors = form.errors
        return self.render_to_response(self.get_context_data(form=form, errors=errors))


def Deconnexion(request):
    logout(request)
    return redirect(reverse('Utilisateur:Connexion'))


@csrf_exempt
def toggle_dark_mode(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            request.user.dark_mode = data.get('dark_mode', False)
            request.user.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False}, status=403)
