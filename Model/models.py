from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from datetime import date

from django.db.models import UniqueConstraint

from decimal import Decimal

from django.utils import timezone


class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Vous devez entrer un nom d'utilisateur")

        user = self.model(
            username=username,
            **extra_fields  # Ajout des champs supplémentaires
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username=username, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

    def create_admin(self, username, email, nom, prenom, roles, password=None):
        if not username:
            raise ValueError("Vous devez entrer un nom d'utilisateur")
        if not email:
            raise ValueError("Vous devez entrer un email")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            nom=nom,
            prenom=prenom,
            roles=roles
        )
        user.set_password(password)
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class Parametre(models.Model):
    info = models.CharField(default="Bienvenue")
    blocage_global = models.BooleanField(default=False, verbose_name="Bloquer l'application")
    titre = models.CharField(default="Information", max_length=100)
    is_afficher = models.BooleanField(default=True)
    image = models.ImageField(upload_to='OGB_Image/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk and Parametre.objects.exists():
            raise ValueError("Il ne peut y avoir qu'une seule instance de Parametre.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.info} {self.titre}"


class Utilisateur(AbstractBaseUser):
    date_mise_a_jour = models.DateTimeField(verbose_name="Date de mise a jour", auto_now=True)
    username = models.CharField(
        unique=True,
        max_length=255,
        blank=False
    )
    nom = models.CharField(max_length=250, verbose_name='nom')
    prenom = models.CharField(max_length=250)
    email = models.EmailField(max_length=254, null=True, blank=True, verbose_name='Email')
    telephone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Numéro de téléphone')
    last_activity = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    dark_mode = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    roles = models.CharField(max_length=20, default='EDUCATIF')
    image = models.ImageField(upload_to='ImagesGestionnaire/', null=True, blank=True)
    USERNAME_FIELD = 'username'
    objects = MyUserManager()

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    def est_en_ligne(self):
        if (timezone.now() - self.last_activity).seconds > 60:
            return False
        return True


class Pere_enfant(models.Model):
    nom_pere = models.CharField()
    prenom_pere = models.CharField()
    date_naissance_pere = models.DateField(blank=True, null=True)
    lieu_naissance_pere = models.CharField(blank=True, null=True)
    profession_pere = models.CharField(blank=True, null=True)
    ethnie_pere = models.CharField(blank=True, null=True)
    religion_pere = models.CharField(blank=True, null=True)
    nombre_personne_charge_pere = models.CharField(blank=True, null=True)
    contact_pere = models.CharField(blank=True, null=True)
    adresse_pere = models.CharField(blank=True, null=True)
    en_vie_pere = models.BooleanField(default=True, blank=True, null=True)
    en_couple_pere = models.BooleanField(default=True, blank=True, null=True)


class Mere_enfant(models.Model):
    nom = models.CharField()
    prenom = models.CharField()
    date_naissance = models.DateField(blank=True, null=True)
    lieu_naissance = models.CharField(blank=True, null=True)
    profession = models.CharField(blank=True, null=True)
    ethnie = models.CharField(blank=True, null=True)
    religion = models.CharField(blank=True, null=True)
    nombre_personne_charge = models.CharField(blank=True, null=True)
    contact = models.CharField(blank=True, null=True)
    adresse = models.CharField(blank=True, null=True)
    en_vie = models.BooleanField(default=True, blank=True, null=True)
    en_couple = models.BooleanField(default=True, blank=True, null=True)


class Repondant(models.Model):
    nom = models.CharField()
    prenom = models.CharField()
    nationalite = models.CharField(blank=True, null=True)
    profession = models.CharField(blank=True, null=True)
    ethnie = models.CharField(blank=True, null=True)
    religion = models.CharField(blank=True, null=True)
    contact = models.CharField(blank=True, null=True)
    adresse = models.CharField(blank=True, null=True)
    nombre_piece = models.CharField(blank=True, null=True)
    type_eau = models.CharField(blank=True, null=True)
    electrifie = models.BooleanField(default=True, blank=True, null=True)
    revenu_mensuel = models.BooleanField(default=False, blank=True, null=True)
    en_couple = models.BooleanField(default=True, blank=True, null=True)
    lien_parente = models.CharField(blank=True, null=True)
    type_habitat = models.CharField(blank=True, null=True)


class Pensionnnaire(models.Model):
    type_habitat_enfant = models.CharField(blank=True, null=True)
    personne_loge_enfant = models.CharField(blank=True, null=True)
    lieu_habitation_enfant = models.CharField(blank=True, null=True)
    nombre_piece_logement = models.CharField(blank=True, null=True)
    motif_deplacement_enfant = models.CharField(blank=True, null=True)
    electrifie_enfant = models.BooleanField(default=True, blank=True, null=True)
    nom_enfant = models.CharField()
    prenom_enfant = models.CharField()
    matricule = models.CharField(max_length=15, unique=True)
    date_ouverture_dossier = models.DateField()
    statue = models.CharField(max_length=40, blank=True, null=True)
    date_naissance_enfant = models.DateField()
    lieu_naissance_enfant = models.CharField(blank=True, null=True)
    nationalite_enfant = models.CharField(blank=True, null=True)
    es_scolarise = models.BooleanField(default=True, blank=True, null=True)
    a_antecdents = models.BooleanField(blank=True, null=True)
    niveau_etude_anterieur = models.CharField(blank=True, null=True)
    classe_inscrit = models.CharField(blank=True, null=True)
    religion_enfant = models.CharField(blank=True, null=True)
    taille = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Taille (en cm)")
    poids = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Poids (en kg)")
    pere = models.ForeignKey(Pere_enfant, on_delete=models.CASCADE, related_name="pensionnaires_pere", null=True,
                             blank=True)
    mere = models.ForeignKey(Mere_enfant, on_delete=models.CASCADE, related_name="pensionnaires_mere", null=True,
                             blank=True)
    repondant = models.ForeignKey(Repondant, on_delete=models.CASCADE, related_name="pensionnaires_repondant",
                                  null=True, blank=True)


class Dossier(models.Model):
    pensionnaire = models.ForeignKey(Pensionnnaire, on_delete=models.CASCADE, related_name="dossiers")
    fichier = models.FileField(upload_to="pensionnaires/dossiers/")
    description = models.CharField(max_length=255, blank=True, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dossier {self.id} pour {self.pensionnaire.nom_enfant}"


class Classe(models.Model):
    nom_classe = models.CharField(max_length=50)
    annee_scolaire = models.CharField(max_length=9,
                                      default=f"{date.today().year}-{date.today().year + 1}")

    def __str__(self):
        return f"{self.nom_classe} - {self.annee_scolaire}"


class Inscription(models.Model):
    pensionnaire = models.ForeignKey(Pensionnnaire, on_delete=models.CASCADE, related_name="inscriptions")
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name="inscriptions")
    ecole = models.CharField(blank=True, null=True, default="OGB")
    date_inscription = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['pensionnaire', 'classe'], name='unique_pensionnaire_classe')
        ]

    def __str__(self):
        return f"{self.pensionnaire.nom_enfant} inscrit en {self.classe.nom_classe} ({self.classe.annee_scolaire})"


