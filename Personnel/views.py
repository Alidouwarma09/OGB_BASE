import json
from datetime import datetime, date

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, IntegrityError
from django.db.models import Count
from django.db.models.functions import Round
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Avg, Count, F
from django.views.decorators.csrf import csrf_exempt

from Model.models import Pensionnnaire, Pere_enfant, Mere_enfant, Inscription, Classe, Evaluation, \
    SuiviMedicalTrimestriele, ConsultationMedicale, Antecedents, Repondant, Dossier
from django.contrib import messages


@login_required(login_url='Utilisateur:Connexion')
def acceuil(request):
    current_date = date.today()
    if current_date.month >= 9:
        annee_scolaire = f"{current_date.year}-{current_date.year + 1}"
    else:
        annee_scolaire = f"{current_date.year - 1}-{current_date.year}"

    today = date.today()
    stats = {
        'total_pensionnaires': Pensionnnaire.objects.count(),
        'consultations_recentes': ConsultationMedicale.objects.filter(annee_scolaire=annee_scolaire,
                                                                      date_consultation__month=today.month).count(),
        'inscriptions_actuelles': Inscription.objects.filter(classe__nom_classe=annee_scolaire).count(),
    }

    total_suivis = SuiviMedicalTrimestriele.objects.filter(annee_scolaire=annee_scolaire).count()
    consultations_data = (
        ConsultationMedicale.objects.filter(date_consultation__month=today.month)
        .values('pensionnaire__nom_enfant')
        .annotate(total=Count('id'))
    )
    data_classe = {
        'labels': [item['pensionnaire__nom_enfant'] for item in consultations_data],
        'values': [item['total'] for item in consultations_data],
    }
    if 'messages' in request.session:
        del request.session['messages']

    return render(
        request,
        'accueil/index.html',
        {
            'stats': stats,
            'total_suivis': total_suivis,
            'data_classe_json': json.dumps(data_classe),
        }
    )


@login_required(login_url='Utilisateur:Connexion')
def enregistrer_pensionnaire(request):
    return render(request, 'enregistrer_pensionnaire/index.html')


