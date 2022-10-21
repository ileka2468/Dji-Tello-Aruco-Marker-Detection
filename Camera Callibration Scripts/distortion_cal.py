import cv2
import glob
import numpy as np

'''
Make sure to edit the variables below, use the values for your specific checkerboard width and height.
Remmeber to subtract 1 from your width and height b/c the computer does not use the outer rows of the grid.
For example if you have an 11x8 board you should enter 10x7. After calibration finshes scanning the photos it could take
5 - 10 minutes to get the distortion values.

'''

cb_width = 10
cb_height = 7
'''
****-----!!! It is extremely important to measure the width of 1 square as accurately as possible, if possible use digital callipers !!!-----****
'''
square_size = 21.7

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points

cb_3D_points = np.zeros((cb_width * cb_height, 3), np.float32)
cb_3D_points[:, :2] = np.mgrid[0:cb_width, 0:cb_height].T.reshape(-1, 2) * square_size

# Array to store points and image points from images

list_cb_3d_points = []  # 3d point in real word
list_cb_2d_img_points = []  # 2d points in img plane

# Pulls all .jpg files in working directory
list_images = glob.glob('*.jpg')

for frame_name in list_images:
    img = cv2.imread(frame_name)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # find corners

    ret, corners = cv2.findChessboardCorners(gray, (10, 7), None)

    # If found, add object points and img points
    if ret == True:
        list_cb_3d_points.append(cb_3D_points)

        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        list_cb_2d_img_points.append(corners2)

        #draw boards

        cv2.drawChessboardCorners(img, (cb_width, cb_height), corners2, ret)
        cv2.imshow("img", img)
        cv2.waitKey(500)


cv2.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs, = cv2.calibrateCamera(list_cb_3d_points, list_cb_2d_img_points, gray.shape[::-1], None, None)

print("Calibration Matrix: ")
print(mtx)
print("Distortion: ", dist)

with open("camera_calibration.npy", "wb") as f:
    np.save(f, mtx)
    np.save(f, dist)
