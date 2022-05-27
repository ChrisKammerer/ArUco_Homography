import cv2
import numpy as np
import util

BLUE_MAX = np.array([130, 255, 255], np.uint8)
BLUE_MIN = np.array([100, 90, 90], np.uint8)
src = cv2.imread("input/spatula_512x512.png")
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()

    # Show Video
    if ret is True:

        mask = util.createMaskEdge(frame, BLUE_MIN, BLUE_MAX)
        corners = util.locateCornersXY(mask, frame)
        cv2.imshow('corners', corners)
        homographyColor = util.homographyColorMask(mask, src, frame)
        cv2.imshow('homography', homographyColor)
        homographyArUco = util.homographyArUco(src, frame)
        cv2.imshow('ArUco homography', homographyArUco)
    # Exit Sequence
    # Exits on 'q' key pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break

# Release cap object from memory and turn off camera
cap.release()
