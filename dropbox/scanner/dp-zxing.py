# Name of code artifact: dp-zxing.py 
# Brief description of what the code does: Scans barcodes using camera and opencv 
# Programmer’s name: Darshil Patel  
# Date the code was created: 2/20/25
# Preconditions: Camera available    
# Postconditions: Camera barcode scsanned and printed to screen 
# Return values or types, and their meanings: N/A
# Error and exception condition values or types that can occur, and their meanings: N/A
# Side effects: 
# Invariants: N/A

import queue
import threading
import time

import cv2
import zxingcpp

NUM_DECODER_THREADS = 2  # Increase based on your CPU cores

def decode_worker(frame_queue, result_queue):
    while True:
        frame = frame_queue.get()
        if frame is None:  # Shutdown signal
            frame_queue.task_done()
            break
        # Convert frame to grayscale for faster processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        results = zxingcpp.read_barcodes(gray)
        result_queue.put(results)
        frame_queue.task_done()

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open camera.")
        return

    # You can adjust the queue size as needed. A slightly larger queue
    # might help if decoding sometimes lags behind capture.
    frame_queue = queue.Queue(maxsize=4)
    result_queue = queue.Queue()

    # Start multiple decoder threads
    decoder_threads = []
    for _ in range(NUM_DECODER_THREADS):
        t = threading.Thread(target=decode_worker, args=(frame_queue, result_queue))
        t.daemon = True
        t.start()
        decoder_threads.append(t)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize the frame for faster processing. If possible, consider using a lower resolution.
        frame = cv2.resize(frame, (640, 480))

        # Enqueue the frame if there is space to avoid backlogging
        if not frame_queue.full():
            frame_queue.put(frame)

        # Process all available decoding results
        while not result_queue.empty():
            results = result_queue.get()
            for result in results:
                barcode_text = result.text
                barcode_format = result.format
                print(f"{barcode_format}: {barcode_text}")

                # Draw the bounding box around the barcode
                points = [
                    (result.position.top_left.x, result.position.top_left.y),
                    (result.position.top_right.x, result.position.top_right.y),
                    (result.position.bottom_right.x, result.position.bottom_right.y),
                    (result.position.bottom_left.x, result.position.bottom_left.y),
                ]
                for i in range(len(points)):
                    cv2.line(frame, tuple(points[i]), tuple(points[(i + 1) % len(points)]), (0, 255, 0), 2)
                cv2.putText(frame, f"{barcode_format}: {barcode_text}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Barcode Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Signal all worker threads to exit and wait for them to finish
    for _ in decoder_threads:
        frame_queue.put(None)
    frame_queue.join()
    for t in decoder_threads:
        t.join()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
