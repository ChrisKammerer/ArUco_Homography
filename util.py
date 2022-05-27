import cv2
import numpy as np


# This file includes all useful functions for doing homography with
# a green screen or by using an ArUco marker. Not all of these functions are
# called in either main.py or video.py, but they were used in my
# experimentation for the project


def createMask(img, HSV_LOW, HSV_HIGH):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv = cv2.bilateralFilter(hsv, 5, 75, 75)
    mask = cv2.inRange(hsv, HSV_LOW, HSV_HIGH)
    return mask


def createMaskEdge(img, HSV_LOW, HSV_HIGH):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv = cv2.bilateralFilter(hsv, 5, 75, 75)
    mask = cv2.inRange(hsv, HSV_LOW, HSV_HIGH)
    mask = cv2.Canny(mask, 100, 200)
    mask = cv2.bilateralFilter(mask, 5, 75, 75)
    return mask


def locateCorners(mask, img):
    edge = cv2.Canny(mask, 100, 200)
    corners = cv2.cornerHarris(edge, 2, 5, .08)
    corners = cv2.dilate(corners, None)
    thresh = 0.01 * corners.max()
    img[corners > thresh] = [0, 0, 255]
    return img


def locateEdges(mask, img):
    edge = cv2.Canny(mask, 100, 200)
    lines = cv2.HoughLines(edge, 1, np.pi / 180, 120, None, 0, 0)
    # points = np.zeros((len(lines), 2, 2), )
    if lines is None:
        return img
    for i in range(len(lines)):
        rho = lines[i][0][0]
        theta = lines[i][0][1]

        dx = np.cos(theta)
        dy = np.sin(theta)

        x0 = dx * rho
        y0 = dy * rho

        pt1 = (int(x0 + 2000 * (-dy)), int(y0 + 2000 * dx))
        pt2 = (int(x0 - 2000 * (-dy)), int(y0 - 2000 * dx))

        # run = abs(pt2[0] - pt1[0])
        # rise = abs(pt2[1] - pt1[1])
        cv2.line(img, pt1, pt2, (0, 255, 0), 3, cv2.LINE_AA)

    return img


def locateCornersXY(mask, frame):
    # x1,y1 = top left
    # x2,y2 = top right
    # x3,y3 = bottom left
    # x4,y4 = bottom right
    img = frame.copy()
    points = np.where(mask > 0)
    if points[0] is None:
        return img
    if points[1] is None:
        return img
    x1 = np.min(points[1])
    y1 = np.where(points[1] == x1)
    y1 = points[0][y1[0][0]]

    y2 = np.max(points[0])
    x2 = np.where(points[0] == y2)
    x2 = points[1][x2[0][0]]

    x3 = np.max(points[1])
    y3 = np.where(points[1] == x3)
    y3 = points[0][y3[0][0]]

    y4 = np.min(points[0])
    x4 = np.where(points[0] == y4)
    x4 = points[1][x4[0][0]]

    cv2.circle(img, (x1, y1), 5, (0, 255, 0))
    cv2.circle(img, (x2, y2), 5, (0, 255, 0))
    cv2.circle(img, (x3, y3), 5, (0, 255, 0))
    cv2.circle(img, (x4, y4), 5, (0, 255, 0))

    return img


def homographyColorMask(mask, src, frame):
    # x1,y1 = top left
    # x2,y2 = top right
    # x3,y3 = bottom left
    # x4,y4 = bottom right
    dst = frame.copy()
    points = np.where(mask > 0)
    if points is None:
        return
    x1 = np.min(points[1])
    y1 = np.where(points[1] == x1)
    y1 = points[0][y1[0][0]]

    y2 = np.max(points[0])
    x2 = np.where(points[0] == y2)
    x2 = points[1][x2[0][0]]

    x3 = np.max(points[1])
    y3 = np.where(points[1] == x3)
    y3 = points[0][y3[0][0]]

    y4 = np.min(points[0])
    x4 = np.where(points[0] == y4)
    x4 = points[1][x4[0][0]]

    cv2.circle(dst, (x1, y1), 5, (0, 255, 0))
    cv2.circle(dst, (x2, y2), 5, (0, 255, 0))
    cv2.circle(dst, (x3, y3), 5, (0, 255, 0))
    cv2.circle(dst, (x4, y4), 5, (0, 255, 0))

    pts_dst = np.empty((0, 2))
    pts_dst = np.append(pts_dst, [(x1, y1)], axis=0)
    pts_dst = np.append(pts_dst, [(x2, y2)], axis=0)
    pts_dst = np.append(pts_dst, [(x3, y3)], axis=0)
    pts_dst = np.append(pts_dst, [(x4, y4)], axis=0)

    height = src.shape[0]
    width = src.shape[1]
    pts_src = np.empty((0, 2))
    pts_src = np.append(pts_src, [(0, 0)], axis=0)
    pts_src = np.append(pts_src, [(width - 1, 0)], axis=0)
    pts_src = np.append(pts_src, [(width - 1, height - 1)], axis=0)
    pts_src = np.append(pts_src, [(0, height - 1)], axis=0)

    tform, status = cv2.findHomography(pts_src, pts_dst)

    dst_shape = dst.shape[0:2]
    warp = cv2.warpPerspective(src, tform, (dst_shape[1], dst_shape[0]))

    cv2.fillConvexPoly(dst, pts_dst.astype(int), 0, 16)
    dst = dst + warp

    return dst


def homographyArUco(src, frame):
    dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
    parameters = cv2.aruco.DetectorParameters_create()
    markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
    markerCorners = np.squeeze(markerCorners)

    if markerCorners.size == 0 or src is None:
        return frame

    height = src.shape[0]
    width = src.shape[1]
    pts_src = np.empty((0, 2))
    pts_src = np.append(pts_src, [(0, 0)], axis=0)
    pts_src = np.append(pts_src, [(width - 1, 0)], axis=0)
    pts_src = np.append(pts_src, [(width - 1, height - 1)], axis=0)
    pts_src = np.append(pts_src, [(0, height - 1)], axis=0)

    tform, status = cv2.findHomography(pts_src, markerCorners)
    warp = cv2.warpPerspective(src, tform, (frame.shape[1], frame.shape[0]))

    cv2.fillConvexPoly(frame, markerCorners.astype(int), 0, 16)

    im_out = frame + warp

    return im_out
