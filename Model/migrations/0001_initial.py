# Generated by Django 4.2.13 on 2024-12-30 10:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_classe', models.CharField(max_length=50)),
                ('annee_scolaire', models.CharField(default='2024-2025', max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name='Mere_enfant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField()),
                ('prenom', models.CharField()),
                ('date_naissance', models.DateField(blank=True, null=True)),
                ('lieu_naissance', models.CharField(blank=True, null=True)),
                ('profession', models.CharField(blank=True, null=True)),
                ('ethnie', models.CharField(blank=True, null=True)),
                ('religion', models.CharField(blank=True, null=True)),
                ('nombre_personne_charge', models.CharField(blank=True, null=True)),
                ('contact', models.CharField(blank=True, null=True)),
                ('adresse', models.CharField(blank=True, null=True)),
                ('en_vie', models.BooleanField(blank=True, default=True, null=True)),
                ('en_couple', models.BooleanField(blank=True, default=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pensionnnaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_habitat_enfant', models.CharField(blank=True, null=True)),
                ('personne_loge_enfant', models.CharField(blank=True, null=True)),
                ('lieu_habitation_enfant', models.CharField(blank=True, null=True)),
                ('nombre_piece_logement', models.CharField(blank=True, null=True)),
                ('motif_deplacement_enfant', models.CharField(blank=True, null=True)),
                ('electrifie_enfant', models.BooleanField(blank=True, default=True, null=True)),
                ('nom_enfant', models.CharField()),
                ('prenom_enfant', models.CharField()),
                ('matricule', models.CharField(max_length=15, unique=True)),
                ('date_ouverture_dossier', models.DateField()),
                ('statue', models.CharField(blank=True, max_length=40, null=True)),
                ('date_naissance_enfant', models.DateField()),
                ('lieu_naissance_enfant', models.CharField(blank=True, null=True)),
                ('nationalite_enfant', models.CharField(blank=True, null=True)),
                ('es_scolarise', models.BooleanField(blank=True, default=True, null=True)),
                ('a_antecdents', models.BooleanField(blank=True, null=True)),
                ('niveau_etude_anterieur', models.CharField(blank=True, null=True)),
                ('classe_inscrit', models.CharField(blank=True, null=True)),
                ('religion_enfant', models.CharField(blank=True, null=True)),
                ('taille', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Taille (en cm)')),
                ('poids', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Poids (en kg)')),
                ('mere', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pensionnaires_mere', to='Model.mere_enfant')),
            ],
        ),
        migrations.CreateModel(
            name='Pere_enfant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_pere', models.CharField()),
                ('prenom_pere', models.CharField()),
                ('date_naissance_pere', models.DateField(blank=True, null=True)),
                ('lieu_naissance_pere', models.CharField(blank=True, null=True)),
                ('profession_pere', models.CharField(blank=True, null=True)),
                ('ethnie_pere', models.CharField(blank=True, null=True)),
                ('religion_pere', models.CharField(blank=True, null=True)),
                ('nombre_personne_charge_pere', models.CharField(blank=True, null=True)),
                ('contact_pere', models.CharField(blank=True, null=True)),
                ('adresse_pere', models.CharField(blank=True, null=True)),
                ('en_vie_pere', models.BooleanField(blank=True, default=True, null=True)),
                ('en_couple_pere', models.BooleanField(blank=True, default=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Repondant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField()),
                ('prenom', models.CharField()),
                ('nationalite', models.CharField(blank=True, null=True)),
                ('profession', models.CharField(blank=True, null=True)),
                ('ethnie', models.CharField(blank=True, null=True)),
                ('religion', models.CharField(blank=True, null=True)),
                ('contact', models.CharField(blank=True, null=True)),
                ('adresse', models.CharField(blank=True, null=True)),
                ('nombre_piece', models.CharField(blank=True, null=True)),
                ('type_eau', models.CharField(blank=True, null=True)),
                ('electrifie', models.BooleanField(blank=True, default=True, null=True)),
                ('revenu_mensuel', models.BooleanField(blank=True, default=False, null=True)),
                ('en_couple', models.BooleanField(blank=True, default=True, null=True)),
                ('lien_parente', models.CharField(blank=True, null=True)),
                ('type_habitat', models.CharField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('date_mise_a_jour', models.DateTimeField(auto_now=True, verbose_name='Date de mise a jour')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('nom', models.CharField(max_length=250, verbose_name='nom')),
                ('prenom', models.CharField(max_length=250)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('telephone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Numéro de téléphone')),
                ('last_activity', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=True)),
                ('dark_mode', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('roles', models.CharField(default='UTILISATEUR', max_length=20)),
                ('image', models.ImageField(blank=True, null=True, upload_to='ImagesGestionnaire/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SuiviMedicalTrimestriele',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trimestre', models.PositiveSmallIntegerField()),
                ('annee_scolaire', models.CharField(default='2024-2025', max_length=9)),
                ('taille_cm', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('poids_kg', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('pensionnaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suivis_medicaux', to='Model.pensionnnaire')),
            ],
        ),
        migrations.AddField(
            model_name='pensionnnaire',
            name='pere',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pensionnaires_pere', to='Model.pere_enfant'),
        ),
        migrations.AddField(
            model_name='pensionnnaire',
            name='repondant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pensionnaires_repondant', to='Model.repondant'),
        ),
        migrations.CreateModel(
            name='Parrain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField()),
                ('prenom', models.CharField()),
                ('date_naissance', models.DateField(blank=True, null=True)),
                ('date_parrainage', models.DateField(blank=True, null=True)),
                ('lieu_naissance', models.CharField(blank=True, null=True)),
                ('nationalite', models.CharField(blank=True, null=True)),
                ('profession', models.CharField(blank=True, null=True)),
                ('ethnie', models.CharField(blank=True, null=True)),
                ('religion', models.CharField(blank=True, null=True)),
                ('type_famille', models.CharField(blank=True, null=True)),
                ('charge_fixe', models.CharField(blank=True, null=True)),
                ('nombre_personne_charge', models.CharField(blank=True, null=True)),
                ('contact', models.CharField(blank=True, null=True)),
                ('adresse', models.CharField(blank=True, null=True)),
                ('nombre_piece', models.CharField(blank=True, null=True)),
                ('type_eau', models.CharField(blank=True, null=True)),
                ('electrifie', models.BooleanField(blank=True, default=True, null=True)),
                ('en_vie', models.BooleanField(blank=True, default=True, null=True)),
                ('en_couple', models.BooleanField(blank=True, default=True, null=True)),
                ('situation_matrimoniale', models.CharField(blank=True, null=True)),
                ('lien_parente', models.CharField(blank=True, null=True)),
                ('niveau_etude', models.CharField(blank=True, null=True)),
                ('type_habitat', models.CharField(blank=True, null=True)),
                ('enfant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Model.pensionnnaire')),
            ],
        ),
        migrations.CreateModel(
            name='Inscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ecole', models.CharField(blank=True, default='OGB', null=True)),
                ('date_inscription', models.DateField(auto_now_add=True)),
                ('classe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inscriptions', to='Model.classe')),
                ('pensionnaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inscriptions', to='Model.pensionnnaire')),
            ],
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evaluation1', models.IntegerField(blank=True, null=True)),
                ('evaluation2', models.IntegerField(blank=True, null=True)),
                ('evaluation3', models.IntegerField(blank=True, null=True)),
                ('moyenne', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('statut_final', models.CharField(max_length=20)),
                ('inscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluations', to='Model.inscription')),
            ],
        ),
        migrations.CreateModel(
            name='Dossier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fichier', models.FileField(upload_to='pensionnaires/dossiers/')),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('date_ajout', models.DateTimeField(auto_now_add=True)),
                ('pensionnaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dossiers', to='Model.pensionnnaire')),
            ],
        ),
        migrations.CreateModel(
            name='ConsultationMedicale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_consultation', models.DateField(auto_now_add=True)),
                ('motif_consultation', models.TextField(blank=True, null=True)),
                ('diagnostic', models.TextField(blank=True, null=True)),
                ('traitement', models.TextField(blank=True, null=True)),
                ('annee_scolaire', models.CharField(default='2024-2025', max_length=9)),
                ('pensionnaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultations_medicales', to='Model.pensionnnaire')),
            ],
        ),
        migrations.CreateModel(
            name='Antecedents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(blank=True, null=True)),
                ('psychopathologie', models.CharField(blank=True, null=True)),
                ('probleme', models.CharField(blank=True, null=True)),
                ('enfant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Model.pensionnnaire')),
            ],
        ),
        migrations.AddConstraint(
            model_name='suivimedicaltrimestriele',
            constraint=models.CheckConstraint(check=models.Q(('trimestre__in', [1, 2, 3])), name='valid_trimestre_values'),
        ),
        migrations.AlterUniqueTogether(
            name='suivimedicaltrimestriele',
            unique_together={('pensionnaire', 'trimestre', 'annee_scolaire')},
        ),
        migrations.AddConstraint(
            model_name='inscription',
            constraint=models.UniqueConstraint(fields=('pensionnaire', 'classe'), name='unique_pensionnaire_classe'),
        ),
        migrations.AddConstraint(
            model_name='evaluation',
            constraint=models.UniqueConstraint(fields=('inscription',), name='unique_evaluation_per_inscription'),
        ),
    ]
