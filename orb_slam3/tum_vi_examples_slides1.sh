#!/bin/bash
pathDatasetTUM_VI='/mnt/share/slam/dataset' #Example, it is necesary to change it by the dataset path

#------------------------------------
# Stereo Examples
echo "Launching Slides 1 with Stereo-Inertial sensor"
./Examples/Stereo-Inertial/stereo_inertial_tum_vi Vocabulary/ORBvoc.txt Examples/Stereo-Inertial/TUM_512.yaml "$pathDatasetTUM_VI"/dataset-slides1_512_16/mav0/cam0/data "$pathDatasetTUM_VI"/dataset-slides1_512_16/mav0/cam1/data Examples/Stereo-Inertial/TUM_TimeStamps/dataset-slides1_512.txt Examples/Stereo-Inertial/TUM_IMU/dataset-slides1_512.txt dataset-slides1_512_stereoi

