# Name of code artifact: zxing-video.py 
# Brief description of what the code does: Scans barcodes using camera and opencv 
# Programmer’s name: Xavier Ruyle 
# Date the code was created: 2/20/25
# Preconditions: Camera available    
# Postconditions: Camera barcode scsanned and printed to screen 
# Return values or types, and their meanings: N/A
# Error and exception condition values or types that can occur, and their meanings: N/A
# Side effects: 
# Invariants: N/A


import cv2
import zxingcpp

cap = cv2.VideoCapture(0)
if not cap.isOpened(): 
    print('Cannot open Camera')
else: 
    print('Camera opened: ', cap)

'''
picam = Picamera2() 
picam.configure(picam.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam.start()
'''

while True:
    # Capture frame-by-frame
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame for faster processing (optional)
    frame = cv2.resize(frame, (640, 480)) 

    # Convert the frame to grayscale (optional but improves performance)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # gray = cv2.GaussianBlur(gray, (5, 5), 0)
    # gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)


    # Decode barcodes
    results = zxingcpp.read_barcodes(gray)

    # Process results
    for result in results:
        # Get the barcode text and type
        barcode_text = result.text
        barcode_format = result.format
        print(result, barcode_format, barcode_text)

        # Get the corners of the barcode
        points = [
            (result.position.top_left.x, result.position.top_left.y),
            (result.position.top_right.x, result.position.top_right.y),
            (result.position.bottom_right.x, result.position.bottom_right.y),
            (result.position.bottom_left.x, result.position.bottom_left.y),
        ]

        # Draw a bounding box around the barcode
        for i in range(len(points)):
            cv2.line(frame, tuple(points[i]), tuple(points[(i + 1) % len(points)]), (0, 255, 0), 2)

        # Put the barcode text and type on the frame
        cv2.putText(frame, f"{barcode_format}: {barcode_text}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame with detected barcodes
    cv2.imshow('Barcode Detection', frame) 

    # Exit on 'q' key press
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break 

# Release the video capture and close windows
cap.release()
cv2.destroyAllWindows()
