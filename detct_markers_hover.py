import numpy as np
import cv2
import cv2.aruco as aruco
import math
from djitellopy import tello
import time


def main():
    # drone setup
    me = tello.Tello()
    me.connect()
    me.streamon()
    me.takeoff()
    alt = me.get_height()
    time.sleep(4)
    getMarkers(me, alt)
    print(me.get_battery())

# Checks if a matrix is a valid rotation matrix.
def isRotationMatrix(R) :
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype=R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6

# Calculates rotation matrix to eulers angle
# The result is the same as MATLAB except the order
# of the euler angles ( x and z are swapped ).
# Credit to Satya Mallick for the angle calculations: https://learnopencv.com/rotation-matrix-to-euler-angles/


def rotationMatrixToEulerAngles(R):

    assert(isRotationMatrix(R))

    sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
    singular = sy < 1e-6

    if  not singular :
        x = math.atan2(R[2,1] , R[2,2])
        y = math.atan2(-R[2,0], sy)
        z = math.atan2(R[1,0], R[0,0])
    else :
        x = math.atan2(-R[1,2], R[1,1])
        y = math.atan2(-R[2,0], sy)
        z = 0

    return np.array([x, y, z])

# set aruco marker size here
marker_size = 100
# Make sure calibration file is in same working directory as script.
with open("mirrorcalibration.npy", "rb") as f:
    camera_matrix = np.load(f)
    camera_distortion = np.load(f)

aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
'''
Functions for controlling drones, this is a very crude way of keeping the drone locked on the target. In my next iteration
I will create a more robust way of locking onto the markers, and create functionality from landing and taking off from
multiple different markers.
'''

# If you're not using a Tello drone this is where you can add your own functions to control your drone.
def drone_rotate(drone, real_time_rotation):
    if real_time_rotation > 10:
        #drone.send_rc_control(0, -20, 0, 0)
        print("Rotating left...")
    if real_time_rotation > -10:
        #drone.send_rc_control(0, 20, 0, 0)
        print("Rotating right...")


def drone_maintain_x(drone, x_distance):
    if x_distance > 10:
        #drone.send_rc_control(0, -20, 0, 0)
        print("Moving left...")
    if x_distance > -10:
        #drone.send_rc_control(0, 20, 0, 0)
        print("Moving right...")

def drone_maintain_y(drone, y_distance):
    if y_distance > 10:
        # drone.send_rc_control(-20, 0, 0, 0)
        print("Moving backwards...")
    if y_distance > -10:
        # drone.send_rc_control(0, 0, 0, 0)
        print("Moving forwards...")



def getMarkers(drone, altitude):
    frame_count = 1000000
    while altitude > 70:
        frame_count += 1
        if frame_count % 1000000 == 0:
            frame = drone.get_frame_read().frame
            frame = cv2.resize(frame, (640, 480))
            frame = cv2.flip(frame, 1)
            if frame_count >= 1000000:
                frame_count = 0

            # ret, frame = cam.read()

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            corners, ids, rejected = aruco.detectMarkers(gray_frame, aruco_dict, camera_matrix, camera_distortion)

            if ids is not None:
                aruco.drawDetectedMarkers(frame, corners)
                rvec_list_all, tvec_list_all, _objPoints = aruco.estimatePoseSingleMarkers(corners, marker_size, camera_matrix, camera_distortion)
                rvec = rvec_list_all[0][0]
                tvec= tvec_list_all[0][0]

                aruco.drawAxis(frame, camera_matrix, camera_distortion, rvec, tvec, 100)

                rvec_flipped = rvec * -1
                tvec_flipped = tvec * -1
                rotation_matrix, jacobian = cv2.Rodrigues(rvec_flipped)
                realorld_tvec = np.dot(rotation_matrix, tvec_flipped)

                pitch, roll, yaw = rotationMatrixToEulerAngles(rotation_matrix)

                tvec_str = "x=%4.0f y=%4.0f direction=%4.0f"%(realorld_tvec[0], realorld_tvec[1], math.degrees(yaw))

                top_position = math.degrees(yaw)
                if realorld_tvec[1] > -35:
                    cv2.putText(frame, f"ID: {ids[0][0]} Y position accurate, move down!", (20, 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                if math.degrees(yaw) > 10 or math.degrees(yaw) < -10:
                    if math.degrees(yaw) > 10 or math.degrees(yaw) > -10:
                        drone_rotate(drone, math.degrees(yaw))
                    if not math.degrees(yaw) > 10 or not math.degrees(yaw) > -10:
                        # drone.send_rc_control(0,0,0,0)
                        cv2.putText(frame, f"ID: {ids[0][0]} rotate to the right!", (20, 40),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                    else:
                        cv2.putText(frame, f"ID: {ids[0][0]} rotate to the left!", (20, 40),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                if realorld_tvec[0] > 10 or realorld_tvec[0] > -10:
                    drone_maintain_x(drone, realorld_tvec[0])
                if not realorld_tvec[0] > 10 or not realorld_tvec[0] > -10:
                    #drone.send_rc_control(0, 0, 0, 0)
                    pass

                if realorld_tvec[1] > 10 or realorld_tvec[1] > -10:
                    drone_maintain_y(drone, realorld_tvec[1])
                if not realorld_tvec[1] > 10 or not realorld_tvec[1] > -10:
                    #drone.send_rc_control(0, 0, 0, 0)
                    pass

                cv2.putText(frame, tvec_str, (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            cv2.imshow("frame", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            elif key == ord("p"):
                drone.land()

    cv2.destroyAllWindows()


main()
