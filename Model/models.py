from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from datetime import date  # Ajoute cette ligne en haut du fichier

from django.db.models import UniqueConstraint

from decimal import Decimal
# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("Vous devez entrer un nom d'utilisateur")

        user = self.model(
            username=username
        )
        user.set_password(password)
        user.save()
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


class Utilisateur(AbstractBaseUser):
    # mon_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    ROLES_CHOICES = [
        ('ADMIN', 'Administrateur'),
        ('GESTIONNAIRE', 'Gestionnaire'),
        ('UTILISATEUR', 'Utilisateur'),
    ]
    date_mise_a_jour = models.DateTimeField(verbose_name="Date de mise a jour", auto_now=True)
    username = models.CharField(
        unique=True,
        max_length=255,
        blank=False
    )
    email = models.EmailField(
        unique=True,
        max_length=255,
        blank=False
    )
    nom = models.CharField(max_length=250, verbose_name='nom')
    prenom = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    roles = models.CharField(max_length=20, choices=ROLES_CHOICES, default='UTILISATEUR')
    image = models.ImageField(upload_to='ImagesGestionnaire/', null=True, blank=True)
    USERNAME_FIELD = 'username'
    objects = MyUserManager()

    def __str__(self):
        return f"{self.nom} {self.prenom}"


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
    pere = models.ForeignKey(Pere_enfant, on_delete=models.CASCADE, related_name="pensionnaires_pere", null=True,
                             blank=True)
    mere = models.ForeignKey(Mere_enfant, on_delete=models.CASCADE, related_name="pensionnaires_mere", null=True,
                             blank=True)
    repondant = models.ForeignKey(Repondant, on_delete=models.CASCADE, related_name="pensionnaires_repondant",
                                  null=True, blank=True)


class Classe(models.Model):
    nom_classe = models.CharField(max_length=50)
    annee_scolaire = models.CharField(max_length=9,
                                      default=f"{date.today().year}-{date.today().year + 1}")

    def __str__(self):
        return f"{self.nom_classe} - {self.annee_scolaire}"


class Inscription(models.Model):
    pensionnaire = models.ForeignKey(Pensionnnaire, on_delete=models.CASCADE, related_name="inscriptions")
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name="inscriptions")
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
    ENTECEDENTS_CHOICES = (
        ('epilesie', 'epilesie'),
        ('diabete', 'diabete'),
        ('seroposivite', 'seroposivite'),
        ('hypertension', 'hypertension'),
        ('psychopathologie', 'psychopathologie'),
        ('trouble_digestifs', 'trouble digestifs'),
        ('dermatoses', 'dermatoses'),
        ('antecedents_operation', 'antecedents operation'),
        ('anemie', 'anemie'),
        ('hernie_ombidicale', 'hernie ombidicale'),
        ('carie_dentaire', 'carie dentaire'),
        ('handicap_physique', 'handicap physique'),
    )
    enfant = models.ForeignKey(Pensionnnaire, on_delete=models.SET_NULL, blank=True, null=True)
    designation = models.CharField(choices=ENTECEDENTS_CHOICES)
    psychopathologie = models.CharField(blank=True, null=True)
    probleme = models.CharField(blank=True, null=True)


class Taille(models.Model):
    trimestre1 = models.CharField()
    trimestre2 = models.CharField()
    trimestre3 = models.CharField()


class Poids(models.Model):
    trimestre1 = models.CharField()
    trimestre2 = models.CharField()
    trimestre3 = models.CharField()


class Suivi_medicale(models.Model):
    enfant = models.ForeignKey(Pensionnnaire, on_delete=models.SET_NULL, blank=True, null=True)
    taille = models.ForeignKey(Taille, on_delete=models.SET_NULL, blank=True, null=True)
    poid = models.ForeignKey(Poids, on_delete=models.SET_NULL, blank=True, null=True)
    annee_scolaire = models.CharField()


class Consultation(models.Model):
    enfant = models.ForeignKey(Pensionnnaire, on_delete=models.SET_NULL, blank=True, null=True)
    date_consultation = models.DateField(auto_now=True)
    motif = models.CharField()
    cat = models.CharField(blank=True, null=True)
