# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chatGame/(?P<room_name>\w+)/(?P<color>\w+)$', consumers.GameConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>\w+)/(?P<color>\w+)/(?P<username>\w+)$', consumers.ChatConsumer.as_asgi()),
]
