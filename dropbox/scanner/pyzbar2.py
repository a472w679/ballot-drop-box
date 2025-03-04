import cv2
import numpy as np
from pyzbar.pyzbar import decode

def process_frame(frame):
    """
    Pre-process the frame to enhance barcode features under poor lighting.
    Steps include:
      - Resizing for consistent processing speed.
      - Conversion to grayscale.
      - Contrast enhancement via histogram equalization.
      - Gaussian blur to reduce noise.
      - Adaptive thresholding to improve local contrast.
    
    Returns:
      - thresh: The pre-processed binary image.
      - resized: The resized color image for annotation/display.
    """
    # Resize for consistency and faster processing
    resized = cv2.resize(frame, (640, 480))
    
    # Convert to grayscale
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    
    # Enhance contrast
    gray_eq = cv2.equalizeHist(gray)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray_eq, (5, 5), 0)
    
    # Adaptive thresholding for local contrast enhancement
    thresh = cv2.adaptiveThreshold(blurred, 255,
                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
    return thresh, resized

def detect_barcode(frame):
    """
    Processes a frame and attempts to decode barcodes using pyzbar.
    
    Returns:
      - results: A list of detected barcode objects (or None if none found).
      - annotated_frame: The frame with bounding boxes and text drawn (if a barcode is found).
    """
    processed, annotated_frame = process_frame(frame)
    results = decode(processed)
    
    if results:
        for result in results:
            barcode_text = result.data.decode("utf-8")
            barcode_type = result.type
            
            # Get the location of the barcode and draw a bounding box
            (x, y, w, h) = result.rect
            cv2.rectangle(annotated_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(annotated_frame, f"{barcode_type}: {barcode_text}",
                        (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)
        return results, annotated_frame
    return None, annotated_frame

def main():
    cap = cv2.VideoCapture(0)  # Change the index if needed.
    if not cap.isOpened():
        print("Failed to open camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results, annotated_frame = detect_barcode(frame)
        
        # If barcode is detected, print details (you could also save the image, etc.)
        if results:
            for result in results:
                barcode_text = result.data.decode("utf-8")
                barcode_type = result.type
                print(f"Detected {barcode_type}: {barcode_text}")
                # Optionally, save the annotated frame:
                # cv2.imwrite("barcode_detected.jpg", annotated_frame)

        # Display the processed frame
        cv2.imshow("Barcode Scanning", annotated_frame)
        
        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
