# Generated by Django 5.0 on 2024-02-07 19:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0003_alter_message_user_messageroom_roommessage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='messageroom',
            name='room_name',
            field=models.CharField(blank=True, default='Privet', max_length=100),
        ),
        migrations.AddField(
            model_name='messageroom',
            name='user',
            field=models.ManyToManyField(blank=True, related_name='chat_rooms', to=settings.AUTH_USER_MODEL),
        ),
    ]