import socket

import cv2
import numpy as np

UDP_IP = "127.0.0.1"  # Replace with Django server IP
UDP_PORT = 5005
DROPBOX_ID = 2
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)  # Or video file
# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))


while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))  # Down from e.g., 1920x1080


    # Encode frame as JPEG (adjust quality as needed)
    _, jpeg_data = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])

    # Convert to bytes and send
    sock.sendto(DROPBOX_ID.to_bytes() + b'|' + jpeg_data.tobytes(), (UDP_IP, UDP_PORT))

cap.release()
