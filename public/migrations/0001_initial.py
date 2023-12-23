# Generated by Django 5.0 on 2023-12-23 20:45

import django.core.validators
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SupportContact',
            fields=[
                ('id', models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, verbose_name='Email Address')),
                ('phone_number', models.CharField(default=8801632398271, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{8,15}$')])),
                ('subject', models.CharField(max_length=300)),
                ('message', models.TextField(blank=True, max_length=5000)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
