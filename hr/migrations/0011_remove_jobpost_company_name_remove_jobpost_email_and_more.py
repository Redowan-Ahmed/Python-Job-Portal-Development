# Generated by Django 5.0 on 2023-12-28 05:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0010_alter_company_company_name_alter_company_location_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobpost',
            name='company_name',
        ),
        migrations.RemoveField(
            model_name='jobpost',
            name='email',
        ),
        migrations.RemoveField(
            model_name='jobpost',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='company',
            name='phone_number',
            field=models.CharField(blank=True, default='+0000000000', max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{8,15}$')]),
        ),
    ]
