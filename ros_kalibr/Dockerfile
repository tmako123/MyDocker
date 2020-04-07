FROM osrf/ros:kinetic-desktop-full

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y \
    	python-setuptools \
	python-rosinstall \
	ipython \
	libeigen3-dev \
	libboost-all-dev \
	doxygen \
	libopencv-dev \
	ros-kinetic-vision-opencv \
	ros-kinetic-image-transport-plugins \
	ros-kinetic-cmake-modules \
	python-software-properties \
	software-properties-common \
	libpoco-dev \
	python-matplotlib \
	python-scipy \
	python-git \
	python-pip \
	libtbb-dev \
	libblas-dev \
	liblapack-dev \
	python-catkin-tools \
	libv4l-dev \
	wget \
	autoconf automake 

RUN python -m pip install --upgrade pip; python -m pip install python-igraph --upgrade
ENV KALIBR_WORKSPACE /catkin_ws

RUN 	mkdir -p $KALIBR_WORKSPACE/src &&\
	cd $KALIBR_WORKSPACE &&\
	catkin init &&\
	catkin config --extend /opt/ros/kinetic &&\
	catkin config --cmake-args -DCMAKE_BUILD_TYPE=Release

RUN 	cd $KALIBR_WORKSPACE/src &&\
	git clone https://github.com/ethz-asl/Kalibr.git

RUN	cd $KALIBR_WORKSPACE &&\
	catkin build -DCMAKE_BUILD_TYPE=Release -j2

RUN echo 'deb http://realsense-hw-public.s3.amazonaws.com/Debian/apt-repo xenial main' || tee /etc/apt/sources.list.d/realsense-public.list
RUN apt-key adv --keyserver keys.gnupg.net --recv-key C8B3A55A6F3EFCDE || apt-key adv --keyserver hkp://keys.gnupg.net:80 --recv-key C8B3A55A6F3EFCDE
RUN add-apt-repository "deb http://realsense-hw-public.s3.amazonaws.com/Debian/apt-repo xenial main"
RUN apt-get update && apt-get install --allow-unauthenticated -y \
	librealsense2-dkms \
	librealsense2-dev  \
	librealsense2-utils \
	librealsense2-dbg
	
RUN apt -q -qq update && \
  DEBIAN_FRONTEND=noninteractive apt install -y --allow-unauthenticated \
  python-rosinstall \
  python-catkin-tools \
  ros-kinetic-jsk-tools \
  ros-kinetic-rgbd-launch \
  ros-kinetic-image-transport-plugins \
  ros-kinetic-image-transport

RUN rosdep update

#realsense
RUN mkdir -p /catkin_ws/src && cd /catkin_ws/src && \
  git clone --depth 1 https://github.com/IntelRealSense/realsense-ros.git && \
  git clone --depth 1 https://github.com/pal-robotics/ddynamic_reconfigure
RUN cd catkin_ws;
RUN mv /bin/sh /bin/sh_tmp && ln -s /bin/bash /bin/sh
RUN source /opt/ros/${ROS_DISTRO}/setup.bash; cd catkin_ws; catkin build -DCATKIN_ENABLE_TESTING=False -DCMAKE_BUILD_TYPE=Release
RUN rm /bin/sh && mv /bin/sh_tmp /bin/sh
RUN touch /root/.bashrc && \
  echo "source /catkin_ws/devel/setup.bash\n" >> /root/.bashrc && \
  echo "rossetip\n" >> /root/.bashrc && \
  echo "rossetmaster localhost"

#ceres
RUN apt -q -qq update &&  apt-get install -y \
	libgoogle-glog-dev
RUN mkdir -p ceres && cd ceres && wget http://ceres-solver.org/ceres-solver-1.12.0.tar.gz && tar zxf ceres-solver-1.12.0.tar.gz
RUN cd ceres/ceres-solver-1.12.0 && \
	mkdir ceres-bin && \
	cd ceres-bin && \
	cmake .. && \
	make -j2 && \
	make test && \
	make install

#code_utils
RUN apt -q -qq update &&  apt-get install -y \
	libdw-dev
RUN cd /catkin_ws/src && \
	git clone https://github.com/gaowenliang/code_utils.git && \
	sed -i -e "s@backward.hpp@code_utils/backward.hpp@g" code_utils/src/sumpixel_test.cpp && \
	cd .. && \
	catkin build -DCATKIN_ENABLE_TESTING=False -DCMAKE_BUILD_TYPE=Release
RUN cd /catkin_ws/src && \
	git clone https://github.com/gaowenliang/imu_utils.git && \
	cd .. && \
	catkin build -DCATKIN_ENABLE_TESTING=False -DCMAKE_BUILD_TYPE=Release

#add rounch files
ADD t265_imu.launch /catkin_ws/src/imu_utils/launch/
ADD rs_t265_linear_interpolation.launch /catkin_ws/src/realsense-ros/realsense2_camera/launch/
ADD rs_t265_sync.launch /catkin_ws/src/realsense-ros/realsense2_camera/launch/


