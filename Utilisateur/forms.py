from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from Model.models import Utilisateur
from django import forms


class ConnexionForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(ConnexionForm, self).__init__(*args, **kwargs)
        self.fields['username'].error_messages = {
            'required': "Nom d'utilisateur invalide !"
        }
        self.fields['password'].error_messages = {
            'required': "Mot de passe invalide!"
        }
        self.error_messages.update({
            "invalid_login": "ce compte n'existe pas",
            "inactive": "Ce compte est inactif. Veuillez contacter l'administrateur.",
        })


class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['username'].error_messages = {
            'unique': 'Ce nom d\'utilisateur existe déjà.',
            'required': 'Ce champ est obligatoire.'
        }

    class Meta:
        model = Utilisateur
        fields = 'username', 'nom', 'prenom'


class UserRegistrationForme(UserCreationForm):
    class Meta:
        model = Utilisateur
        fields = 'username', 'nom', 'prenom', 'roles'

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForme, self).__init__(*args, **kwargs)

        self.fields['username'].error_messages = {
            'unique': 'Ce nom d\'utilisateur existe déjà.',
            'required': 'Ce champ est obligatoire.'
        }


class UserRegistrationFormee(UserChangeForm):
    class Meta:
        model = Utilisateur
        fields = 'nom', 'prenom'
