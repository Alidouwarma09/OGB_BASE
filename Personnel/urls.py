# Personnel/urls.py
from django.urls import path
from . import views
from .views import details_pensionnaire, suivi_trimestrielle, create_new_suivi, consultation, create_new_consultation, \
    update_pere_info, update_enfant_info, update_mere_info

app_name = 'Personnel'
urlpatterns = [
    path('', views.acceuil, name='acceuil'),
    path('enregistrer_pensionnaire/', views.enregistrer_pensionnaire, name='enregistrer_pensionnaire'),
    path('espace_scolaire/', views.espace_scolaire, name='espace_scolaire'),
    path('suivi_trimestrielle/', suivi_trimestrielle, name='suivi_trimestrielle'),
    path('ajouter-document/<int:pensionnaire_id>/', views.ajouter_document, name='ajouter_document'),
    path('consultation/', consultation, name='consultation'),
    path('update_pere_info/', update_pere_info, name='update_pere_info'),
    path('update_mere_info/', update_mere_info, name='update_mere_info'),
    path('update_enfant_info/', update_enfant_info, name='update_enfant_info'),
    path('inscription_scolaire/', views.inscription_scolaire, name='inscription_scolaire'),
    path('create_new_suivi/', create_new_suivi, name='create_new_suivi'),
    path('create_new_consultation/', create_new_consultation, name='create_new_consultation'),
    path('rechercher_pensionnaires/', views.rechercher_pensionnaires, name='rechercher_pensionnaires'),
    path('liste_pensionnaire/', views.liste_pensionnaire, name='liste_pensionnaire'),
    path('resultats_scolaire/', views.resultats_scolaire, name='resultats_scolaire'),
    path('detatil_classe/<str:classe>/', views.detatil_classe, name='detatil_classe'),
    path('evaluate/<int:pensionnaire_id>/', views.evaluate_pensionnaire, name='evaluate_pensionnaire'),
    path('enregistrer_pensionnaire_et_pere/', views.enregistrer_pensionnaire_et_pere, name='enregistrer_info'),
    path('details/<int:pensionnaire_id>/', details_pensionnaire, name='details_pensionnaires'),
]
