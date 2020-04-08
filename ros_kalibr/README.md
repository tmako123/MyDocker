DockerFile of ROS + KALIBR + RealSenseSDK
====

Kalibration kit for realsense t265 stereo camera & imu calibration.

<!--
## Description
## Demo
-->

## Requirement
Ububtu 18.04
Docker 19.03

## Install

#### Build the image.
```
$ sudo docker build -t ros-kalibr .
```


## Usage

#### 1.Set permission for x server and run image.
```
$ xhost++
$ sudo docker run --name kalibr_calibration -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix --privileged --volume=/dev:/dev -v PATH_TO_REPOSITORY/ros_kalibr:/mnt/share ros-kalibr /bin/bash
```

If container is not started
```
$ sudo docker start kalibr_calibration
$ sudo docker exec -it kalibr_calibration /bin/bash
```

If multiple terminals are necessary (in another terminal)
```
$ sudo docker exec -it kalibr_calibration /bin/bash
```

#### 2.Calibrate IMU intrinsic parameter.
Connect t265 and run t265 in terminal A.
```
$ cd /catkin_ws
$ roslaunch realsense2_camera rs_t265_linear_interpolation.launch
```

Collect imu data and calculate imu bias and noise. Run in terminal B.
Put the camera on table for 60min.
```
$ cd /catkin_ws
$ roslaunch imu_utils t265_imu.launch
```

You can find the parameter at
/catkin_ws/src/imu_ttils/data

Copy the calibration result.
```
$ mkdir /mnt/share/param/t265
$ cp src/imu_utils/data/BMI055_imu_param.yaml /mnt/share/param/t265/
```

Make imu.yaml at /mnt/share/param/t265


<details><summary>Example</summary>
#Accelerometers
accelerometer_noise_density: 2.0285060826919065e-02   #Noise density (continuous-time)
accelerometer_random_walk:   4.7319936547417403e-04   #Bias random walk

#Gyroscopes
gyroscope_noise_density:     2.3220154778317275e-03   #Noise density (continuous-time)
gyroscope_random_walk:       1.7982958907276115e-05   #Bias random walk

rostopic:                    /imu      #the IMU ROS topic
update_rate:                 200.0      #Hz (for discretization of the values above)
</details>

#### 3.Stereo Camera Calibration
Download april_6x6_80x80cm_A0.pdf from kalibr web page.
Print or display on the screen, create or modify apriltags.yaml.
```
target_type: 'aprilgrid' #gridtype
tagCols: 6               #number of apriltags
tagRows: 6               #number of apriltags
tagSize: 0.0594           #size of apriltag, edge to edge [m]
tagSpacing: 0.3          #ratio of space between tags to tagSize
```

Run t265 in terminal A.
```
$ cd /catkin_ws
$ roslaunch realsense2_camera rs_t265_linear_interpolation.launch
```

Reduce the frequency of image topics in terminal B, C.
```
$ rosrun topic_tools throttle messages /camera/fisheye1/image_raw 4.0 /fisheye1
$ rosrun topic_tools throttle messages /camera/fisheye2/image_raw 4.0 /fisheye2
```

Record camera images. Attention to the camera move slowly, and the camera field of view should fully see apriltags. See the kalibr tutorial.
```
rosbag record -O /mnt/share/param/t265 /t265_stereo.bag  /fisheye1 /fisheye2
```

Calibration.
```
kalibr_calibrate_cameras --target /mnt/share/param/t265/april.yaml --bag /mnt/share/param/t265/t265_stereo.bag --models omni-radtan omni-radtan --topics /fisheye1 /fisheye2  --show-extraction
```

Following camera models are available.
- pinhole camera model (pinhole)
 - (intrinsics vector: [fu fv pu pv])
- omnidirectional camera model (omni)
 - (intrinsics vector: [xi fu fv pu pv])
- double sphere camera model (ds)
 - (intrinsics vector: [xi alpha fu fv pu pv])
- extended unified camera model (eucm)
 - (intrinsics vector: [alpha beta fu fv pu pv])

- radial-tangential (radtan)
 - (distortion_coeffs: [k1 k2 r1 r2])
- equidistant (equi)
 - (distortion_coeffs: [k1 k2 k3 k4])
fov (fov)
 - (distortion_coeffs: [w])
- none (none)
 - (distortion_coeffs: [])

If you plan to use opencv, you should choose
1. Pinhole(OpenCV) pinhole-radtan
2. Fisheye(OpenCV) pinhole-equi

After that, you can get following parameter and reports.
- results-cam-xxx.txt
- report-cam-xxx.pdf
- camchain-xxx.yaml

You may get an error when using the default.

- Using the default setup in the initial run leads to an error of Cameras are not connected through mutual observations, please check the dataset. Maybe adjust the approx. Sync. Tolerance.

This is due to the lack of synchronization between the two cameras.
In such case, add at the end--approx-sync 0.04.

Copy the result.
```
cp camchain-xxx.yaml /mnt/share/param/t265/
```

#### 4. Camera-IMU joint calibration
Run t265 and make topic in each terminal
```
$ roslaunch realsense-ros rs_t265_sync.launch
$ rosrun topic_tools throttle messages /camera/fisheye1/image_raw 20.0 /fisheye1
$ rosrun topic_tools throttle messages /camera/fisheye2/image_raw 20.0 /fisheye2
$ rosrun topic_tools throttle messages /camera/imu 200.0 /imu
```

Record rosbag.
```
rosbag record -O /mnt/share/param/t265 /t265_imu.bag  /fisheye1 /fisheye2 /imu
```

