# Generated by Django 5.0 on 2024-01-01 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0002_category_blogpost_comment_postlike'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='slug',
            field=models.SlugField(default='14', max_length=500),
        ),
    ]
