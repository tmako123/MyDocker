DockerFile of MAPLAB + RealSenseSDK
====

MAPLAB use RealSense t265.  

MAPLAB  
https://github.com/ethz-asl/maplab  
RealSenseSDK  
https://github.com/IntelRealSense/librealsense

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
$ sudo docker build -t maplab:realsense .
```

## Usage

#### 1.Make parameters.
Make following parameter files from kalibr results,
put them into PATH_TO_REPOSITORY/MyDocker/maplab/param/t265/

EXAMPLE
<details><summary>imu-adis.yaml</summary><div>
id: c63aecb41bfdfd6b7e1fac37c7cbe7bf  
hardware_id: camera/imu  
sensor_type: IMU  
sigmas:  
  gyro_noise_density: 2.3220154778317275e-03  
  gyro_bias_random_walk_noise_density: 1.7982958907276115e-05  
  acc_noise_density: 2.0285060826919065e-02  
  acc_bias_random_walk_noise_density: 4.7319936547417403e-04  
saturation_accel_max_mps2: 150.0  
saturation_gyro_max_radps: 7.5  
gravity_magnitude_mps2: 9.81  
</div>
</details>


<details><summary>imu-sigmas.yaml</summary><div>
acc_noise_density: 2.0285060826919065e-02  
acc_bias_random_walk_noise_density: 4.7319936547417403e-04  
gyro_noise_density: 2.3220154778317275e-03  
gyro_bias_random_walk_noise_density: 1.7982958907276115e-05  
</div>
</details>

<details><summary>imu-sigmas.yaml</summary><div>
label: "t265_calibration"  
id: 412eab8e4058621f7036b5e765dfe812  
cameras:  
- camera:  
    label: camera/fisheye1  
    id: 54812562fa109c40fe90b29a59dd7798  
    line-delay-nanoseconds: 0  
    image_height: 800  
    image_width: 848  
    type: pinhole  
    intrinsics:  
      cols: 1  
      rows: 4  
      data: [288.6819700148808, 284.87056764099316, 420.20986131934535, 402.7797045021024]  
    distortion:  
      type: equidistant  
      parameters:  
        cols: 1  
        rows: 4  
        data: [-0.005477013337796245, 0.05067263597233775, -0.05055290656828977,
    0.010381072290273024]  
  T_B_C:  
    cols: 4  
    rows: 4  
    data: [-0.99995955, -0.00694458,  0.00571579,  0.01667597,  
0.00691062, -0.99995847, -0.00594143,  0.00800261,  
0.00575681, -0.00590169,  0.99996601,  0.007587,  
 0.       ,   0.       ,   0.       ,   1.        ]  
</div>
</details>

#### 2.Run maplab(ROVIO)
Set permission for x server and run image.
```
$ xhost +
$ sudo docker run -it --name maplab_realsense -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix --privileged --volume=/dev:/dev -v PATH_TO_REPOSITORY/MyDocker/maplab:/mnt/share maplab:realsense /bin/bash
```

Register parameters in environment.
```
ROVIO_CONFIG_DIR=/mnt/share/param/t265
LOCALIZATION_MAP_OUTPUT=$1
NCAMERA_CALIBRATION="$ROVIO_CONFIG_DIR/ncamera-t265.yaml"
IMU_PARAMETERS_MAPLAB="$ROVIO_CONFIG_DIR/imu-adis.yaml"
IMU_PARAMETERS_ROVIO="$ROVIO_CONFIG_DIR/imu-sigmas.yaml"
```

Run t265.
```
$ source catkin_ws/devel/setup.bash
$ roslaunch realsense2_camera rs_t265_sync.launch
```

Run maplab.
```
$ rosrun rovioli rovioli \
--alsologtostderr=1 \
--v=2 \
--ncamera_calibration=$NCAMERA_CALIBRATION \
--imu_parameters_maplab=$IMU_PARAMETERS_MAPLAB \
--imu_parameters_rovio=$IMU_PARAMETERS_ROVIO \
--datasource_type="rostopic" \
--save_map_folder="$LOCALIZATION_MAP_OUTPUT" \
--optimize_map_to_localization_map=false \
--map_builder_save_image_as_resources=false \
$REST
```

View camera position via rviz.
```
$ rosrun rviz rviz -d /mnt/share/param/t265/rovio.rviz
```

<!--
## Contribution
-->

## Author

[tmako123](https://github.com/tmako123/)
