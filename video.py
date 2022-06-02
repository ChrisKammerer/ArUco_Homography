import cv2
import numpy as np
import util

BLUE_MAX = np.array([130, 255, 255], np.uint8)
BLUE_MIN = np.array([100, 90, 90], np.uint8)
src = cv2.imread("input/spatula_512x512.png")
cap = cv2.VideoCapture(0)
vid = cv2.VideoCapture("input/LONELY_MANS_PING_PONG_TABLE1.mp4")
frameCounter = 0
while True:

    if vid.get(cv2.CAP_PROP_POS_FRAMES) == vid.get(cv2.CAP_PROP_FRAME_COUNT):  # end of video, reset frame to 0
        frameCounter = 0
        vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
    ret, frame = cap.read()
    ret2, frame_vid = vid.read()
    frameCounter += 1
    if ret2:  # frame ready
        homography = util.homographyArUco(frame_vid, frame)
        pos_frame = vid.get(cv2.CAP_PROP_POS_FRAMES)
    else:  # frame not ready
        vid.set(cv2.CAP_PROP_POS_FRAMES, pos_frame - 1)
    cv2.imshow('ArUco homography', homography)
    # Exit Sequence
    # Exits on 'q' key pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break

# Release cap object from memory and turn off camera
cap.release()
