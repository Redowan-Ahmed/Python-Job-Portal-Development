# Generated by Django 5.0 on 2024-01-02 01:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0008_alter_comment_reply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='public.comment'),
        ),
    ]
