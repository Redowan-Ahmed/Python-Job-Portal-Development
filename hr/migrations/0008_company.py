# Generated by Django 5.0 on 2023-12-28 04:58

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0007_alter_jobcategory_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('company_name', models.CharField(max_length=150, unique=True)),
                ('company_logo', models.ImageField(upload_to='companies-logo')),
                ('location', models.CharField(max_length=300)),
                ('website', models.URLField(blank=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=50)),
                ('employ_volume_average', models.CharField(blank=True, choices=[('0 - 10', '0 - 10'), ('10 - 50', '10 - 50'), ('50 - 100', '50 - 100'), ('100 - 200', '100 - 200'), ('200+', '200+')], max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
