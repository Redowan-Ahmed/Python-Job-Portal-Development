# Generated by Django 5.0 on 2024-01-03 21:00

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0002_favoritejobs'),
        ('hr', '0015_alter_jobpost_description_alter_jobpost_requirements'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FavoriteJobs',
            new_name='FavoriteJob',
        ),
    ]
