from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(route="ws/chat/<str:room_name>/", view=consumers.ChatConsumer.as_asgi()),
]