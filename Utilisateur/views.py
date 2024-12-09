import json

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
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


@csrf_exempt
def bloque_user(request, user_id):
    if request.method == 'POST':

        try:
            utilisateur = get_object_or_404(Utilisateur, id=user_id)
            utilisateur.is_active = False
            utilisateur.save()
            return JsonResponse({
                'success': True,
                'message': f"L'utilisateur {utilisateur.nom} a été bloqué."
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'}, status=403)


@csrf_exempt
def debloque_user(request, user_id):
    if request.method == 'POST':
        try:
            utilisateur = get_object_or_404(Utilisateur, id=user_id)
            utilisateur.is_active = True
            utilisateur.save()
            return JsonResponse({
                'success': True,
                'message': f"L'utilisateur {utilisateur.nom} a été débloqué."
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'}, status=403)


@csrf_exempt
def delete_user(request, user_id):
    if request.method == 'POST':
        try:
            utilisateur = get_object_or_404(Utilisateur, id=user_id)
            utilisateur.delete()
            return JsonResponse({
                'success': True,
                'message': f"L'utilisateur {utilisateur.nom} a été débloqué."
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'}, status=403)

@csrf_exempt
def edit_user(request, user_id):
    utilisateur = get_object_or_404(Utilisateur, id=user_id)

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        nom = request.POST.get('nom', '').strip()
        prenom = request.POST.get('prenom', '').strip()
        roles = request.POST.get('roles', '').strip()
        password = request.POST.get('password', '').strip()
        password_confirmation = request.POST.get('password_confirmation', '').strip()

        # Mise à jour des autres informations
        utilisateur.username = username
        utilisateur.nom = nom
        utilisateur.prenom = prenom
        utilisateur.roles = roles

        # Si un mot de passe est soumis et que la confirmation est valide
        if password:
            if password == password_confirmation:
                utilisateur.set_password(password)  # Utiliser set_password pour hasher le mot de passe
            else:
                return HttpResponse("Les mots de passe ne correspondent pas", status=400)

        utilisateur.save()

        return redirect('Utilisateur:gestion_utilisateur')

    return HttpResponse("Méthode non autorisée", status=405)
