# Aruco Marker Detection for Dji Tello Drone
Use Aruco markers (binary square markers that can be used for camera pose estimation) to make an autonomus drone that cant detect markers, hovver, and do cool stuff!
 
### Motivation :rocket:
------------------
Who doesn't love drones? Maybe the ATF, but that's beside the point. I  think autonomus computer vision projects are pretty cool and python libraries such as [**OpenCV**](https://docs.opencv.org/4.x/) make it semi-easy to have object tracking with just a few lines of code.

### Required Python Packages
------------------
[opencv-contrib](https://pypi.org/project/opencv-contrib-python/) - opencv-contrib is needed because regular open-cv does not have the aruco module which will be needed for this project. Unless you are using the Conda environment install py-opencv which will contain the aruco module as well.

```
pip install opencv-contrib-python
```


