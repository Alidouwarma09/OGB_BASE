import json

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import random
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages

from Model.models import Utilisateur
from .forms import ConnexionForm, ResetPasswordRequestForm, ProfileForm, ProfileImageForm


class Connexion(LoginView):
    template_name = 'connexion.html'
    form_class = ConnexionForm

    def get_success_url(self):
        if self.request.user.is_authenticated:
            return reverse('Personnel:acceuil')
        return reverse('Utilisateur:Connexion')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


def Deconnexion(request):
    logout(request)
    return redirect(reverse('Utilisateur:Connexion'))


@login_required
def profil(request):
    user = request.user

    profile_form = ProfileForm(instance=user)
    image_form = ProfileImageForm(instance=user)

    if request.method == 'POST':
        if 'image' in request.FILES:
            image_form = ProfileImageForm(request.POST, request.FILES, instance=user)
            if image_form.is_valid():
                image_form.save()
                return redirect('Utilisateur:profil')
        else:
            profile_form = ProfileForm(request.POST, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('Utilisateur:profil')

    return render(request, 'profil/index.html', {
        'profile_form': profile_form,
        'image_form': image_form,
    })


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
    for utilisateur in utilisateurs:
        utilisateur.est_en_ligne = utilisateur.est_en_ligne()
    if 'messages' in request.session:
        del request.session['messages']
    return render(request, 'gestion_utilisateur/index.html', {'utilisateurs': utilisateurs})


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
                utilisateur = Utilisateur(
                    username=username,
                    nom=nom,
                    prenom=prenom,
                    roles=roles,
                )
                utilisateur.set_password(password)  # Hachage du mot de passe avant de l'enregistrer

                if image:
                    utilisateur.image.save(image.name, image)

                utilisateur.save()  # Sauvegarde de l'utilisateur après avoir haché le mot de passe

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

        if password:
            if password == password_confirmation:
                utilisateur.set_password(password)
            else:
                return HttpResponse("Les mots de passe ne correspondent pas", status=400)

        utilisateur.save()

        return redirect('Utilisateur:gestion_utilisateur')

    return HttpResponse("Méthode non autorisée", status=405)


User = get_user_model()


def reset_password_request(request):
    if request.method == 'POST':
        form = ResetPasswordRequestForm(request.POST)
        if form.is_valid():
            identifiant = form.cleaned_data['email']
            user = None
            if '@' in identifiant:
                try:
                    user = Utilisateur.objects.get(email=identifiant)
                except Utilisateur.DoesNotExist:
                    messages.error(request, 'Utilisateur non trouvé avec cet email.')
            else:
                try:
                    user = Utilisateur.objects.get(telephone=identifiant)
                except Utilisateur.DoesNotExist:
                    messages.error(request, 'Utilisateur non trouvé avec ce numéro de téléphone.')
            if user:
                if user.is_admin:
                    code = random.randint(100000, 999999)
                    if user.email:
                        subject = 'Code de réinitialisation de mot de passe'
                        message = f'Votre code de réinitialisation est : {code}'
                        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
                    if user.telephone:
                        pass

                    request.session['reset_code'] = code
                    request.session['user_id'] = user.id

                    return redirect('Utilisateur:reset_password_validate')
                else:
                    messages.error(request, 'Cet utilisateur n\'a pas les droits d\'administrateur.')
            else:
                print(form.errors)
        else:
            messages.error(request, 'Le formulaire contient des erreurs.')

    else:
        form = ResetPasswordRequestForm()

    return render(request, 'reset_password_request/index.html', {'form': form})


def reset_password_validate(request):
    form = None
    if request.method == 'POST':
        code = request.POST.get('code')
        if code == str(request.session.get('reset_code')):
            return redirect('Utilisateur:reset_password_change')
        else:
            messages.error(request, 'Code de validation invalide.')
    return render(request, 'reset_password_validate/index.html')


def reset_password_change(request):
    user_id = request.session.get('user_id')
    try:
        user = Utilisateur.objects.get(id=user_id)
    except Utilisateur.DoesNotExist:
        messages.error(request, 'Utilisateur introuvable.')
        return redirect('Utilisateur:reset_password_request')

    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            messages.success(request, 'Votre mot de passe a été réinitialisé avec succès.')
            return redirect('Utilisateur:Connexion')
        else:
            messages.error(request, 'Formulaire invalide.')
            print(form.errors)
    else:
        form = SetPasswordForm(user)

    return render(request, 'reset_password_confirm/index.html', {'form': form})
