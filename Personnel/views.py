from datetime import datetime, date

from django.db import transaction
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.serializers import serialize

from Model.models import Pensionnnaire, Pere_enfant, Mere_enfant, Inscription, Classe
from django.contrib import messages


def acceuil(request):
    return render(request, 'accueil/index.html')


def enregistrer_pensionnaire(request):
    return render(request, 'enregistrer_pensionnaire/index.html')


def enregistrer_pensionnaire_et_pere(request):
    if request.method == "POST":
        date_naissance_enfant = request.POST.get('date_naissance_enfant', '').strip()
        date_ouverture_dossier = request.POST.get('date_ouverture_dossier', '').strip()
        nom_enfant = request.POST.get('nom_enfant', '').strip()
        prenom_enfant = request.POST.get('prenom_enfant', '').strip()
        matricule = request.POST.get('matricule', '').strip()
        statue = request.POST.get('statue', '').strip()
        lieu_naissance_enfant = request.POST.get('lieu_naissance_enfant', '').strip()
        nationalite_enfant = request.POST.get('nationalite_enfant', '').strip()
        es_scolarise = request.POST.get('es_scolarise', '').strip()
        a_antecdents = request.POST.get('es_scolarise', '').strip()
        niveau_etude_anterieur = request.POST.get('niveau_etude_anterieur', '').strip()
        classe_inscrit = request.POST.get('classe_inscrit', '').strip()
        religion_enfant = request.POST.get('religion_enfant', '').strip()
        type_habitat_enfant = request.POST.get('type_habitat_enfant', '').strip()
        personne_loge_enfant = request.POST.get('personne_loge_enfant', '').strip()
        lieu_habitation_enfant = request.POST.get('lieu_habitation_enfant', '').strip()
        nombre_piece_logement = request.POST.get('nombre_piece_logement', '').strip()
        motif_deplacement_enfant = request.POST.get('motif_deplacement_enfant', '').strip()
        electrifie_enfant = request.POST.get('electrifie_enfant', '').strip()

        nom_pere = request.POST.get('nom_pere', '').strip()
        prenom_pere = request.POST.get('prenom_pere', '').strip()
        date_naissance_pere = request.POST.get('date_naissance_pere', '').strip()
        lieu_naissance_pere = request.POST.get('lieu_naissance_pere', '').strip()
        ethnie_pere = request.POST.get('ethnie_pere', '').strip()
        religion_pere = request.POST.get('religion_pere', '').strip()
        nombre_personne_charge_pere = request.POST.get('nombre_personne_charge_pere', '').strip()
        contact_pere = request.POST.get('contact_pere', '').strip()
        adresse_pere = request.POST.get('adresse_pere', '').strip()
        profession_pere = request.POST.get('profession_pere', '').strip()
        en_vie_pere = request.POST.get('en_vie_pere', '').strip()
        en_couple_pere = request.POST.get('en_couple_pere', '').strip()

        nom_mere = request.POST.get('nom_mere', '').strip()
        prenom_mere = request.POST.get('prenom_mere', '').strip()
        date_naissance_mere = request.POST.get('date_naissance_mere', '').strip()
        lieu_naissance_mere = request.POST.get('lieu_naissance_mere', '').strip()
        ethnie_mere = request.POST.get('ethnie_mere', '').strip()
        religion_mere = request.POST.get('religion_mere', '').strip()
        nombre_personne_charge_mere = request.POST.get('nombre_personne_charge_mere', '').strip()
        contact_mere = request.POST.get('contact_mere', '').strip()
        adresse_mere = request.POST.get('adresse_mere', '').strip()
        profession_mere = request.POST.get('profession_mere', '').strip()
        en_vie_mere = request.POST.get('en_vie_mere', '').strip()
        en_couple_mere = request.POST.get('en_couple_mere', '').strip()

        es_scolarise = True if es_scolarise == "True" else False
        a_antecdents = True if a_antecdents == "True" else False
        en_couple_pere = True if en_couple_pere == "True" else False
        en_couple_mere = True if en_couple_mere == "True" else False
        en_vie_mere = True if en_vie_mere == "True" else False
        en_vie_pere = True if en_vie_pere == "True" else False

        if not (nom_enfant and prenom_enfant and matricule and date_naissance_enfant):
            messages.error(request, "Tous les champs obligatoires doivent être remplis.")
            return redirect('Personnel:enregistrer_pensionnaire')

        try:
            date_naissance_enfant = datetime.strptime(date_naissance_enfant, '%Y-%m-%d').date()
            with transaction.atomic():
                mere = Mere_enfant.objects.create(
                    prenom=prenom_mere,
                    nom=nom_mere,
                    date_naissance=date_naissance_mere,
                    lieu_naissance=lieu_naissance_mere,
                    ethnie=ethnie_mere,
                    religion=religion_mere,
                    nombre_personne_charge=nombre_personne_charge_mere,
                    contact=contact_mere,
                    adresse=adresse_mere,
                    profession=profession_mere,
                    en_couple=en_couple_mere,
                    en_vie=en_vie_mere,
                )
                pere = Pere_enfant.objects.create(
                    nom_pere=nom_pere,
                    prenom_pere=prenom_pere,
                    date_naissance_pere=date_naissance_pere,
                    lieu_naissance_pere=lieu_naissance_pere,
                    ethnie_pere=ethnie_pere,
                    religion_pere=religion_pere,
                    nombre_personne_charge_pere=nombre_personne_charge_pere,
                    contact_pere=contact_pere,
                    adresse_pere=adresse_pere,
                    profession_pere=profession_pere,
                    en_couple_pere=en_couple_pere,
                    en_vie_pere=en_vie_pere,
                )

                Pensionnnaire.objects.create(
                    pere=pere,
                    mere=mere,
                    nom_enfant=nom_enfant,
                    prenom_enfant=prenom_enfant,
                    date_ouverture_dossier=date_ouverture_dossier,
                    matricule=matricule,
                    date_naissance_enfant=date_naissance_enfant,
                    lieu_naissance_enfant=lieu_naissance_enfant,
                    nationalite_enfant=nationalite_enfant,
                    niveau_etude_anterieur=niveau_etude_anterieur,
                    classe_inscrit=classe_inscrit,
                    religion_enfant=religion_enfant,
                    es_scolarise=es_scolarise,
                    a_antecdents=a_antecdents,
                    statue=statue,
                    type_habitat_enfant=type_habitat_enfant,
                    lieu_habitation_enfant=lieu_habitation_enfant,
                    nombre_piece_logement=nombre_piece_logement,
                    electrifie_enfant=electrifie_enfant,
                    personne_loge_enfant=personne_loge_enfant,
                    motif_deplacement_enfant=motif_deplacement_enfant,
                )
            messages.success(request, "Enregistrement réussi.")
            return redirect('Personnel:enregistrer_pensionnaire')
            print({ve})
        except ValueError as ve:
            messages.error(request, f"Erreur de validation : {ve}")
            print({ve})
        except Exception as e:
            messages.error(request, "Une erreur inattendue s’est produite.")
        return redirect('Personnel:enregistrer_pensionnaire')


