import cv2
import zxingcpp
import threading
import queue
import time

def decode_worker(frame_queue, result_queue):
    """
    Worker thread that takes frames from the frame_queue,
    decodes barcodes, and puts the results into result_queue.
    """
    while True:
        frame = frame_queue.get()
        if frame is None:  # Shutdown signal
            break
        # Convert frame to grayscale for faster processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Decode barcodes using zxingcpp (this is a C++ library so it should release the GIL)
        results = zxingcpp.read_barcodes(gray)
        result_queue.put(results)
        frame_queue.task_done()

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open camera.")
        return

    # Create a small queue to buffer frames (small to reduce latency)
    frame_queue = queue.Queue(maxsize=2)
    result_queue = queue.Queue()

    # Start the decode worker thread
    decoder_thread = threading.Thread(target=decode_worker, args=(frame_queue, result_queue))
    decoder_thread.daemon = True
    decoder_thread.start()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize the frame for faster processing
        frame = cv2.resize(frame, (640, 480))

        # If there's space, push the frame for decoding.
        # If the queue is full, we skip this frame to maintain responsiveness.
        if not frame_queue.full():
            frame_queue.put(frame)

        # If there are any decoding results, process them
        if not result_queue.empty():
            results = result_queue.get()
            for result in results:
                barcode_text = result.text
                barcode_format = result.format
                print(f"{barcode_format}: {barcode_text}")

                # Get the corners of the barcode and draw a bounding box
                points = [
                    (result.position.top_left.x, result.position.top_left.y),
                    (result.position.top_right.x, result.position.top_right.y),
                    (result.position.bottom_right.x, result.position.bottom_right.y),
                    (result.position.bottom_left.x, result.position.bottom_left.y),
                ]
                for i in range(len(points)):
                    cv2.line(frame, tuple(points[i]), tuple(points[(i + 1) % len(points)]), (0, 255, 0), 2)
                # Display the barcode text on the frame
                cv2.putText(frame, f"{barcode_format}: {barcode_text}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Show the processed frame
        cv2.imshow("Barcode Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Signal the worker thread to exit and wait for it to finish
    frame_queue.put(None)
    decoder_thread.join()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
