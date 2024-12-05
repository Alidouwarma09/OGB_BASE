# Personnel/urls.py
from django.urls import path
from . import views
from .views import details_pensionnaire, suivi_trimestrielle

app_name = 'Personnel'
urlpatterns = [
    path('acceuil/', views.acceuil, name='acceuil'),
    path('enregistrer_pensionnaire/', views.enregistrer_pensionnaire, name='enregistrer_pensionnaire'),
    path('espace_scolaire/', views.espace_scolaire, name='espace_scolaire'),
    path('suivi_trimestrielle/', suivi_trimestrielle, name='suivi_trimestrielle'),
    path('inscription_scolaire/', views.inscription_scolaire, name='inscription_scolaire'),
    path('rechercher_pensionnaires/', views.rechercher_pensionnaires, name='rechercher_pensionnaires'),
    path('liste_pensionnaire/', views.liste_pensionnaire, name='liste_pensionnaire'),
    path('resultats_scolaire/', views.resultats_scolaire, name='resultats_scolaire'),
    path('detatil_classe/<str:classe>/', views.detatil_classe, name='detatil_classe'),
    path('evaluate/<int:pensionnaire_id>/', views.evaluate_pensionnaire, name='evaluate_pensionnaire'),
    path('enregistrer_pensionnaire_et_pere/', views.enregistrer_pensionnaire_et_pere, name='enregistrer_info'),
    path('details/<int:pensionnaire_id>/', details_pensionnaire, name='details_pensionnaires'),
]
