import cv2
import numpy as np

### METHOD BLOCK BEGINS ###

def detect_object():
    # Arrays store the minimum and maximum values for each HSV value. Refer to "hsv_value_setup.py"
    minimum_values = np.array([7, 0, 0])
    maximum_values = np.array([150, 255, 255])

    image_HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # Converts the image from blue green red (BGR) to HSV
    image_HSV_specific = cv2.inRange(image_HSV, minimum_values,
                                     maximum_values)  # Converts HSV image so only the red ball is displayed
    blur_image = cv2.blur(image_HSV_specific, (7, 7))
    contours, hierarchy = cv2.findContours(blur_image, cv2.RETR_LIST,
                                           cv2.CHAIN_APPROX_SIMPLE)  # Finds contours in image (which can be used to identify shapes)

    # Displays image that the computer processes
    # cv2.imshow("Processed_Image", blur_image)

    for contour in contours:
        shape_area = cv2.contourArea(contour)
        if shape_area > 1300:  # If shape area is larger than 500 (makes sure random detectoins are not processed)
            perimeter = cv2.arcLength(contour, True)
            verticies = cv2.approxPolyDP(contour, 0.03 * perimeter, True)  # Adjust values as needed

            if len(verticies) > 6:  # Circles will still have verticies. If we can find a good balance then we are solid
                x, y, width, height = cv2.boundingRect(verticies)  # Gets parameters for a rectangle around object
                # cv2.line(image, (x, 0), (x, 480), (255, 255, 255), 2)
                # if x < center_x:
                #     cv2.putText(image, 'Left', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                # elif x > center_x:
                #     cv2.putText(image, 'Right', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 3)  # Draws rectangle on image

### HELPER BLOCK ENDS ###

### MAIN CODE BLOCK BEGINS ###

# Video frame dimensions
video_frame_width = 640
video_frame_height = 480
video_brightness_adjustment = 7

video_capture = cv2.VideoCapture(0) # Captures video from computer webcam (May need to configure computer settings for this to work)
video_capture.set(3, video_frame_width)
video_capture.set(4, video_frame_height)
video_capture.set(10, video_brightness_adjustment)
# https://stackoverflow.com/questions/11420748/setting-camera-parameters-in-opencv-python --> good source to see what each .set() parameter does.

# Center of the image frames
center_x = video_frame_width/2
center_y = video_frame_height/2

while True:
    success, image = video_capture.read()

    detect_object() # Calls method to process image and identify object

    cv2.imshow("Webcam_Input", image)

    if cv2.waitKey(1) & 0xFF == ord('q'): # If 'q' is pressed, code ends
        break


print("Terminated")

### MAIN CODE BLOCK ENDS ###

