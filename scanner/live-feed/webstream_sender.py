import os
import socket
import struct

import cv2
import yaml

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
with open(os.path.join(parent_dir, "config.yaml"), 'r') as file:
    config = yaml.safe_load(file)

UDP_IP = config["server"]["host"]  # Django server IP
UDP_PORT = config["server"]["live_feed_port"]
DROPBOX_ID = config["dropbox"]["id"] # The dropbox id tab you want to send live feed to 

def send_jpeg_stream_data_on_motion():
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
            if cv2.contourArea(c) > 2000:  # motion is significant 
                motion_detected = True
        
        _, jpeg_data = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
        packed_data = struct.pack('!I', DROPBOX_ID)
        packed_data += struct.pack('!I', len(jpeg_data))  
        packed_data += struct.pack('?', motion_detected)
        packed_data += jpeg_data.tobytes()  # Add the actual jpeg data
        # Encode frame as JPEG (adjust quality as needed)


        sock.sendto(packed_data, (UDP_IP, UDP_PORT))

    cap.release()


def send_jpeg_stream_data(): 
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

    cap.release()

if __name__ == "__main__": 
    # send_jpeg_stream_data()
    send_jpeg_stream_data_on_motion()
