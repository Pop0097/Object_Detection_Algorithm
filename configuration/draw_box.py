# NOTE: to make this file run, move it to the root directory. For some reason it doesn't work when it's in this directory.

import cv2
import numpy as np

def identify_circle_and_draw_recangle(image):
    contours, heirarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # Gets all contours in image
    for contour in contours:
        shape_area = cv2.contourArea(contour)
        if shape_area > 100: # If shape area is larger than 500 (makes sure random detectoins are not processed)
            perimeter = cv2.arcLength(contour, True)
            print(shape_area)
            verticies = cv2.approxPolyDP(contour, 0.05*perimeter, True) # Adjust values as needed
            print(len(verticies))
            if len(verticies) > 6: # Circles will still have verticies. If we can find a good balance then we are solid
                x, y, width, height = cv2.boundingRect(verticies) # Gets parameters for a rectangle around object
                print(x, " ", y, " ", width, " ", height)
                cv2.rectangle(image, (x, y), (x+width, y+height), (255, 0, 0), 3) # Draws rectangle on image


# Main block of code
image_path = 'image/ball.jpg'

image = cv2.imread(image_path) # Gets image from directory
image_HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # Converts the image from blue green red (BGR) to HSV

# Arrays store the minimum and maximum values for each HSV value. Refer to "hsv_value.py"
minimum_values = np.array([7, 0, 0])
maximum_values = np.array([179, 255, 255])

# Creates an image that displays only the ball
HSV_specific_image = cv2.inRange(image_HSV, minimum_values, maximum_values)

# Resizes the image
HSV_specific_image_resized = cv2.resize(HSV_specific_image, (1000, 600))

canny_image = cv2.Canny(HSV_specific_image_resized, 50, 50)
identify_circle_and_draw_recangle(canny_image)

cv2.imshow("Cool", canny_image)

cv2.waitKey(0)