class Evaluation(models.Model):
    inscription = models.ForeignKey(Inscription, on_delete=models.CASCADE, related_name="evaluations")
    evaluation1 = models.IntegerField(null=True, blank=True)
    evaluation2 = models.IntegerField(null=True, blank=True)
    evaluation3 = models.IntegerField(null=True, blank=True)
    moyenne = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    statut_final = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if self.moyenne is not None:
            try:
                self.moyenne = Decimal(self.moyenne)
                self.statut_final = 'Admis' if self.moyenne >= 10 else 'Redoublant'
            except (ValueError, TypeError):
                self.statut_final = 'Invalide'

        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['inscription'], name='unique_evaluation_per_inscription')
        ]

    def __str__(self):
        return f"Evaluation de {self.inscription.pensionnaire.nom_enfant} ({self.inscription.classe.nom_classe})"


class Parrain(models.Model):
    nom = models.CharField()
    prenom = models.CharField()
    enfant = models.ForeignKey(Pensionnnaire, on_delete=models.SET_NULL, blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    date_parrainage = models.DateField(blank=True, null=True)
    lieu_naissance = models.CharField(blank=True, null=True)
    nationalite = models.CharField(blank=True, null=True)
    profession = models.CharField(blank=True, null=True)
    ethnie = models.CharField(blank=True, null=True)
    religion = models.CharField(blank=True, null=True)
    type_famille = models.CharField(blank=True, null=True)
    charge_fixe = models.CharField(blank=True, null=True)
    nombre_personne_charge = models.CharField(blank=True, null=True)
    contact = models.CharField(blank=True, null=True)
    adresse = models.CharField(blank=True, null=True)
    nombre_piece = models.CharField(blank=True, null=True)
    type_eau = models.CharField(blank=True, null=True)
    electrifie = models.BooleanField(default=True, blank=True, null=True)
    en_vie = models.BooleanField(default=True, blank=True, null=True)
    en_couple = models.BooleanField(default=True, blank=True, null=True)
    situation_matrimoniale = models.CharField(blank=True, null=True)
    lien_parente = models.CharField(blank=True, null=True)
    niveau_etude = models.CharField(blank=True, null=True)
    type_habitat = models.CharField(blank=True, null=True)


class Antecedents(models.Model):
    enfant = models.ForeignKey(Pensionnnaire, on_delete=models.SET_NULL, blank=True, null=True)
    designation = models.CharField(blank=True, null=True)
    psychopathologie = models.CharField(blank=True, null=True)
    probleme = models.CharField(blank=True, null=True)


class SuiviMedicalTrimestriele(models.Model):
    pensionnaire = models.ForeignKey(
        'Pensionnnaire',
        on_delete=models.CASCADE,
        related_name='suivis_medicaux'
    )
    trimestre = models.PositiveSmallIntegerField()
    annee_scolaire = models.CharField(max_length=9, default=f"{date.today().year}-{date.today().year + 1}")
    taille_cm = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    poids_kg = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        unique_together = ('pensionnaire', 'trimestre', 'annee_scolaire')  # Un suivi par trimestre et par an
        constraints = [
            models.CheckConstraint(
                check=models.Q(trimestre__in=[1, 2, 3]),
                name='valid_trimestre_values'
            )
        ]

    def __str__(self):
        return f"Suivi {self.trimestre}/{self.annee_scolaire} - {self.pensionnaire.nom_enfant}"

    def __str__(self):
        return f"Suivi {self.trimestre}/{self.annee} - {self.pensionnaire.nom_enfant}"


class ConsultationMedicale(models.Model):
    pensionnaire = models.ForeignKey(
        'Pensionnnaire',
        on_delete=models.CASCADE,
        related_name='consultations_medicales'
    )
    date_consultation = models.DateField(auto_now_add=True)
    motif_consultation = models.TextField(blank=True, null=True)
    diagnostic = models.TextField(blank=True, null=True)
    traitement = models.TextField(blank=True, null=True)
    annee_scolaire = models.CharField(max_length=9, default=f"{date.today().year}-{date.today().year + 1}")

    def __str__(self):
        return f"Consultation {self.date_consultation} - {self.pensionnaire.nom_enfant}"
