import socket
import subprocess as sp

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# FFmpeg command to capture camera and output MJPEG over stdout
ffmpeg_cmd = [
    'ffmpeg',
    '-f', 'v4l2',              # Input format (Linux camera)
    '-i', '/dev/video0',       # Camera device
    '-vf', 'scale=320:240',    # Resize
    '-f', 'mjpeg',             # Output format (Motion JPEG)
    '-q:v', '4',               # Quality (2-31, lower is better)
    '-'                        # Output to stdout
]

process = sp.Popen(ffmpeg_cmd, stdout=sp.PIPE, stderr=sp.PIPE, bufsize=10**8)

while True:
    # Read JPEG data from FFmpeg stdout
    # Note: This simple approach might need more robust frame boundary detection
    jpeg_data = process.stdout.read(65536)  # Max UDP packet size
    if not jpeg_data:
        break
    
    # print(jpeg_data.__sizeof__())
    # Send over UDP
    sock.sendto(jpeg_data, (UDP_IP, UDP_PORT))

process.terminate()