@login_required(login_url='Utilisateur:Connexion')
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
        a_antecdents = request.POST.get('a_antecdents', '').strip()
        niveau_etude_anterieur = request.POST.get('niveau_etude_anterieur', '').strip()
        classe_inscrit = request.POST.get('classe_inscrit', '').strip()

        religion_enfant = request.POST.get('religion_enfant', '').strip()
        autre_religion_enfant = request.POST.get('autre_religion_enfant', '').strip()
        if religion_enfant == "Autre":
            religion_enfant = autre_religion_enfant
        type_habitat_enfant = request.POST.get('type_habitat_enfant', '').strip()
        personne_loge_enfant = request.POST.get('personne_loge_enfant', '').strip()

        lieu_habitation_enfant = request.POST.get('lieu_habitation_enfant', '').strip()
        autre_lieu_habitation_enfant = request.POST.get('autre_lieu_habitation_enfant', '').strip()
        if lieu_habitation_enfant == "Autre":
            lieu_habitation_enfant = autre_lieu_habitation_enfant

        nombre_piece_logement = request.POST.get('nombre_piece_logement', '').strip()

        motif_deplacement_enfant = request.POST.get('motif_deplacement_enfant', '').strip()
        autre_motif_deplacement_enfant = request.POST.get('autre_motif_deplacement_enfant', '').strip()
        if motif_deplacement_enfant == "Autre":
            motif_deplacement_enfant = autre_motif_deplacement_enfant

        electrifie_enfant = request.POST.get('electrifie_enfant', '').strip()

        nom_pere = request.POST.get('nom_pere', '').strip()
        prenom_pere = request.POST.get('prenom_pere', '').strip()
        date_naissance_pere = request.POST.get('date_naissance_pere', '').strip()
        lieu_naissance_pere = request.POST.get('lieu_naissance_pere', '').strip()
        ethnie_pere = request.POST.get('ethnie_pere', '').strip()

        religion_pere = request.POST.get('religion_pere', '').strip()
        autre_religion_pere = request.POST.get('autre_religion_pere', '').strip()
        if religion_pere == "Autre":
            religion_pere = autre_religion_pere
        nombre_personne_charge_pere = request.POST.get('nombre_personne_charge_pere', '').strip()
        contact_pere = request.POST.get('contact_pere', '').strip()

        adresse_pere = request.POST.get('adresse_pere', '').strip()
        autre_adresse_pere = request.POST.get('autre_adresse_pere', '').strip()
        if adresse_pere == "Autre":
            adresse_pere = autre_adresse_pere

        profession_pere = request.POST.get('profession_pere', '').strip()
        en_vie_pere = request.POST.get('en_vie_pere', '').strip()
        en_couple_pere = request.POST.get('en_couple_pere', '').strip()

        nom_mere = request.POST.get('nom_mere', '').strip()
        nom_repondant = request.POST.get('nom_repondant', '').strip()
        prenom_mere = request.POST.get('prenom_mere', '').strip()
        date_naissance_mere = request.POST.get('date_naissance_mere', '').strip()
        lieu_naissance_mere = request.POST.get('lieu_naissance_mere', '').strip()
        ethnie_mere = request.POST.get('ethnie_mere', '').strip()

        religion_mere = request.POST.get('religion_mere', '').strip()
        autre_religion_mere = request.POST.get('autre_religion_mere', '').strip()
        if religion_mere == "Autre":
            religion_mere = autre_religion_mere
        nombre_personne_charge_mere = request.POST.get('nombre_personne_charge_mere', '').strip()
        contact_mere = request.POST.get('contact_mere', '').strip()

        adresse_mere = request.POST.get('adresse_mere', '').strip()
        autre_adresse_mere = request.POST.get('autre_adresse_mere', '').strip()
        if adresse_mere == "Autre":
            adresse_mere = autre_adresse_mere
        profession_mere = request.POST.get('profession_mere', '').strip()
        en_vie_mere = request.POST.get('en_vie_mere', '').strip()
        en_couple_mere = request.POST.get('en_couple_mere', '').strip()
        en_couple_repondant = request.POST.get('en_couple_repondant', '').strip()
        revenu_mensuel_repondant = request.POST.get('revenu_mensuel_repondant', '').strip()
        electrifie_repondant = request.POST.get('electrifie_repondant', '').strip()

        es_scolarise = True if es_scolarise == "True" else False
        a_antecdents = True if a_antecdents == "True" else False
        en_couple_pere = True if en_couple_pere == "True" else False
        en_couple_mere = True if en_couple_mere == "True" else False
        en_couple_repondant = True if en_couple_repondant == "True" else False
        revenu_mensuel_repondant = True if revenu_mensuel_repondant == "True" else False
        electrifie_repondant = True if electrifie_repondant == "True" else False
        en_vie_mere = True if en_vie_mere == "True" else False
        en_vie_pere = True if en_vie_pere == "True" else False

        if not (nom_enfant and prenom_enfant and matricule and date_naissance_enfant):
            messages.error(request, "Tous les champs obligatoires doivent être remplis.")
            return redirect('Personnel:enregistrer_pensionnaire')

        try:
            date_naissance_enfant = datetime.strptime(date_naissance_enfant, '%Y-%m-%d').date()
            with transaction.atomic():
                mere = None
                pere = None
                repondant = None
                if nom_mere:
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

                if nom_repondant:
                    repondant = Repondant.objects.create(
                        nom=nom_repondant,
                        prenom=request.POST.get('prenom_repondant', '').strip(),
                        nationalite=request.POST.get('nationalite_repondant', '').strip(),
                        profession=request.POST.get('profession_repondant', '').strip(),
                        ethnie=request.POST.get('ethnie_repondant', '').strip(),
                        religion=request.POST.get('religion_repondant', '').strip(),
                        contact=request.POST.get('contact_repondant', '').strip(),
                        adresse=request.POST.get('adresse_repondant', '').strip(),
                        nombre_piece=request.POST.get('nombre_piece_repondant', '').strip(),
                        type_eau=request.POST.get('type_eau_repondant', '').strip(),
                        lien_parente=request.POST.get('lien_parente', '').strip(),
                        type_habitat=request.POST.get('type_habitat_repondant', '').strip(),
                        en_couple=en_couple_repondant,
                        revenu_mensuel=revenu_mensuel_repondant,
                        electrifie=electrifie_repondant,
                    )
                    if nom_pere:
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

                enfant = Pensionnnaire.objects.create(
                    pere=pere if pere else None,
                    mere=mere if mere else None,
                    repondant=repondant if repondant else None,
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
                    taille=request.POST.get('taille', '').strip(),
                    poids=request.POST.get('poids', '').strip(),
                )
                if a_antecdents:
                    Antecedents.objects.create(
                        enfant=enfant,
                        designation=request.POST.get('designation', '').strip(),
                        psychopathologie=request.POST.get('psychopathologie', '').strip(),
                        probleme=request.POST.get('probleme', '').strip(),
                    )

            return redirect('Personnel:enregistrer_pensionnaire')
            print({ve})
        except ValueError as ve:
            messages.error(request, f"Erreur de validation : {ve}")
            print({ve})
        except Exception as e:
            messages.error(request, "Une erreur inattendue s’est produite.")
        return redirect('Personnel:enregistrer_pensionnaire')


