import cv2
import zxingcpp
import numpy as np
import threading
import queue
import time

# Global variables for debouncing detections.
last_detected_barcode = None
detection_count = 0
DETECTION_THRESHOLD = 3  # Require 3 consecutive frames with the same code.


def process_frame(frame, method=0):
    """
    Pre-process the frame using one of several methods.

    Methods:
      0: Minimal processing (grayscale + histogram equalization)
      1: Slight Gaussian blur + histogram equalization
      2: Adaptive thresholding on grayscale

    Returns:
      - processed: Processed image for ZXing scanning.
      - display_frame: The resized original frame for annotation.
    """
    display_frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(display_frame, cv2.COLOR_BGR2GRAY)

    if method == 0:
        processed = cv2.equalizeHist(gray)
    elif method == 1:
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        processed = cv2.equalizeHist(blurred)
    elif method == 2:
        processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY, 11, 2)
    else:
        processed = gray

    return processed, display_frame


def barcode_worker(frame_queue, result_queue, max_processing_time=1.0):
    """
    Worker thread that attempts to detect barcodes using different
    pre-processing methods. If processing takes longer than max_processing_time
    seconds, it gives up on that frame.
    """
    while True:
        frame = frame_queue.get()
        if frame is None:
            break

        start_time = time.time()
        results = None
        annotated_frame = None
        processed = None

        # Try several pre-processing methods.
        for method in range(3):
            processed, annotated_frame = process_frame(frame, method=method)
            try:
                results = zxingcpp.read_barcodes(processed)
            except Exception as e:
                print(f"Error scanning barcode with method {method}: {e}")
                results = None
            if results:
                break  # Stop if we get a valid result.
            if time.time() - start_time > max_processing_time:
                print("Processing timed out for this frame.")
                break

        result_queue.put((results, annotated_frame, processed))
        frame_queue.task_done()


def main():
    global last_detected_barcode, detection_count

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    frame_queue = queue.Queue(maxsize=2)
    result_queue = queue.Queue()

    worker_thread = threading.Thread(target=barcode_worker, args=(frame_queue, result_queue))
    worker_thread.daemon = True
    worker_thread.start()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if not frame_queue.full():
            frame_queue.put(frame)

        if not result_queue.empty():
            results, annotated_frame, processed = result_queue.get()

            if results:
                # We'll work with the first detected barcode.
                result = results[0]
                barcode_text = result.text
                barcode_format = result.format

                # Compute bounding box from the barcode's position, if available.
                try:
                    tl = result.position.top_left
                    tr = result.position.top_right
                    br = result.position.bottom_right
                    bl = result.position.bottom_left
                    x = min(tl.x, tr.x, br.x, bl.x)
                    y = min(tl.y, tr.y, br.y, bl.y)
                    w = max(tl.x, tr.x, br.x, bl.x) - x
                    h = max(tl.y, tr.y, br.y, bl.y) - y
                    # If the detected bounding box is very small, ignore it.
                    if w * h < 500:
                        results = None
                except Exception as e:
                    # If we can't compute a bounding box, skip filtering.
                    print(f"Error computing bounding box: {e}")

                # Debounce: check for consecutive detections.
                if results:
                    if barcode_text == last_detected_barcode:
                        detection_count += 1
                    else:
                        last_detected_barcode = barcode_text
                        detection_count = 1

                    if detection_count >= DETECTION_THRESHOLD:
                        # Annotate using the position data.
                        try:
                            points = [
                                (result.position.top_left.x, result.position.top_left.y),
                                (result.position.top_right.x, result.position.top_right.y),
                                (result.position.bottom_right.x, result.position.bottom_right.y),
                                (result.position.bottom_left.x, result.position.bottom_left.y),
                            ]
                            for i in range(len(points)):
                                cv2.line(annotated_frame, points[i], points[(i + 1) % len(points)], (0, 255, 0), 2)
                        except Exception as e:
                            print(f"Error drawing bounding box: {e}")
                        cv2.putText(annotated_frame, f"{barcode_format}: {barcode_text}", (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        print(f"Confirmed detection: {barcode_format}: {barcode_text}")
                        cv2.imshow("Barcode Detected", annotated_frame)
                        # Reset the debounce counters after confirmation.
                        last_detected_barcode = None
                        detection_count = 0
                    else:
                        print(f"Detected {barcode_format}: {barcode_text} (count {detection_count})")
                        cv2.imshow("Barcode (Not Confirmed)", annotated_frame)
                else:
                    # Clear debounce if detection was filtered out.
                    last_detected_barcode = None
                    detection_count = 0
            else:
                cv2.imshow("Live Feed", cv2.resize(frame, (320, 240)))

            # Display the processed image for debugging.
            cv2.imshow("Processed", processed)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    frame_queue.put(None)
    worker_thread.join()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
