# Generated by Django 5.0 on 2024-01-01 22:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_hrprofile_company'),
        ('hr', '0014_alter_company_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hrprofile',
            name='company',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='hr.company'),
        ),
    ]
