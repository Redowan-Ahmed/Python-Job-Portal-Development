import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from message.routings import websocket_urlpatterns

os.environ.setdefault(key="DJANGO_SETTINGS_MODULE", value="mysite.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

import message.routings

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            application=AuthMiddlewareStack(inner=URLRouter(routes=websocket_urlpatterns))
        ),
    }
)