from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/video/1$', consumers.VideoConsumer.as_asgi()),
    re_path(r'^ws/video/2$', consumers.VideoConsumer.as_asgi()),
]