Do joint calibration.
```
kalibr_calibrate_imu_camera --target /mnt/share/param/t265/april_6x6_aquos.yaml --cam /mnt/share/param/t265/camchain-xxxx.yaml --imu /mnt/share/param/t265/imu.yaml --bag /mnt/share/param/t265/t265_imu.bag --max-iter 30 --show-extraction

```

Following result can be obtained.

<details><summary>Calibration results</summary><div>

===================   
Normalized Residuals
----------------------------  
Reprojection error (cam0):     mean 0.917256397968, median 0.742516514595, std: 0.636171993758  
Reprojection error (cam1):     mean 0.822725833571, median 0.664566913474, std: 0.587884503862  
Gyroscope error (imu0):        mean 0.284120146237, median 0.220347720452, std: 0.2305630649  
Accelerometer error (imu0):    mean 0.466338168541, median 0.355625258691, std: 0.414384497089  

Residuals
----------------------------
Reprojection error (cam0) [px]:     mean 0.917256397968, median 0.742516514595, std: 0.636171993758  
Reprojection error (cam1) [px]:     mean 0.822725833571, median 0.664566913474, std: 0.587884503862  
Gyroscope error (imu0) [rad/s]:     mean 0.00933001061055, median 0.00723583525158, std: 0.00757128936618  
Accelerometer error (imu0) [m/s^2]: mean 0.133780333699, median 0.102019669392, std: 0.118876171928

Transformation (cam0):  
-----------------------  
T_ci:  (imu0 to cam0):  
[[-0.99995955  0.00691062  0.00575681  0.01657632]  
 [-0.00694458 -0.99995847 -0.00590169  0.00816286]  
 [ 0.00571579 -0.00594143  0.99996601 -0.00763451]  
 [ 0.          0.          0.          1.        ]]  

T_ic:  (cam0 to imu0):  
[[-0.99995955 -0.00694458  0.00571579  0.01667597]  
 [ 0.00691062 -0.99995847 -0.00594143  0.00800261]  
 [ 0.00575681 -0.00590169  0.99996601  0.007587  ]  
 [ 0.          0.          0.          1.        ]]  

timeshift cam0 to imu0: [s] (t_imu = t_cam + shift)
-0.00935795508877  


Transformation (cam1):  
-----------------------  
T_ci:  (imu0 to cam1):  
[[-0.9999646   0.00841345  0.00007544 -0.0474304 ]  
 [-0.00841327 -0.99996232  0.00213833  0.0083957 ]  
 [ 0.00009343  0.00213762  0.99999771 -0.00734377]  
 [ 0.          0.          0.          1.        ]]  

T_ic:  (cam1 to imu0):  
[[-0.9999646  -0.00841327  0.00009343 -0.0473574 ]  
 [ 0.00841345 -0.99996232  0.00213762  0.00881014]  
 [ 0.00007544  0.00213833  0.99999771  0.00732937]  
 [ 0.          0.          0.          1.        ]]  

timeshift cam1 to imu0: [s] (t_imu = t_cam + shift)
-0.0122912038075  

Baselines:  
----------
Baseline (cam0 to cam1):  
[[ 0.99998273 -0.00146921 -0.00569014 -0.06403788]  
 [ 0.00151489  0.9999666   0.00803138  0.00026932]  
 [ 0.00567815 -0.00803986  0.99995156  0.00026188]  
 [ 0.          0.          0.          1.        ]]  
baseline norm:  0.0640389847991 [m]  


Gravity vector in target coords: [m/s^2]  
[ 0.00820782 -9.80638158 -0.05688437]  


Calibration configuration  
=========================  

cam0  
-----
  Camera model: omni  
  Focal length: [543.7916463149062, 536.2178305623025]  
  Principal point: [421.13198559065535, 403.4168845166052]  
  Omni xi: 0.883531660058  
  Distortion model: radtan  
  Distortion coefficients: [-0.2719670670526357, -0.006380993867875025, -0.0007139982580822136, -0.0007698788089056164]  
  Type: aprilgrid  
  Tags:  
    Rows: 6  
    Cols: 6  
    Size: 0.0594 [m]  
    Spacing 0.01782 [m]  


cam1  
-----
  Camera model: omni  
  Focal length: [536.8596234548693, 529.0137374167572]  
  Principal point: [430.8562994003341, 407.06586027413476]  
  Omni xi: 0.855579840505
  Distortion model: radtan  
  Distortion coefficients: [-0.2756953258399794, 0.0019039855208915267, -0.0022496015443047484, -0.00030676226719549455]  
  Type: aprilgrid  
  Tags:  
    Rows: 6  
    Cols: 6  
    Size: 0.0594 [m]  
    Spacing 0.01782 [m]  



IMU configuration  
=================  

IMU0:  
----------------------------  
  Model: calibrated  
  Update rate: 200.0  
  Accelerometer:  
    Noise density: 0.0202850608269  
    Noise density (discrete): 0.28687408135  
    Random walk: 0.000473199365474  
  Gyroscope:  
    Noise density: 0.00232201547783  
    Noise density (discrete): 0.0328382578079  
    Random walk: 1.79829589073e-05  
  T_i_b  
    [[ 1.  0.  0.  0.]  
     [ 0.  1.  0.  0.]  
     [ 0.  0.  1.  0.]  
     [ 0.  0.  0.  1.]]  
  time offset with respect to IMU0: 0.0 [s]  
  </div>
</details>


<!--
## Contribution
-->

## Author

[tmako123](https://github.com/tmako123/)
