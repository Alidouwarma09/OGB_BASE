from datetime import date

from Model.models import Parametre


def annee_scolaire_processor(request):
    current_date = date.today()
    if current_date.month >= 9:
        annee_scolaire = f"{current_date.year}-{current_date.year + 1}"
    else:
        annee_scolaire = f"{current_date.year - 1}-{current_date.year}"

    return {'annee_scolaire': annee_scolaire}


def parametre_context(request):
    try:
        parametre = Parametre.objects.first()
    except Parametre.DoesNotExist:
        parametre = None
    return {'parametre': parametre}
