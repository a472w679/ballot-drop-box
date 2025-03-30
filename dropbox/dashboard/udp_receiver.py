# your_app/udp_receiver.py
import base64
import socket
import struct

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
        MIN_PACKET_SIZE = 8 
        while True:
            data, addr = self.sock.recvfrom(65536)  # Max UDP packet size

            # Check if packet is too small
            if len(data) < MIN_PACKET_SIZE:
                # print(f"Packet too small: {len(data)} bytes")
                continue 
            
            # Verify that there enough data for the claimed JPEG size
            try:
                sender_id = struct.unpack('!I', data[:4])[0]
                jpeg_size = struct.unpack('!I', data[4:8])[0]
            except struct.error:
                continue 
                
            # 3. Check if jpeg_size is reasonable
            if jpeg_size > 10 * 1024 * 1024:  # 10MB max
                continue 
                
            #  Verify complete JPEG data was received
            if len(data) < 8 + jpeg_size:
                # print(f"Incomplete JPEG data. Expected {8+jpeg_size}, got {len(data)}")
                continue 
                
            # Extract and validate JPEG data
            jpeg_bytes = data[8:8+jpeg_size]
            
            # Verify JPEG header (starts with 0xFFD8)
            if len(jpeg_bytes) < 2 or jpeg_bytes[0] != 0xFF or jpeg_bytes[1] != 0xD8:
                # print("Incorrect JPEG format")
                continue 


            # encode jpg data to b64 
            jpg_base64 = base64.b64encode(jpeg_bytes).decode('utf-8')

            
            # Broadcast to WebSocket clients
            async_to_sync(self.channel_layer.group_send)(
                "video_group",
                {
                    "type": "video.frame",
                    "frame": jpg_base64,
                    "sender_id": sender_id
                }
            )

        self.sock.shutdown(socket.SHUT_RDWR)  # Signal that we're done sending and receiving
        self.sock.close()  # Close the socket

# To start in Django
def start_udp_receiver():
    receiver = UDPVideoReceiver()
    receiver.start_receiving()

