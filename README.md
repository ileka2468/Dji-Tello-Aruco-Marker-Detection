# Aruco Marker Detection for DJI Tello Drone
Use Aruco markers (binary square markers that can be used for camera pose estimation) to make an autonomous drone that cant detect markers, hover, and do cool stuff!
 
### Motivation :rocket:
------------------
Who doesn't love drones? Maybe the ATF, but that's beside the point. I  think autonomous computer vision projects are pretty cool and python libraries such as [**OpenCV**](https://docs.opencv.org/4.x/) make it semi-easy to have object tracking with just a few lines of code.

## Required Python Packages

[opencv-contrib](https://pypi.org/project/opencv-contrib-python/) - OpenCV-contrib is needed because regular open-cv does not have the aruco module, which will be needed for this project. Unless you are using the Conda environment, install py-OpenCV, which will contain the aruco module as well.

```
pip install opencv-contrib-python
```

[numPy](https://pypi.org/project/numpy/) - numPy should be installed with OpenCV, so there is no need to install it explicitly, but if for some reason it doesn't install, you can install it with the following command.

 ```
 pip install NumPy
 ```
 
[djiTelloPy](https://djitellopy.readthedocs.io/en/latest/tello/) - Python wrapper to interact with the Ryze Tello drone using the official Tello API. If you're not using a Tello drone, this package is not required.

 ```
pip install djitellopy
 ```

---------------------
## Camera Calibration 📷 📈

When trying to use cameras for computer vision applications, the camera you are using needs to be **calibrated** so that the pose estimations and distance calculations can be as accurate as possible. Naturally, all cameras have a **distortion** effect on them, some cameras may pull the picture at the frame, and some may squeeze the image at the center. To fix this, we need to counteract the image distortion; luckily, OpenCV makes this quite easy for us using the **calibrateCamera()** function.

There are multiple methods of calibrating a camera, we will be using the checkerboard method.

### 1. Obtain a checkerboard calibration board
Checkerboards for calibration can be obtained at this website https://markhedleyjones.com/projects/calibration-checkerboard-collection

This is the exact [checkerboard](https://raw.githubusercontent.com/MarkHedleyJones/markhedleyjones.github.io/master/media/calibration-checkerboard-collection/Checkerboard-A4-25mm-10x7.pdf) I used.

### 1. Take pictures of the checkerboard.
#### I wrote a script to take pictures of the checkerboard, it will take 1 picture every 30 frames.

To calibrate the camera, we need around 100 - 200 images of the checkerboard at lots of different angles and different distances. So, there is a script called CameraCap.py. If you're using a Tello drone, everything is already set up to run; all you need to do is connect the drone to your PC's wifi and run the script.

If you are not using a Tello drone, comment out the drone camera configs and uncomment the code block that sets up the camera for a native camera device.


```python
# If not using a DJI Tello drone, comment this code block out, and uncomment code below
drone = tello.Tello()
drone.connect()
print(drone.get_battery())
drone.streamon()

# If using a webcam or a raspberry pi, uncomment this for camera setup
'''
cam = cv2.VideoCapture(0)
cam.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv.CAP_PROP_FRAME_WIDTH, 480)
cam.set(cv.CAP_PROP_FPS, 30)
'''

```

### How to take the pictures.

#### Option 1 - Hold the checkerboard (Reccommended).

You have two options for deciding how you want to take the pictures. You can either paste the checkerboard on a board (refer to the image below) for maximum contrast. Then hold the board in your hands and move it around the camera frame like the guy pictured below ⬇️

![alt text](https://miro.medium.com/max/1280/1*Ms8XcIR_dNDs0GKGJHSE3g.png)

#### Option 2 - Put the checkerboard on a wall.

Alternatively, you can 


When you think you have taken enough images, press "q" on your keyboard to terminate the script, and in the working directory, you will see all of the images the camera took.



