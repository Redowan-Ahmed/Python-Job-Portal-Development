# Generated by Django 5.0 on 2023-12-28 05:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0008_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpost',
            name='company',
            field=models.ForeignKey(default='46821c24-d5d6-4d40-b426-3aebcfcedc85', on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='hr.company'),
        ),
    ]