@csrf_exempt
def update_pere_info(request):
    if request.method == 'POST':
        try:
            # Charger les données envoyées par le frontend
            data = json.loads(request.body)

            # Récupérer l'ID du pensionnaire ou du père depuis les données reçues
            pensionnaire_id = data.get('pensionnaire_id')
            if not pensionnaire_id:
                return JsonResponse({'success': False, 'error': 'ID du pensionnaire manquant'})

            # Vérifier si le pensionnaire existe
            pensionnaire = Pensionnnaire.objects.select_related('pere').filter(id=pensionnaire_id).first()
            if not pensionnaire or not pensionnaire.pere:
                return JsonResponse({'success': False, 'error': 'Pensionnaire ou père introuvable'})

            # Mettre à jour les champs du père
            pere = pensionnaire.pere
            for field, value in data.items():
                if hasattr(pere, field):
                    setattr(pere, field, value)
            pere.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Requête invalide'})


def update_mere_info(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pensionnaire_id = data.get('pensionnaire_id')
            if not pensionnaire_id:
                return JsonResponse({'success': False, 'error': 'ID du pensionnaire manquant'})
            pensionnaire = Pensionnnaire.objects.select_related('mere').filter(id=pensionnaire_id).first()
            if not pensionnaire or not pensionnaire.pere:
                return JsonResponse({'success': False, 'error': 'Pensionnaire ou père introuvable'})
            mere = pensionnaire.mere
            for field, value in data.items():
                if hasattr(mere, field):
                    setattr(mere, field, value)
            mere.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Requête invalide'})


@csrf_exempt
def update_enfant_info(request):
    if request.method == 'POST':
        try:
            # Charger les données envoyées par le frontend
            data = json.loads(request.body)

            # Récupérer l'ID du pensionnaire ou du père depuis les données reçues
            pensionnaire_id = data.get('pensionnaire_id')
            if not pensionnaire_id:
                return JsonResponse({'success': False, 'error': 'ID du pensionnaire manquant'})

            # Vérifier si le pensionnaire existe
            pensionnaire = Pensionnnaire.objects.filter(id=pensionnaire_id).first()
            if not pensionnaire:
                return JsonResponse({'success': False, 'error': 'Pensionnaire ou père introuvable'})
            for field, value in data.items():
                if hasattr(pensionnaire, field):
                    setattr(pensionnaire, field, value)
            pensionnaire.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Requête invalide'})


@login_required(login_url='Utilisateur:Connexion')
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


@login_required(login_url='Utilisateur:Connexion')
def details_pensionnaire(request, pensionnaire_id):
    details_pensionnaires = get_object_or_404(Pensionnnaire, id=pensionnaire_id)
    dossier_pensionnaire = Dossier.objects.filter(pensionnaire_id=pensionnaire_id)
    return render(request, 'details_pensionnaire/index.html', {'details_pensionnaires': details_pensionnaires,
                                                               'dossier_pensionnaire': dossier_pensionnaire,
                                                               })


@login_required(login_url='Utilisateur:Connexion')
def espace_scolaire(request):
    current_date = date.today()
    if current_date.month >= 9:
        annee_scolaire = f"{current_date.year}-{current_date.year + 1}"
    else:
        annee_scolaire = f"{current_date.year - 1}-{current_date.year}"
    classes_college = ['6e', '5e', '4e', '3e', '2nd', '1ere', 'Tle']

    nombre_eleve_college = Inscription.objects.filter(
        classe__nom_classe__in=classes_college, classe__annee_scolaire=annee_scolaire
    ).count()

    inscrits_ids = Inscription.objects.filter(classe__annee_scolaire=annee_scolaire).values_list('pensionnaire_id',
                                                                                                 flat=True)
    nombre_eleve = Inscription.objects.filter(classe__annee_scolaire=annee_scolaire).count()

    nombre_eleve_cp1 = Inscription.objects.filter(classe__nom_classe='CP1',
                                                  classe__annee_scolaire=annee_scolaire).count()
    nombre_eleve_cp2 = Inscription.objects.filter(classe__nom_classe='CP2',
                                                  classe__annee_scolaire=annee_scolaire).count()
    nombre_eleve_ce1 = Inscription.objects.filter(classe__nom_classe='CE1',
                                                  classe__annee_scolaire=annee_scolaire).count()
    nombre_eleve_ce2 = Inscription.objects.filter(classe__nom_classe='CE2',
                                                  classe__annee_scolaire=annee_scolaire).count()
    nombre_eleve_cm1 = Inscription.objects.filter(classe__nom_classe='CM1',
                                                  classe__annee_scolaire=annee_scolaire).count()
    nombre_eleve_cm2 = Inscription.objects.filter(classe__nom_classe='CM2',
                                                  classe__annee_scolaire=annee_scolaire).count()
    nombre_eleve_specialise = Inscription.objects.filter(classe__nom_classe='Specialise',
                                                         classe__annee_scolaire=annee_scolaire).count()
    pensionnaires = Pensionnnaire.objects.exclude(id__in=inscrits_ids)
    if 'messages' in request.session:
        del request.session['messages']

    return render(request, 'espace_scolaire/index.html', {
        'pensionnaires': pensionnaires,
        'annee_scolaire': annee_scolaire,
        'nombre_eleve_cp1': nombre_eleve_cp1,
        'nombre_eleve_cp2': nombre_eleve_cp2,
        'nombre_eleve_ce1': nombre_eleve_ce1,
        'nombre_eleve_ce2': nombre_eleve_ce2,
        'nombre_eleve_cm1': nombre_eleve_cm1,
        'nombre_eleve_cm2': nombre_eleve_cm2,
        'nombre_eleve': nombre_eleve,
        'nombre_eleve_specialise': nombre_eleve_specialise,
        'nombre_eleve_college': nombre_eleve_college,
    })


def ajouter_document(request, pensionnaire_id):
    if request.method == "POST":
        pensionnaire = Pensionnnaire.objects.get(pk=pensionnaire_id)
        fichier = request.FILES.get("fichier")
        description = request.POST.get("description")

        if fichier:
            Dossier.objects.create(
                pensionnaire=pensionnaire,
                fichier=fichier,
                description=description
            )
        return redirect("Personnel:details_pensionnaires", pensionnaire_id)


@login_required(login_url='Utilisateur:Connexion')
def inscription_scolaire(request):
    if request.method == "POST":
        classe_name = request.POST.get('classe_name', '').strip()
        ecole = request.POST.get('ecole', '').strip()
        pensionnaire_id = request.POST.get('pensionnaire_id', '').strip()
        pensionnaire = get_object_or_404(Pensionnnaire, id=pensionnaire_id)
        try:
            with transaction.atomic():
                annee_scolaire = f"{date.today().year}-{date.today().year + 1}"

                if Inscription.objects.filter(
                        pensionnaire=pensionnaire,
                        classe__annee_scolaire=annee_scolaire
                ).exists():
                    messages.error(
                        request,
                        f"{pensionnaire.nom_enfant} est déjà inscrit dans une autre classe pour l'année {annee_scolaire}."
                    )
                    return redirect('Personnel:espace_scolaire')

                classe, created = Classe.objects.get_or_create(
                    nom_classe=classe_name,
                    annee_scolaire=annee_scolaire
                )

                Inscription.objects.create(
                    pensionnaire=pensionnaire,
                    classe=classe,
                    ecole=ecole if ecole != '' else 'OGB'
                )

            messages.success(request, "Enregistrement réussi.")
            return redirect('Personnel:espace_scolaire')
        except IntegrityError:
            messages.error(
                request,
                f"{pensionnaire.nom_enfant} est déjà inscrit en {classe.nom_classe} pour cette année."
            )
        except Exception as e:
            messages.error(request, "Une erreur inattendue s’est produite.")
        return redirect('Personnel:espace_scolaire')


@login_required(login_url='Utilisateur:Connexion')
def rechercher_pensionnaires(request):
    current_date = date.today()
    if current_date.month >= 9:
        annee_scolaire = f"{current_date.year}-{current_date.year + 1}"
    else:
        annee_scolaire = f"{current_date.year - 1}-{current_date.year}"

    inscrits_ids = Inscription.objects.filter(classe__annee_scolaire=annee_scolaire).values_list('pensionnaire_id',
                                                                                                 flat=True)
    query = request.GET.get('q', '')

    pensionnaires = Pensionnnaire.objects.exclude(id__in=inscrits_ids)
    if query:
        pensionnaires = pensionnaires.filter(nom_enfant__icontains=query)

    data = {
        "results": [
            {"id": pensionnaire.id, "text": f"{pensionnaire.nom_enfant} {pensionnaire.prenom_enfant}"}
            for pensionnaire in pensionnaires
        ]
    }
    return JsonResponse(data)


@login_required(login_url='Utilisateur:Connexion')
def detatil_classe(request, classe=None):
    classe_nam = classe
    current_date = date.today()

    if current_date.month >= 9:
        annee_scolaire = f"{current_date.year}-{current_date.year + 1}"
    else:
        annee_scolaire = f"{current_date.year - 1}-{current_date.year}"

    if classe == 'COLLEGE':
        classes_college = ['6e', '5e', '4e', '3e', '2nd', '1ere', 'Tle']
        inscrits_ids = Inscription.objects.filter(
            classe__nom_classe__in=classes_college,
            classe__annee_scolaire=annee_scolaire
        ).values_list('pensionnaire_id', flat=True)
    else:
        inscrits_ids = Inscription.objects.filter(
            classe__nom_classe=classe,
            classe__annee_scolaire=annee_scolaire
        ).values_list('pensionnaire_id', flat=True)

    inscrits_total_ids = Inscription.objects.filter(
        classe__annee_scolaire=annee_scolaire
    ).values_list('pensionnaire_id', flat=True)

    if classe != "TOTAL":
        pensionnaires = Pensionnnaire.objects.filter(id__in=inscrits_ids)
    else:
        pensionnaires = Pensionnnaire.objects.filter(id__in=inscrits_total_ids)

    pensionnaires_details = []
    for index, pensionnaire in enumerate(pensionnaires, start=1):
        inscription = Inscription.objects.filter(pensionnaire=pensionnaire,
                                                 classe__annee_scolaire=annee_scolaire).first()
        if inscription:
            classe_enfant = inscription.classe.nom_classe
            evaluation_exist = Evaluation.objects.filter(inscription=inscription).exists()
            ecole = inscription.ecole
        else:
            classe_enfant = None
            evaluation_exist = False

        pensionnaires_details.append({
            'numero': index,
            'nom_enfant': pensionnaire.nom_enfant,
            'prenom_enfant': pensionnaire.prenom_enfant,
            'matricule': pensionnaire.matricule,
            'date_naissance_enfant': pensionnaire.date_naissance_enfant,
            'statue': pensionnaire.statue,
            'id': pensionnaire.id,
            'classe': classe_enfant,
            'evaluation_exist': evaluation_exist,
            'ecole': ecole,
        })

    nombre_total = len(pensionnaires_details)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'results': pensionnaires_details})

    return render(request, 'detatil_classe/index.html', {
        'pensionnaires': pensionnaires_details,
        'nombre_total': nombre_total,
        'classe_nam': classe_nam,
    })


