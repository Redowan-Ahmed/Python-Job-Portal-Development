from django.contrib import admin
from .models import Message, TestModel, MessageRoom, RoomMessage
# Register your models here.

admin.site.register(model_or_iterable=Message)
admin.site.register(model_or_iterable=TestModel)
admin.site.register(model_or_iterable=MessageRoom)
admin.site.register(model_or_iterable=RoomMessage)