"""
ASGI config for awacs project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from awacs.websocket import websocket_middleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'awacs.settings')

application = get_asgi_application()
application = websocket_middleware(application)
