import cv2
import numpy as np

def detect_object():
    # Arrays store the minimum and maximum values for each HSV value. Refer to "hsv_value_setup.py"
    minimum_values = np.array([7, 0, 0])
    maximum_values = np.array([179, 255, 255])

    image_HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # Converts the image from blue green red (BGR) to HSV
    image_HSV_specific = cv2.inRange(image_HSV, minimum_values,
                                     maximum_values)  # Converts HSV image so only the red ball is displayed
    contours, hierarchy = cv2.findContours(image_HSV_specific, cv2.RETR_LIST,
                                           cv2.CHAIN_APPROX_SIMPLE)  # Finds contours in image (which can be used to identify shapes)

    for contour in contours:
        shape_area = cv2.contourArea(contour)
        if shape_area > 500:  # If shape area is larger than 500 (makes sure random detectoins are not processed)
            perimeter = cv2.arcLength(contour, True)
            verticies = cv2.approxPolyDP(contour, 0.03 * perimeter, True)  # Adjust values as needed

            if len(verticies) > 5:  # Circles will still have verticies. If we can find a good balance then we are solid
                x, y, width, height = cv2.boundingRect(verticies)  # Gets parameters for a rectangle around object
                cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 3)  # Draws rectangle on image


# Video frame dimensions
video_frame_width = 640
video_frame_height = 480
video_brightness_adjustment = 7

video_capture = cv2.VideoCapture(0) # Captures video from computer webcam (May need to configure computer settings for this to work)
video_capture.set(3, video_frame_width)
video_capture.set(4, video_frame_height)
video_capture.set(10, video_brightness_adjustment)
# https://stackoverflow.com/questions/11420748/setting-camera-parameters-in-opencv-python --> good source to see what each .set() parameter does.


while True:

    success, image = video_capture.read()

    x, y, width, height = detect_object() # Calls method to process image and identify object

    cv2.imshow("Webcam_Input", image)

    if cv2.waitKey(1) & 0xFF == ord('q'): # If 'q' is pressed, code ends
        break


print("Terminated")

