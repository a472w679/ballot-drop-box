import cv2
import RPi.GPIO as GPIO
import time

''' The angles, timings, and thresholds below are estimates
assuming typical servo behavior, as the parts have not been acquired yet.
Advising that calibration is necessary when the actual components are available.'''

# Setting up servo configuration
SERVO_PIN = 18  # Specifying GPIO pin connected to the servo signal
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Initializing PWM on the servo pin at 50Hz, this is typical for servos
pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)  # Starting PWM at neutral position

def set_servo_angle(angle):
    """
    Setting the servo to a given angle.
    Using a conversion formula (duty_cycle = 2 + angle/18) that may need calibration.
    """
    duty_cycle = 2 + (angle / 18.0)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)  # Allowing time for the servo to reach the target position
    pwm.ChangeDutyCycle(0)  # Stopping PWM signal to reduce jitter

def trigger_servo():
    """
    Operating the gate to let an envelope pass and then closing it.
    """
    open_angle = 90   # Calibrating the angle to allow the envelope to pass through
    closed_angle = 0  # Calibrating the closed position for the dropbox
    set_servo_angle(open_angle)
    time.sleep(1)  # Maintaining the gate open long enough for an envelope to pass
    set_servo_angle(closed_angle)

# Configuring camera setup
cap = cv2.VideoCapture(0)  # Selecting the appropriate camera index

# Setting camera resolution (adjusting based on camera specifications)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Adjusting exposure settings for low-light conditions if supported
# cap.set(cv2.CAP_PROP_EXPOSURE, -6)  # Tuning exposure value as necessary

# Establishing envelope detection parameters
MIN_CONTOUR_AREA = 5000  # Defining minimum contour area to consider as an envelope
last_trigger_time = 0    # Initializing time for debouncing triggers
trigger_cooldown = 2     # Defining minimum seconds between triggers

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame from camera")
            break

        # Converting the frame to grayscale and blurring to reduce noise
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Applying adaptive thresholding to account for uneven low-light conditions
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 11, 2)

        # Detecting contours in the thresholded image
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        envelope_detected = False
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > MIN_CONTOUR_AREA:
                envelope_detected = True
                # Drawing a rectangle around the detected envelope for debugging
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                break  # Assuming one envelope per frame

        # Checking for envelope detection and debouncing before triggering the servo
        current_time = time.time()
        if envelope_detected and (current_time - last_trigger_time) > trigger_cooldown:
            print("Envelope detected! Triggering servo.")
            trigger_servo()
            last_trigger_time = current_time

        # Displaying the frame for debugging purposes, comment out when running headless
        cv2.imshow("Envelope Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Exiting gracefully...")

finally:
    # Releasing camera and GPIO resources
    cap.release()
    cv2.destroyAllWindows()
    pwm.stop()
    GPIO.cleanup()
