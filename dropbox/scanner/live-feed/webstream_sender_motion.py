import socket
from datetime import datetime

import cv2
import numpy as np

UDP_IP = "127.0.0.1"  # Replace with Django server IP
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Initialize webcam
cap = cv2.VideoCapture(0)

# Create background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=False)

# Kernel for noise removal
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.resize(frame, (640, 480))  

    # Apply background subtraction
    fgmask = fgbg.apply(frame)
    
    # Remove noise and enhance detection
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    fgmask = cv2.dilate(fgmask, kernel, iterations=2)
    
    # contours of moving objects
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    motion_detected = False
    for c in contours:
        if cv2.contourArea(c) > 500:  # motion is significant 
            motion_detected = True
    
    if motion_detected: 
    # Encode frame as JPEG (adjust quality as needed)
        _, jpeg_data = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
        sock.sendto(jpeg_data.tobytes(), (UDP_IP, UDP_PORT))
        # print("motion detected", datetime.now())
