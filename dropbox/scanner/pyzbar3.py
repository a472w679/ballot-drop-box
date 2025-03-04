import cv2
import numpy as np
from pyzbar.pyzbar import decode
import threading
import queue

def process_frame(frame):
    """
    Pre-process the frame to reduce noise and enhance barcode features.
    Steps:
      1. Resize to 640x480 for a good balance between resolution and speed.
      2. Convert to grayscale.
      3. Apply bilateral filtering to smooth noise while preserving edges.
      4. Apply median blur to further reduce salt-and-pepper noise.
      5. Enhance contrast via histogram equalization.
      6. Use adaptive thresholding to create a binary image.
      7. Perform morphological closing to fill gaps.
    
    Returns:
      - processed: the final processed binary image for decoding.
      - display_frame: the resized color frame for annotation.
    """
    # Resize for consistent processing
    display_frame = cv2.resize(frame, (640, 480))
    
    # Convert to grayscale
    gray = cv2.cvtColor(display_frame, cv2.COLOR_BGR2GRAY)
    
    # Bilateral filter preserves edges while reducing noise
    filtered = cv2.bilateralFilter(gray, 9, 75, 75)
    
    # Median blur to remove salt-and-pepper noise
    median = cv2.medianBlur(filtered, 5)
    
    # Enhance contrast using histogram equalization
    equalized = cv2.equalizeHist(median)
    
    # Adaptive thresholding to generate a binary image
    thresh = cv2.adaptiveThreshold(equalized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
    
    # Morphological closing to fill small gaps and further reduce noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    return closed, display_frame

def barcode_worker(frame_queue, result_queue):
    """
    Worker thread that takes frames from frame_queue,
    pre-processes them, decodes barcodes using pyzbar,
    and puts the result into result_queue.
    """
    while True:
        frame = frame_queue.get()
        if frame is None:  # Shutdown signal
            break
        processed, annotated_frame = process_frame(frame)
        results = decode(processed)
        result_queue.put((results, annotated_frame))
        frame_queue.task_done()

def main():
    cap = cv2.VideoCapture(0)  # Adjust the index if needed
    if not cap.isOpened():
        print("Error: Unable to open camera.")
        return
    
    # Use small queues to ensure processing of fresh frames
    frame_queue = queue.Queue(maxsize=2)
    result_queue = queue.Queue()
    
    # Start the worker thread
    worker_thread = threading.Thread(target=barcode_worker, args=(frame_queue, result_queue))
    worker_thread.daemon = True
    worker_thread.start()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Continuously add frames to the queue (skip if full)
        if not frame_queue.full():
            frame_queue.put(frame)
        
        # Check if there are any processed results available
        if not result_queue.empty():
            results, annotated_frame = result_queue.get()
            if results:
                for result in results:
                    barcode_text = result.data.decode("utf-8")
                    barcode_type = result.type
                    (x, y, w, h) = result.rect
                    cv2.rectangle(annotated_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(annotated_frame, f"{barcode_type}: {barcode_text}",
                                (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    print(f"Detected {barcode_type}: {barcode_text}")
                cv2.imshow("Barcode Detected", annotated_frame)
            else:
                # Show the processed frame if no barcode is found, for debugging
                cv2.imshow("Live Feed", annotated_frame)
        else:
            # If no processed frame is ready, show a downsized live feed
            cv2.imshow("Live Feed", cv2.resize(frame, (320, 240)))
        
        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Cleanup: signal the worker thread to stop
    frame_queue.put(None)
    worker_thread.join()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
