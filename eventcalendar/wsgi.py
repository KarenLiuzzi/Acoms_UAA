"""
WSGI config for eventcalendar project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from eventcalendar import routing

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywebsite.settings')

# application = ProtocolTypeRouter({
#     'http':get_asgi_application(),
#     'websocket':AuthMiddlewareStack(
#         URLRouter(
#             routing.websocket_urlpatterns
#         )
#     )
# })


import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eventcalendar.settings")

application = get_wsgi_application()