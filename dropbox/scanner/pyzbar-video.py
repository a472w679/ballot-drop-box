import cv2
from pyzbar.pyzbar import decode
import threading
import queue

def decode_worker(frame_queue, result_queue):
    """
    Worker thread that processes frames from the frame_queue,
    decodes barcodes using pyzbar, and puts the results in result_queue.
    """
    while True:
        frame = frame_queue.get()
        if frame is None:  # Shutdown signal
            break
        # Convert frame to grayscale for faster processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        results = decode(gray)
        result_queue.put(results)
        frame_queue.task_done()

def main():
    # Open the camera (0 is typically the default camera)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open camera.")
        return

    # Create a small queue to hold frames (to avoid lag)
    frame_queue = queue.Queue(maxsize=2)
    result_queue = queue.Queue()

    # Start the decoding thread
    decoder_thread = threading.Thread(target=decode_worker, args=(frame_queue, result_queue))
    decoder_thread.daemon = True
    decoder_thread.start()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize frame for faster processing
        frame = cv2.resize(frame, (640, 480))

        # If the queue isn't full, add the current frame for decoding
        if not frame_queue.full():
            frame_queue.put(frame)

        # Check if there are any decoding results available
        if not result_queue.empty():
            results = result_queue.get()
            for result in results:
                barcode_text = result.data.decode("utf-8")
                barcode_type = result.type
                print(f"{barcode_type}: {barcode_text}")

                # Draw bounding box around the barcode (result.rect returns (x, y, w, h))
                (x, y, w, h) = result.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # Put the barcode text on the frame
                cv2.putText(frame, f"{barcode_type}: {barcode_text}", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the frame with detected barcodes
        cv2.imshow("Barcode Detection with Pyzbar", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Shutdown: signal the worker thread and wait for it to finish
    frame_queue.put(None)
    decoder_thread.join()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
