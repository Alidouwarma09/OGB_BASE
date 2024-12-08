import json

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from Model.models import Utilisateur
from .forms import ConnexionForm


class Connexion(LoginView):
    template_name = 'connexion.html'
    form_class = ConnexionForm

    def get_success_url(self):
        if self.request.user.is_authenticated:
            return reverse('Personnel:acceuil')
        return reverse('Utilisateur:Connexion')

    def form_invalid(self, form):
        # Passer les erreurs au contexte
        return self.render_to_response(self.get_context_data(form=form))


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


def gestion_utilisateur(request):
    utilisateur_connecter_id = request.user.id
    utilisateurs = Utilisateur.objects.exclude(id=utilisateur_connecter_id)
    return render(request, 'gestion_utilisateur/index.html', {'utilisateurs':utilisateurs})


def add_user(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        nom = request.POST.get('nom', '').strip()
        prenom = request.POST.get('prenom', '').strip()
        roles = request.POST.get('roles', '').strip()
        password = request.POST.get('password', '').strip()
        image = request.FILES.get('image')

        errors = []
        if not username:
            errors.append("L'identifiant est obligatoire.")
        if not nom:
            errors.append("Le nom est obligatoire.")
        if not prenom:
            errors.append("Le prénom est obligatoire.")
        if not password:
            errors.append("Le mot de passe est obligatoire.")
        if roles not in ['Utilisateur', 'Admin']:
            errors.append("Le rôle sélectionné est invalide.")

        if Utilisateur.objects.filter(username=username).exists():
            errors.append("L'identifiant existe déjà.")
        if len(username) < 3:
            errors.append("L'identifiant doit contenir au moins 3 caractères.")

        try:
            validate_password(password)
        except ValidationError as e:
            errors.extend(e.messages)

        if image and not image.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            errors.append("Le fichier d'image doit être au format PNG, JPG ou JPEG.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('Utilisateur:gestion_utilisateur')

        try:
            with transaction.atomic():
                utilisateur = Utilisateur.objects.create(
                    username=username,
                    nom=nom,
                    prenom=prenom,
                    roles=roles,
                )
                utilisateur.set_password(password)  # Hachage du mot de passe

                if image:
                    utilisateur.image.save(image.name, image)

                messages.success(request, "Utilisateur ajouté avec succès.")
                return redirect('Utilisateur:gestion_utilisateur')

        except Exception as e:
            messages.error(request, f"Une erreur inattendue s’est produite : {e}")
            return redirect('Utilisateur:gestion_utilisateur')
