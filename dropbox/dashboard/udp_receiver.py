# your_app/udp_receiver.py
import base64
import json
import socket

import cv2
import numpy as np
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class UDPVideoReceiver:
    def __init__(self):
        self.udp_ip = "0.0.0.0"
        self.udp_port = 5005
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.udp_ip, self.udp_port))
        self.channel_layer = get_channel_layer()

    def start_receiving(self):
        print(f"UDP receiver started on port {self.udp_port}")
        while True:
            data, addr = self.sock.recvfrom(65536)  # Max UDP packet size
            
            # Convert bytes to numpy array
            nparr = np.frombuffer(data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Convert frame to JPEG and base64
            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')
            
            # Broadcast to WebSocket clients
            async_to_sync(self.channel_layer.group_send)(
                "video_group",
                {
                    "type": "video.frame",
                    "frame": jpg_as_text
                }
            )

# To start in Django
def start_udp_receiver():
    receiver = UDPVideoReceiver()
    receiver.start_receiving()
