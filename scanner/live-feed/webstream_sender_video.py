import os
import socket
import struct
import subprocess

import cv2
import numpy as np
import yaml


def send_webm_stream_data():
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    with open(os.path.join(parent_dir, "config.yaml"), 'r') as file:
        config = yaml.safe_load(file)

    UDP_IP = config["server"]["host"]
    UDP_PORT = config["server"]["live_feed_port"]
    DROPBOX_ID = config["dropbox"]["id"]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"Webstreamer: Established socket with {UDP_IP}:{UDP_PORT} as Dropbox ID {DROPBOX_ID}")

    cap = cv2.VideoCapture(0)  # Or video file
    
    # WebM configuration
    fps = 20
    width, height = 640, 480
    chunk_size = 10  # Number of frames per WebM chunk
    
    # FFmpeg command to encode WebM in memory (no disk writing)
    ffmpeg_cmd = [
        'ffmpeg',
        '-y',  # Overwrite without asking
        '-f', 'rawvideo',
        '-vcodec', 'rawvideo',
        '-pix_fmt', 'bgr24',
        '-s', f'{width}x{height}',
        '-r', str(fps),
        '-i', '-',  # Read from stdin
        '-c:v', 'libvpx',  # VP8 codec (WebM)
        '-f', 'webm',
        '-crf', '30',  # Quality (lower = better, 10-50)
        '-deadline', 'realtime',  # Faster encoding
        '-cpu-used', '4',  # Faster encoding (0-5)
        '-',  # Output to stdout
    ]

    # Start FFmpeg process
    ffmpeg_proc = subprocess.Popen(
        ffmpeg_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    frame_count = 0
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (width, height))
            ffmpeg_proc.stdin.write(frame.tobytes())
            frame_count += 1

            if frame_count >= chunk_size:
                # Signal FFmpeg to flush the current chunk
                ffmpeg_proc.stdin.flush()
                
                # Read the WebM chunk from FFmpeg's stdout
                webm_data = ffmpeg_proc.stdout.read()  # May need buffering adjustments
                print(webm_data)
                
                if webm_data:
                    # Pack and send the data
                    packed_data = struct.pack('!I', DROPBOX_ID)
                    packed_data += struct.pack('!I', len(webm_data))
                    packed_data += webm_data
                    sock.sendto(packed_data, (UDP_IP, UDP_PORT))
                
                frame_count = 0

    finally:
        print("released")
        cap.release()
        ffmpeg_proc.stdin.close()
        ffmpeg_proc.terminate()
        ffmpeg_proc.wait()

if __name__ == "__main__":
    send_webm_stream_data()
