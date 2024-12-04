# Utilisateur/urls.py
from django.urls import path
from . import views  # Assurez-vous que le fichier views.py existe et contient les vues nécessaires
from .views import Connexion, Deconnexion, toggle_dark_mode

app_name = 'Utilisateur'
urlpatterns = [
    path('', Connexion.as_view(), name='Connexion'),
    path('Deconnexion/', Deconnexion, name='Deconnexion'),
    path('toggle-dark-mode/', toggle_dark_mode, name='toggle_dark_mode'),
]
