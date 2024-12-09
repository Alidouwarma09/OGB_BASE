from django.urls import path
from .views import Connexion, Deconnexion, toggle_dark_mode, gestion_utilisateur, add_user, bloque_user, debloque_user, \
    delete_user, edit_user

app_name = 'Utilisateur'
urlpatterns = [
    path('', Connexion.as_view(), name='Connexion'),
    path('Deconnexion/', Deconnexion, name='Deconnexion'),
    path('add_user/', add_user, name='add_user'),
    path('gestion_utilisateur/', gestion_utilisateur, name='gestion_utilisateur'),
    path('toggle-dark-mode/', toggle_dark_mode, name='toggle_dark_mode'),
    path('bloque_user/<int:user_id>/', bloque_user, name='bloque_user'),
    path('debloque_user/<int:user_id>/', debloque_user, name='debloque_user'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('edit_user/<int:user_id>/', edit_user, name='edit_user'),
]
