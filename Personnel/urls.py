# Personnel/urls.py
from django.urls import path
from . import views
app_name = 'Personnel'
urlpatterns = [
    path('acceuil/', views.acceuil, name='acceuil'),
    path('enregistrer_pensionnaire/', views.enregistrer_pensionnaire, name='enregistrer_pensionnaire'),
    path('espace_scolaire/', views.espace_scolaire, name='espace_scolaire'),
    path('liste_pensionnaire/', views.liste_pensionnaire, name='liste_pensionnaire'),
    path('enregistrer_pensionnaire_et_pere/', views.enregistrer_pensionnaire_et_pere, name='enregistrer_pensionnaire_et_pere'),
    path('details_pensionnaire/<int:pensionnaire_id>', views.details_pensionnaire, name='details_pensionnaire'),
]
