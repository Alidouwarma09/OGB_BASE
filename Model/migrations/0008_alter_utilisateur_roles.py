# Generated by Django 5.0.4 on 2024-12-12 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Model', '0007_utilisateur_last_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='roles',
            field=models.CharField(default='UTILISATEUR', max_length=20),
        ),
    ]
