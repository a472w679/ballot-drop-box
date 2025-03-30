from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/video/(?P<dropbox_id>\d+)$', consumers.VideoConsumer.as_asgi()),
]
