"""
ASGI config for funi project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import ws_pattern

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "funi.settings")

http_response_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': http_response_app,
    'websocket': URLRouter(ws_pattern)
})
