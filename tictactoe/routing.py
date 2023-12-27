from django.urls import re_path

from .import consumers

websocket_urlpatterns = [
    re_path(r"ws/playing/(?P<room_code>\w+)/$", consumers.PlayConsumer.as_asgi()),
]