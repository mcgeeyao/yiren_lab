"""
ASGI config for myweb project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
import channels.layers

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myweb.settings')
channel_layer = channels.layers.get_channel_layer()
application = get_asgi_application()
