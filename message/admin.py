from django.contrib import admin
from .models import Message, TestModel, MessageRoom, RoomMessage
# Register your models here.

admin.site.register(model_or_iterable=Message)
admin.site.register(model_or_iterable=TestModel)

class RoomMessageAdmin(admin.ModelAdmin):
    list_display = ['room', 'messenger', 'body' ]
    search_fields = ['body','room__room_name', 'messenger__email']
    actions_on_bottom = True

admin.site.register(model_or_iterable=MessageRoom)
admin.site.register(model_or_iterable=RoomMessage, admin_class=RoomMessageAdmin)