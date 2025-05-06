import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sstore.settings")
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from page_views.middleware import TokenAuthMiddleware
import api.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddleware(
        URLRouter(
            api.routing.websocket_urlpatterns
        )
    ),
})