@login_required(login_url='Utilisateur:Connexion')
def evaluate_pensionnaire(request, pensionnaire_id):
    if request.method == 'POST':
        pensionnaire = get_object_or_404(Pensionnnaire, id=pensionnaire_id)
        inscription = Inscription.objects.filter(pensionnaire=pensionnaire).first()

        if not inscription:
            return JsonResponse({'success': False, 'message': "L'élève n'est pas inscrit dans une classe."}, status=400)
        evaluation, created = Evaluation.objects.get_or_create(inscription=inscription)
        evaluation.evaluation1 = request.POST.get('evaluation1')
        evaluation.evaluation2 = request.POST.get('evaluation2')
        evaluation.evaluation3 = request.POST.get('evaluation3')
        evaluation.moyenne = request.POST.get('moyenne')
        evaluation.save()
        return JsonResponse({'success': True, 'message': "Évaluation enregistrée avec succès."})


@login_required(login_url='Utilisateur:Connexion')
def resultats_scolaire(request):
    annee_scolaire = request.GET.get('annee_scolaire', f"{date.today().year}-{date.today().year + 1}")
    selected_class = request.GET.get('classe', None)
    if selected_class:
        classes = Classe.objects.filter(annee_scolaire=annee_scolaire, nom_classe=selected_class)
    else:
        classes = Classe.objects.filter(annee_scolaire=annee_scolaire)

    inscriptions = Inscription.objects.filter(classe__in=classes)
    nombre_eleve = inscriptions.count()

    resultats = Evaluation.objects.filter(inscription__in=inscriptions).values(
        'inscription__pensionnaire__nom_enfant',
        'inscription__pensionnaire__prenom_enfant',
        'inscription__classe__nom_classe',
        'inscription__pensionnaire__matricule',
        'inscription__pensionnaire__statue',
        'inscription__pensionnaire__date_naissance_enfant',
        'inscription__pensionnaire__lieu_naissance_enfant',
        'inscription__pensionnaire__nationalite_enfant',
        'inscription__pensionnaire__religion_enfant',
        'statut_final'
    ).annotate(
        moyenne=Round(Avg('moyenne'), 2),
        admis=Count('id', filter=F('statut_final') == 'Admis')
    )
    taux_reussite = Evaluation.objects.filter(inscription__classe__in=classes, statut_final='Admis').count()
    taux_echec = Evaluation.objects.filter(inscription__classe__in=classes, statut_final='Redoublant').count()
    total_evaluations = Evaluation.objects.filter(inscription__classe__in=classes).count()
    taux_reussite_global = (taux_reussite / total_evaluations) * 100 if total_evaluations > 0 else 0
    taux_echec = (taux_echec / total_evaluations) * 100 if total_evaluations > 0 else 0
    moyenne_classe = resultats.aggregate(Avg('moyenne'))['moyenne__avg'] or 0
    context = {
        'classes': classes,
        'resultats': resultats,
        'taux_reussite_global': taux_reussite_global,
        'taux_echec': taux_echec,
        'moyenne_classe': moyenne_classe,
        'nombre_eleve': nombre_eleve,
    }

    return render(request, 'resultats/index.html', context)


