# your_app/udp_receiver.py
import base64
import socket

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
            
            sender_id, jpeg_bytes = data.split(b'|', 1)  # Split at first '|'
            jpg_base64 = base64.b64encode(jpeg_bytes).decode('utf-8')
            sender_id_int = int.from_bytes(sender_id)
            
            # Broadcast to WebSocket clients
            async_to_sync(self.channel_layer.group_send)(
                "video_group",
                {
                    "type": "video.frame",
                    "frame": jpg_base64,
                    "sender_id": sender_id_int
                }
            )

        self.sock.shutdown(socket.SHUT_RDWR)  # Signal that we're done sending and receiving
        self.sock.close()  # Close the socket

# To start in Django
def start_udp_receiver():
    receiver = UDPVideoReceiver()
    receiver.start_receiving()

