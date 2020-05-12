FROM ros:kinetic-perception
LABEL maintainer="tmako123 <https://github.com/tmako123/>"

ENV CERES_VERSION="1.12.0"
ENV CATKIN_WS=/root/catkin_ws

      # set up thread number for building
RUN   apt-get update && apt-get install -y \
      cmake \
      libatlas-base-dev \
      libeigen3-dev \
      libgoogle-glog-dev \
      libsuitesparse-dev \
      python-catkin-tools \
      ros-kinetic-cv-bridge \
      ros-kinetic-image-transport \
      ros-kinetic-message-filters \
      ros-kinetic-tf && \
      rm -rf /var/lib/apt/lists/* && \
      # Build and install Ceres
      git clone https://ceres-solver.googlesource.com/ceres-solver && \
      cd ceres-solver && \
      git checkout tags/${CERES_VERSION} && \
      mkdir build && cd build && \
      cmake .. && \
      make -j2 install && \
      rm -rf ../../ceres-solver && \
      mkdir -p $CATKIN_WS/src/

# Copy VINS-Fusion
#COPY ./ $CATKIN_WS/src/VINS-Fusion/
# use the following line if you only have this dockerfile
RUN cd $CATKIN_WS/src/ && \
	git clone https://github.com/HKUST-Aerial-Robotics/VINS-Fusion.git

# Build VINS-Fusion
WORKDIR $CATKIN_WS
ENV TERM xterm
ENV PYTHONIOENCODING UTF-8
RUN catkin config \
      --extend /opt/ros/kinetic \
      --cmake-args \
        -DCMAKE_BUILD_TYPE=Release && \
    catkin build -j2 && \
    sed -i '/exec "$@"/i \
            source "/root/catkin_ws/devel/setup.bash"' /ros_entrypoint.sh

# realsense
RUN apt -q -qq update && \
  DEBIAN_FRONTEND=noninteractive apt install -y --allow-unauthenticated \
  python-rosinstall \
  python-catkin-tools \
  ros-kinetic-jsk-tools \
  ros-kinetic-rgbd-launch \
  ros-kinetic-image-transport-plugins \
  ros-kinetic-image-transport \
  software-properties-common

RUN echo 'deb http://realsense-hw-public.s3.amazonaws.com/Debian/apt-repo xenial main' || tee /etc/apt/sources.list.d/realsense-public.list
RUN apt-key adv --keyserver keys.gnupg.net --recv-key C8B3A55A6F3EFCDE || apt-key adv --keyserver hkp://keys.gnupg.net:80 --recv-key C8B3A55A6F3EFCDE
RUN add-apt-repository "deb http://realsense-hw-public.s3.amazonaws.com/Debian/apt-repo xenial main"
RUN apt-get update && apt-get install --allow-unauthenticated -y \
	librealsense2-dkms \
	librealsense2-dev  \
	librealsense2-utils \
	librealsense2-dbg
	
RUN rosdep update

RUN mkdir -p $CATKIN_WS//src && cd $CATKIN_WS/src && \
  git clone --depth 1 https://github.com/IntelRealSense/realsense-ros.git && \
  git clone --depth 1 https://github.com/pal-robotics/ddynamic_reconfigure
RUN cd $CATKIN_WS/;
RUN mv /bin/sh /bin/sh_tmp && ln -s /bin/bash /bin/sh
RUN source /opt/ros/${ROS_DISTRO}/setup.bash; cd $CATKIN_WS/; catkin build -DCATKIN_ENABLE_TESTING=False -DCMAKE_BUILD_TYPE=Release
RUN rm /bin/sh && mv /bin/sh_tmp /bin/sh
RUN touch /root/.bashrc && \
  echo "source $CATKIN_WS//devel/setup.bash\n" >> /root/.bashrc && \
  echo "rossetip\n" >> /root/.bashrc && \
  echo "rossetmaster localhost"
