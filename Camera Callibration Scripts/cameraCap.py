import cv2
import cv2 as cv
import time
from djitellopy import tello

'''
*** Make sure to run this script in the same directory as process.py ***
Use a checkerboard calibration grid which you can print from here: https://markhedleyjones.com/projects/calibration-checkerboard-collection
When running the script keep the checkerboard in the camera frame, making sure to capture images up close,
and far away as well as at differing angles. Refrain from moving checkerboard too fast, as it can cause blur. Quality over quantity here.
The more images you take the better the calibration will be, but the longer it will take to run the distortion calibration.

*** When you think you have captured enough images (150 - 200), go through all the photos and delete blurry or cut off
checkerboards. ***

'''

# If not using a DJI Tello drone comment this code block out, and uncomment code below
drone = tello.Tello()
drone.connect()
print(drone.get_battery())
drone.streamon()

# If using a webcam or a raspberry pi uncomment this for camera setup
'''
cam = cv2.VideoCapture(0)
cam.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv.CAP_PROP_FRAME_WIDTH, 480)
cam.set(cv.CAP_PROP_FPS, 30)
'''

prev_frame_time = time.time()
frame_count = 0
cal_picks = 0
while True:
    # uncomment line below if using PC webcam
    '''
    ret, img = cam.read()
    '''
    img = drone.get_frame_read().frame
    img = cv.resize(img, (640, 480))

    # saves 1 picture every 30 frames and saves picture.
    frame_count += 1
    if frame_count == 30:
        cv.imwrite("checer_image" + str(cal_picks) + ".jpg", img)
        cal_picks += 1
        frame_count = 0

    # FPS calculation
    new_frame_time = time.time()
    fps = 1/(new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    cv2.putText(img, f"FPS: {str(int(fps))}", (20, 460),  cv.FONT_HERSHEY_COMPLEX, 1, (0, 250, 0), 2)

    cv2.imshow("Camera", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
