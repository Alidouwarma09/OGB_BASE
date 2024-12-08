from django.urls import path
from .views import Connexion, Deconnexion, toggle_dark_mode, gestion_utilisateur, add_user

app_name = 'Utilisateur'
urlpatterns = [
    path('', Connexion.as_view(), name='Connexion'),
    path('Deconnexion/', Deconnexion, name='Deconnexion'),
    path('add_user/', add_user, name='add_user'),
    path('gestion_utilisateur/', gestion_utilisateur, name='gestion_utilisateur'),
    path('toggle-dark-mode/', toggle_dark_mode, name='toggle_dark_mode'),
]
