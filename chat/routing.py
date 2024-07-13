from django.urls import path
from .consumers import ChatConsumer

ws_pattern = [
    path("ws/message/<str:room_name>/", ChatConsumer.as_asgi())
]