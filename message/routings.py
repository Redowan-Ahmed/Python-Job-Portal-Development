from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(route=r"ws/chat/(?P<room_name>\w+)/$", view=consumers.ChatConsumer.as_asgi()),
]