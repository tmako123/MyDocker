DockerFile of okvis with ros
====

okvis_ros  
https://github.com/ethz-asl/okvis_ros

<!--
## Description
## Demo
-->

## Requirement
Ububtu 18.04
Docker 19.03

#### Build the image.
```
$ sudo docker build -t ros-okvis .
```

## Usage

#### 1. download dataset
- TUM VI DATASET  
download Bag 512x512 dataset "slides1"   
https://vision.in.tum.de/data/datasets/visual-inertial-dataset

- EuRoC Dataset
download bag "Machine Hall 01"
https://projects.asl.ethz.ch/datasets/doku.php?id=kmavvisualinertialdatasets

#### 2. run docker image
```
sudo docker run -it --name ros_okvis -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix --privileged --volume=/dev:/dev -v [PATH_TO_DATASET]:/mnt/share ros-okvis /bin/bash
```

#### 3. run okvis
- TUM VI DATASET
```
rosrun okvis_ros okvis_node_synchronous /catkin_ws/src/okvis_ros/okvis/config/tum_vi_slides1.cfg /mnt/share/dataset-slides1_512_16.bag 
```

- EuRoC Dataset
```
rosrun okvis_ros okvis_node_synchronous /catkin_ws/src/okvis_ros/okvis/config/config_fpga_p2_euroc.yaml /mnt/share/MH_01_easy.bag 
```
