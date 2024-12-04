# Utilisateur/urls.py
from django.urls import path
from . import views  # Assurez-vous que le fichier views.py existe et contient les vues nécessaires
from .views import Connexion, Deconnexion

app_name = 'Utilisateur'
urlpatterns = [
    path('', Connexion.as_view(), name='Connexion'),
    path('Deconnexion/', Deconnexion, name='Deconnexion'),
]