@login_required(login_url='Utilisateur:Connexion')
def suivi_trimestrielle(request):
    current_date = date.today()
    if current_date.month >= 9:
        annee_scolaire = f"{current_date.year}-{current_date.year + 1}"
    else:
        annee_scolaire = f"{current_date.year - 1}-{current_date.year}"
    inscrits_ids = Inscription.objects.filter(classe__annee_scolaire=annee_scolaire).values_list('pensionnaire_id',
                                                                                                 flat=True)
    pensionnaires = Pensionnnaire.objects.filter(id__in=inscrits_ids)

    pensionnaires_data = []
    for pensionnaire in pensionnaires:
        suivis = SuiviMedicalTrimestriele.objects.filter(pensionnaire=pensionnaire, annee_scolaire=annee_scolaire)
        trimestres_suivis = suivis.values_list('trimestre', flat=True)
        trimestres_non_suivis = [t for t in [1, 2, 3] if t not in trimestres_suivis]
        pensionnaires_data.append({
            'pensionnaire': pensionnaire,
            'trimestres_suivis': trimestres_suivis,
            'trimestres_non_suivis': trimestres_non_suivis,
            'suivis': suivis,
        })
    pensionnaires_choice = pensionnaires.exclude(
        id__in=[p['pensionnaire'].id for p in pensionnaires_data if len(p['trimestres_suivis']) == 3]
    )
    pensionnaire_selected = pensionnaires_choice.first()
    return render(request, 'suivi_trimestrielle/index.html', {
        'pensionnaires_data': pensionnaires_data,
        'pensionnaires_choice': pensionnaires_choice,
        'pensionnaire_selected': pensionnaire_selected,
        'trimestres': [1, 2, 3],
    })


