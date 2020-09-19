from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import OriginValidator,AllowedHostsOriginValidator
import mainsite.routing

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
        
            URLRouter(
                mainsite.routing.websocket_urlpatterns
            )
        )
    ),
})


