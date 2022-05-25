import cv2
import numpy as np
import util


BLUE_MAX = np.array([130, 255, 255], np.uint8)
BLUE_MIN = np.array([100, 90, 90], np.uint8)
src = cv2.imread("input/spatula_512x512.png")
cap = cv2.VideoCapture(0)
while (True):
    ret, frame = cap.read()

    # Show Video
    if ret is True:
        # mask = util.createMaskEdge(frame, BLUE_MIN, BLUE_MAX)
        # corners = util.locateCorners(mask, frame)
        # corners = util.locateCornersXY(mask, frame)
        # edges = util.locateEdges(mask, frame)

        # cv2.imshow('Camera', mask)
        # cv2.imshow('Corners', corners)
        # cv2.imshow('Edges', edges)
        # util.locateCornersXY(mask)

        # homography = util.homographyColorMask(mask, src, frame)

        # homography = util.homographyColorMask(src, frame)
        # cv2.imshow('homography', homography)

        homography = util.homographyArUco(src, frame)
        cv2.imshow('ArUco homography', homography)
        # cv2.imshow("frame", frame)
    # Exit Sequence
    # Exits on 'q' key pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break

# Release cap object from memory and turn off camera
cap.release()