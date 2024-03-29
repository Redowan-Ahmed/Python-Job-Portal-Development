from django.db import models
from base.model import BaseModel
from django.contrib.auth import get_user_model
# Create your models here.
from django_cryptography.fields import encrypt


class Message(BaseModel):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='messag')
    sender = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='from_user')
    receiver = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='to_user')
    content = models.TextField(null=True)
    is_read = models.BooleanField(default=False)

    def senderMessage(from_user, to_user, content):
        sender_message = Message(
            user=from_user, sender=from_user, receiver=to_user, content=content, is_read=True)
        sender_message.save()

        receiver_message = Message(
            user=to_user,
            sender=from_user,
            receiver=from_user,
            content=content,
            is_read=True
        )

        receiver_message.save()

        return sender_message

    def get_message(user):
        users = []
        messages = Message.objects.filter(user = user).values('receiver').annotate(last = models.Max('created_at')).order_by('-last')
        for message in messages:
            users.append({
                'user': get_user_model().objects.get(pk=message['receiver']),
                'last_message': message['last'],
                'unread': Message.objects.filter(
                    user=user, is_read=False, receiver=message['receiver']).count()
            })
        return users

    def __str__(self) -> str:
        return self.user.email



class TestModel(BaseModel):
    name = models.CharField(max_length=50)
    sensitive_data = encrypt(models.CharField(max_length=50))

    def __str__(self):
        return self.name


class MessageRoom(BaseModel):
    users = models.ManyToManyField(to=get_user_model(), related_name='chat_rooms', blank=True)
    room_name = models.CharField(max_length=100, blank=True, default='Privet')
    is_group = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f'{self.pk} ({self.room_name})'

class RoomMessage(BaseModel):
    room = models.ForeignKey(MessageRoom, on_delete=models.CASCADE, related_name="messages")
    messenger = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='messages')
    body = models.TextField(blank=True)
    is_deleted = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f'{self.room.pk } ({self.room.room_name})'

    class Meta:
        ordering = ('created_at',)