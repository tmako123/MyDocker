DockerFile of ORB-SLAM3
====

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
$ sudo docker build -t orb-slam3 .
```

## Usage

#### 1.Set permission for x server and run image.
```
$ xhost++
$ sudo docker run --name orb-slam3 -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix --privileged --volume=/dev:/dev -v PATH_TO_DATASET:/mnt/share orb-slam3 /bin/bash
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

<!--
## Contribution
-->

## Author

[tmako123](https://github.com/tmako123/)
