# Name of code artifact: scanning.py 
# Brief description of what the code does: Uses camera to detect when there is motion  
# Programmer’s name: Xavier Ruyle   
# Date the code was created: 3/24/25
# Preconditions: Camera
# Postconditions: 
# Return values or types, and their meanings: N/A
# Error and exception condition values or types that can occur, and their meanings: N/A
# Side effects: 
# Invariants: N/A

from datetime import datetime

import cv2
import numpy as np

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
    
    # 1. Apply background subtraction
    fgmask = fgbg.apply(frame)
    
    # 2. Remove noise and enhance detection
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    fgmask = cv2.dilate(fgmask, kernel, iterations=2)
    
    # 3. Find contours of moving objects
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 4. Draw bounding boxes around motion
    motion_detected = False
    for c in contours:
        if cv2.contourArea(c) > 1000:  # Only consider significant motion
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            motion_detected = True
    
    # 5. Display status
    status = "Motion Detected!" if motion_detected else "Monitoring..."
    cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # Show all windows
    # cv2.imshow("Live Camera", frame)
    # cv2.imshow("Motion Mask", fgmask)
    if motion_detected: 
        print("motion detected", datetime.now())
    
    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
