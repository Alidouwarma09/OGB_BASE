from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Utilisateur

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
