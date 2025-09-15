from django.urls import path
from .consumers import ChatConsumer,PresenceConsumer

websocket_urlpatterns = [
    path('ws/notification/<str:room_name>/', ChatConsumer.as_asgi()),
    path(r'ws/presence/$', PresenceConsumer.as_asgi()),

]