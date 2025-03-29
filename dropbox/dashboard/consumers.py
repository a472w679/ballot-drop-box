# your_app/consumers.py
import base64
import json

import cv2
import numpy as np
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer


class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("video_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("video_group", self.channel_name)

    async def receive(self, text_data):
        pass  # Not needed for this use case

    async def video_frame(self, event):
        await self.send(text_data=json.dumps({
            'frame': event['frame']
        }))



