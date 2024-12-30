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
    if 'Model_parametre' in connection.introspection.table_names():
        if not Parametre.objects.filter(id=1).exists():
            Parametre.objects.create(
                id=1,
                info='Bienvenue',
                titre='Information',
                image='OGB_Image/img.png'
            )
            print("Parametre créé avec succès !")
