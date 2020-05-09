FROM osrf/ros:kinetic-desktop-full
LABEL maintainer="tmako123 <https://github.com/tmako123/>"

RUN apt update && apt install -y \
	libgoogle-glog-dev \
	libatlas-base-dev libeigen3-dev libsuitesparse-dev \
	libopencv-dev libboost-dev libboost-filesystem-dev \
        zip unzip wget python-catkin-tools

ENV ROS_VERSION=kinetic
ENV CATKIN_WS=/catkin_ws
RUN mkdir -p $CATKIN_WS/src && \
	cd $CATKIN_WS && \
	catkin init && \
	catkin config --merge-devel && \
	catkin config --extend /opt/ros/$ROS_VERSION && \
	catkin config --cmake-args -DCMAKE_BUILD_TYPE=Release && \
	cd src && \
	wget https://www.doc.ic.ac.uk/~sleutene/software/okvis_ros-1.1.3.zip && \
	unzip okvis_ros-1.1.3.zip && rm okvis_ros-1.1.3.zip

RUN sed -i -e '208,209d' $CATKIN_WS/src/okvis_ros/src/okvis_node_synchronous.cpp && \
        sed -i '208i const cv::Mat filtered = cv_bridge::toCvCopy(msg1, "mono8")->image;' $CATKIN_WS/src/okvis_ros/src/okvis_node_synchronous.cpp && \
        sed -i '68i #include <cv_bridge/cv_bridge.h>' $CATKIN_WS/src/okvis_ros/src/okvis_node_synchronous.cpp && \
        cd $CATKIN_WS && catkin build j2

#realsense essential
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

#realsense essential
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

ADD tum_vi_slides1.cfg /catkin_ws/src/okvis_ros/okvis/config