def liste_pensionnaire(request):
    nombre_total = Pensionnnaire.objects.count()
    oc_count = Pensionnnaire.objects.filter(statue='OC').count()
    cs_count = Pensionnnaire.objects.filter(statue='CS').count()
    om_count = Pensionnnaire.objects.filter(statue='OM').count()
    op_count = Pensionnnaire.objects.filter(statue='OP').count()
    search_query = request.GET.get('search', '')
    if search_query:
        pensionnaires = Pensionnnaire.objects.filter(
            nom_enfant__icontains=search_query
        ) | Pensionnnaire.objects.filter(
            prenom_enfant__icontains=search_query
        ) | Pensionnnaire.objects.filter(
            matricule__icontains=search_query
        )
    else:
        pensionnaires = Pensionnnaire.objects.all()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        results = []
        for pensionnaire in pensionnaires:
            results.append({
                'nom_enfant': pensionnaire.nom_enfant,
                'prenom_enfant': pensionnaire.prenom_enfant,
                'matricule': pensionnaire.matricule,
                'date_naissance_enfant': pensionnaire.date_naissance_enfant,
                'statue': pensionnaire.statue,
                'id': pensionnaire.id
            })
        return JsonResponse({'results': results})

    return render(request, 'liste_pensionnaire/index.html', {
        'pensionnaires': pensionnaires,
        'nombre_total': nombre_total,
        'oc_count': oc_count,
        'cs_count': cs_count,
        'op_count': op_count,
        'om_count': om_count,
    })


def details_pensionnaire(request, pensionnaire_id):
    details_pensionnaires = get_object_or_404(Pensionnnaire, id=pensionnaire_id)
    return render(request, 'details_pensionnaire/index.html', {'details_pensionnaires': details_pensionnaires})


def espace_scolaire(request):
    return render(request, 'espace_scolaire/index.html')


def inscription_scolaire(request):
    if request.method == "GET":
        pensionnaires = Pensionnnaire.objects.all()
        return render(request, 'espace_scolaire.html', {'pensionnaires': pensionnaires})

    if request.method == "POST":
        classe_name = request.POST.get('classe_name', '').strip()
        pensionnaire_id = request.POST.get('pensionnaire_id', '').strip()
        pensionnaire = get_object_or_404(Pensionnnaire, id=pensionnaire_id)
        try:
            with transaction.atomic():
                classe, created = Classe.objects.get_or_create(
                    nom_classe=classe_name,
                    annee_scolaire=f"{date.today().year}-{date.today().year + 1}"
                )
                Inscription.objects.create(
                    pensionnaire=pensionnaire,
                    classe=classe,
                )
            messages.success(request, "Enregistrement réussi.")
            return redirect('Personnel:espace_scolaire')
        except ValueError as ve:
            messages.error(request, f"Erreur de validation : {ve}")
        except Exception as e:
            messages.error(request, "Une erreur inattendue s’est produite.")
        return redirect('Personnel:espace_scolaire')

def pensionnaires_autocomplete(request):
    if 'term' in request.GET:
        print("Recherche reçue :", request.GET['term'])  # Débogage
        qs = Pensionnnaire.objects.filter(nom_enfant__icontains=request.GET['term'])
        results = [{'id': p.id, 'text': f"{p.nom_enfant} {p.prenom_enfant}"} for p in qs]
        print("Résultats renvoyés :", results)  # Débogage
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})

