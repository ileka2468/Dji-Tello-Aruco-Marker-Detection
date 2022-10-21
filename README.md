# Aruco Marker Detection for Dji Tello Drone
Use Aruco markers (binary square markers that can be used for camera pose estimation) to make an autonomus drone that cant detect markers, hovver, and do cool stuff!
 
### Motivation :rocket:
------------------
Who doesn't love drones? Maybe the ATF, but that's beside the point. I  think autonomus computer vision projects are pretty cool and python libraries such as [**OpenCV**](https://docs.opencv.org/4.x/) make it semi-easy to have object tracking with just a few lines of code.

## Required Python Packages

[opencv-contrib](https://pypi.org/project/opencv-contrib-python/) - opencv-contrib is needed because regular open-cv does not have the aruco module which will be needed for this project. Unless you are using the Conda environment install py-opencv which will contain the aruco module as well.

```
pip install opencv-contrib-python
```

[numPy](https://pypi.org/project/numpy/) - numPy should be installed with opencv, so there is no need to explicity install it, but if for some reason it doesn't install, you can install it with the following command.

 ```
 pip install numpy
 ```
 
[djiTelloPy](https://djitellopy.readthedocs.io/en/latest/tello/) - Python wrapper to interact with the Ryze Tello drone using the official Tello api. If you're not using a Tello drone, this package is not required.

 ```
pip install djitellopy
 ```

---------------------
## Camera Calibration 📷 📈

When trying to use cameras for computer vision applications the camera you are using needs to be **calibrated** so that the pose estiamtions and distance calculations can be as accurate as posible. Naturally, all cameras have a **distortion** effect to them, some cameras may pull the picture at the frame, and some may squeeze the image at the center. To fix this we need to counteract the image distortion, luckily OpenCv makes this quiote easy for us using the **calibrateCamera()** function.

There are multiple methods of calibrating a camera, we will be using the checkerboard method.

### Obtain a checkerboard calibration board
