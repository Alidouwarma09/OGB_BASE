from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

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
            return reverse('utilisateur:connexion_user')

    def form_invalid(self, form):
        """Méthode appelée si le formulaire est invalide."""
        errors = form.errors  # Récupération des erreurs de validation du formulaire
        return self.render_to_response(self.get_context_data(form=form, errors=errors))


def deconnexion(request):
    logout(request)
    return redirect(reverse('utilisateur:connexion_user'))