@login_required(login_url='Utilisateur:Connexion')
def create_new_suivi(request):
    if request.method == "POST":
        trimestre = request.POST.get('trimestre', '').strip()
        taille_cm = request.POST.get('taille_cm', '').strip()
        poids_kg = request.POST.get('poids_kg', '').strip()
        pensionnaire_id = request.POST.get('pensionnaires_choice_id', '').strip()

        try:
            if not pensionnaire_id or not trimestre:
                raise ValueError("Tous les champs sont obligatoires.")

            pensionnaire = Pensionnnaire.objects.get(id=pensionnaire_id)

            current_date = date.today()
            annee_scolaire = (
                f"{current_date.year}-{current_date.year + 1}"
                if current_date.month >= 9
                else f"{current_date.year - 1}-{current_date.year}"
            )

            with transaction.atomic():
                SuiviMedicalTrimestriele.objects.create(
                    pensionnaire=pensionnaire,
                    annee_scolaire=annee_scolaire,
                    trimestre=trimestre,
                    taille_cm=float(taille_cm),
                    poids_kg=float(poids_kg),
                )
                messages.success(request, "Suivi médical enregistré avec succès.")
                return redirect('Personnel:suivi_trimestrielle')

        except ValueError as e:
            messages.error(request, f"Erreur : {e}")
        except ObjectDoesNotExist:
            messages.error(request, "Le pensionnaire sélectionné n'existe pas.")
        except Exception as e:
            messages.error(request, f"Une erreur inattendue s’est produite : {e}")

        return redirect('Personnel:suivi_trimestrielle')


