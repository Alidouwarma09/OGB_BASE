from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Utilisateur, Parametre
from django.db import connection


@receiver(post_migrate)
def create_default_admin(sender, **kwargs):
    if not Utilisateur.objects.filter(username='admin').exists():
        Utilisateur.objects.create_user(
            username='admin',
            password='09102079Darius',
            nom='Admin',
            prenom='Super',
            email='alidouwrm@gmail.com',
            roles='ADMIN',
            is_admin=True,
            is_staff=True,
        )
        print("Utilisateur admin créé avec succès !")


@receiver(post_migrate)
def create_default_parametre(sender, **kwargs):
    # Vérifie si la table existe dans la base de données
    if 'Model_parametre' in connection.introspection.table_names():
        # Vérifie si une instance existe déjà
        if not Parametre.objects.filter(id=1).exists():
            Parametre.objects.create(
                id=1,
                info='Bienvenue',
                titre='Information',
            )
            print("Parametre créé avec succès !")
