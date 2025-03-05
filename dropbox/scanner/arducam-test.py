# import cv2 # I don't know why cv2 doesn't work 
from picamera2 import Picamera2, Preview 
from libcamera import  controls  # might need to set include-system-packages to true in .venv/pyvenv.cfg to get this to work 
import zxingcpp


cam = Picamera2()
height = 480
width = 640
middle = (int(width / 2), int(height / 2))
cam.configure(cam.create_video_configuration(main={"format": 'RGB888', "size": (width, height)}))
cam.start_preview(Preview.QT, x=100, y=200, width=width, height=height)

cam.start()

while True:
        frame = cam.capture_array()
        results = zxingcpp.read_barcodes(frame)
        for result in results: 
            print(result, result.text) 
