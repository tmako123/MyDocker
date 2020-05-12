FROM osrf/ros:kinetic-desktop-full
LABEL maintainer="tmako123 <https://github.com/tmako123/>"

ENV CERES_VERSION="1.12.0"
ENV CATKIN_WS=/catkin_ws

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

RUN rosdep update
RUN mv /bin/sh /bin/sh_tmp && ln -s /bin/bash /bin/sh
RUN source /opt/ros/kinetic/setup.bash

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
    catkin build && \
    sed -i '/exec "$@"/i \
            source "/catkin_ws/devel/setup.bash"' /ros_entrypoint.sh
