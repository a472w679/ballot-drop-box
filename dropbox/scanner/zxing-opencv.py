import cv2
import zxingcpp

    # Convert the frame to grayscale (optional but improves performance)
img = cv2.imread("./example2.jpg")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# gray = cv2.GaussianBlur(gray, (5, 5), 0)
# gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)


# Decode barcodes
results = zxingcpp.read_barcodes(gray)

for result in results:
    # Get the barcode text and type
    barcode_text = result.text
    barcode_format = result.format

    print(barcode_format, barcode_text) 




