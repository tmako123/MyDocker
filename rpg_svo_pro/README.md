DockerFile of SVO Pro
====

SVO Pro
https://github.com/uzh-rpg/rpg_svo_pro_open

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
$ sudo docker build -t rpg_svo_pro .
```

## Usage

#### 1.Run docker container
```
$ sudo docker run -it --name rpg_svo_pro -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix --privileged --volume=/dev:/dev -v [path to EuRoC bag]:/mnt/dataset/ /bin/bash
```

### 2. enable docker gui
```
$ xhost +
```

#### 3.run rpg svo Pro in Docker
```
$ docker exec -it rpg_svo_pro
$ cd svo_ws/
$ source devel/setup.bash
$ roslaunch svo_ros euroc_vio_stereo.launch
```

### 4. run the EuRoC bag in other bash
```
$ docker exec -it rpg_svo_pro
$ rosbag play /mnt/dataset/V2_03_difficult.bag
```

<!--
## Contribution
-->

## Author

[tmako123](https://github.com/tmako123/)
