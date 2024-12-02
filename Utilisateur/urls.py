# Utilisateur/urls.py
from django.urls import path
from . import views  # Assurez-vous que le fichier views.py existe et contient les vues nécessaires
from .views import Connexion

app_name = 'Utilisateur'
urlpatterns = [
    path('', Connexion.as_view(), name='Connexion'),   # Remplacez 'accueil' par une vue définie dans views.py
]
