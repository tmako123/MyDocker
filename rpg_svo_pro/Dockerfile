FROM osrf/ros:melodic-desktop-full
LABEL maintainer="tmako123 <https://github.com/tmako123/>"

ENV DEBIAN_FRONTEND noninteractive

RUN apt update && apt install vim python-catkin-tools python-vcstool python-pip python-git python-setuptools python-termcolor python-wstool git libatlas3-base wget libglew-dev libopencv-dev libyaml-cpp-dev libblas-dev liblapack-dev libsuitesparse-dev autoconf automake libtool --yes

RUN mkdir svo_ws && cd svo_ws && \
catkin config --init --mkdirs --extend /opt/ros/melodic --cmake-args -DCMAKE_BUILD_TYPE=Release -DEIGEN3_INCLUDE_DIR=/usr/include/eigen3 && \
cd src && \
git clone https://github.com/uzh-rpg/rpg_svo_pro_open.git && \
sed -i 's/git@github.com:/https:\/\/github.com\//g' ./rpg_svo_pro_open/dependencies.yaml && \
vcs-import < ./rpg_svo_pro_open/dependencies.yaml && \
sed -i 's/git@github.com:/https:\/\/github.com\//g' ./dbow2_catkin/CMakeLists.txt && \
touch minkindr/minkindr_python/CATKIN_IGNORE && \
cd rpg_svo_pro_open/svo_online_loopclosing/vocabularies && ./download_voc.sh && \
cd ../../..

RUN cd svo_ws/src && \
rm rpg_svo_pro_open/svo_global_map/CATKIN_IGNORE && \
sed 'a SET(USE_GLOBAL_MAP TRUE)' rpg_svo_pro_open/svo_cmake/cmake/Modules/SvoSetup.cmake

RUN cd svo_ws/src && \
git clone --branch 4.0.3 http://github.com/borglab/gtsam.git && \
sed -i 's/use the one bundled with GTSAM" OFF)/use the one bundled with GTSAM" ON)/g' ./gtsam/CMakeLists.txt && \
sed -i 's/list_append_cache(GTSAM_COMPILE_OPTIONS_PUBLIC "-march=native")`/list_append_cache(GTSAM_COMPILE_OPTIONS_PUBLIC "-march=native")`\\nlist_append_cache(GTSAM_COMPILE_OPTIONS_PUBLIC "-mno-avx")/g' ./gtsam/cmake/GtsamBuildTypes.cmake

RUN cd svo_ws && \
catkin build