@login_required(login_url='Utilisateur:Connexion')
def consultation(request):
    current_date = date.today()
    if current_date.month >= 9:
        annee_scolaire = f"{current_date.year}-{current_date.year + 1}"
    else:
        annee_scolaire = f"{current_date.year - 1}-{current_date.year}"
    inscrits_ids = Inscription.objects.filter(classe__annee_scolaire=annee_scolaire).values_list('pensionnaire_id',
                                                                                                 flat=True)
    pensionnaires = Pensionnnaire.objects.filter(id__in=inscrits_ids)
    consultations = ConsultationMedicale.objects.filter(pensionnaire__in=pensionnaires)
    for pensionnaire in pensionnaires:
        inscription = Inscription.objects.filter(pensionnaire=pensionnaire).first()
        if inscription:
            pensionnaire.classe_nom_classe = inscription.classe.nom_classe
        else:
            pensionnaire.classe_nom_classe = "Non assignée"

    return render(request, 'consultation/index.html', {
        'pensionnaires': pensionnaires,
        'consultations': consultations,
    })


@login_required(login_url='Utilisateur:Connexion')
def create_new_consultation(request):
    if request.method == "POST":
        motif_consultation = request.POST.get('motif_consultation', '').strip()
        diagnostic = request.POST.get('diagnostic', '').strip()
        traitement = request.POST.get('traitement', '').strip()
        pensionnaire_id = request.POST.get('pensionnaires_choicee_id', '').strip()
        try:
            if not pensionnaire_id or not motif_consultation or not diagnostic or not traitement:
                raise ValueError("Tous les champs sont obligatoires.")

            pensionnaire = Pensionnnaire.objects.get(id=pensionnaire_id)

            current_date = date.today()
            annee_scolaire = (
                f"{current_date.year}-{current_date.year + 1}"
                if current_date.month >= 9
                else f"{current_date.year - 1}-{current_date.year}"
            )

            with transaction.atomic():
                # Créer une nouvelle consultation médicale
                ConsultationMedicale.objects.create(
                    pensionnaire=pensionnaire,
                    annee_scolaire=annee_scolaire,
                    diagnostic=diagnostic,
                    motif_consultation=motif_consultation,
                    traitement=traitement,
                )
                messages.success(request, "La consultation a été enregistrée avec succès.")
                return redirect('Personnel:consultation')
        except ValueError as e:
            messages.error(request, f"Erreur : {e}")
        except ObjectDoesNotExist:
            messages.error(request, "Le pensionnaire sélectionné n'existe pas.")
        except Exception as e:
            messages.error(request, f"Une erreur inattendue s’est produite : {e}")
        return redirect('Personnel:consultation')
