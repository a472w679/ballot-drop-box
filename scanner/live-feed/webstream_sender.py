import os
import socket
import struct

import cv2
import yaml


def send_jpeg_stream_data(): 
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    with open(os.path.join(parent_dir, "config.yaml"), 'r') as file:
        config = yaml.safe_load(file)

    UDP_IP = config["server"]["host"]  # Django server IP
    UDP_PORT = config["server"]["live_feed_port"]
    DROPBOX_ID = config["dropbox"]["id"] # The dropbox id tab you want to send live feed to 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"Webstreamer: Established socket with {UDP_IP}:{UDP_PORT} as Dropbox ID {DROPBOX_ID}")

    cap = cv2.VideoCapture(0)  # Or video file

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (640, 480))  # downscale 

        # Encode frame as JPEG
        _, jpeg_data = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])


        # Packed Data: [4-byte integer, 4-byte jpeg size, jpeg data of len(jpeg_data) size]
        packed_data = struct.pack('!I', DROPBOX_ID)
        packed_data += struct.pack('!I', len(jpeg_data))  
        packed_data += jpeg_data.tobytes()  # Add the actual jpeg data
        sock.sendto(packed_data, (UDP_IP, UDP_PORT))

    print("released") 
    cap.release()

if __name__ == "__main__": 
    send_jpeg_stream_data()
