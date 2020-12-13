#!/bin/bash
pathDatasetEuroc='/mnt/share/slam/dataset' #Example, it is necesary to change it by the dataset path

#------------------------------------
# Stereo-Inertial Examples
echo "Launching MH01 with Stereo-Inertial sensor"
./Examples/Stereo-Inertial/stereo_inertial_euroc ./Vocabulary/ORBvoc.txt ./Examples/Stereo-Inertial/EuRoC.yaml "$pathDatasetEuroc"/MH_01_easy ./Examples/Stereo-Inertial/EuRoC_TimeStamps/MH01.txt dataset-MH01_stereoi
