# Name of code artifact: arducam-test.py 
# Brief description of what the code does: Scans barcodes using camera and opencv 
# Programmer’s name: Xavier uryle   
# Date the code was created: 2/20/25
# Preconditions: Camera available    
# Postconditions: Camera barcode scsanned and printed to screen 
# Return values or types, and their meanings: N/A
# Error and exception condition values or types that can occur, and their meanings: N/A
# Side effects: cv2 doesn't work if libcamera is also used 
# Invariants: N/A

# import cv2 # I don't know why cv2 doesn't work 
import zxingcpp
from libcamera import \
    controls  # might need to set include-system-packages to true in .venv/pyvenv.cfg to get this to work
from picamera2 import Picamera2, Preview

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
