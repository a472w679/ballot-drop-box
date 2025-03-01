import cv2
import zxingcpp

# Initialize the video capture (0 for webcam, or replace with a video file path)
cap = cv2.VideoCapture(0)

while True:
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
        print(barcode_format, barcode_text)

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
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close windows
cap.release()
cv2.destroyAllWindows()
