from django.urls import path
from mainsite.consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/', ChatConsumer),
]
