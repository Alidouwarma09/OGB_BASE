# Generated by Django 5.0.4 on 2024-12-06 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Model', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultationmedicale',
            name='annee_scolaire',
            field=models.CharField(default='2024-2025', max_length=9),
        ),
        migrations.AlterField(
            model_name='consultationmedicale',
            name='date_consultation',
            field=models.DateField(auto_now_add=True),
        ),
    ]