# Generated by Django 4.2.13 on 2024-12-30 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Model', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parametre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.CharField(default='Bienvenue')),
                ('titre', models.CharField(default='Information', max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='OGB_Image/')),
            ],
        ),
    ]