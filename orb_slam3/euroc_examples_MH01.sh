#!/bin/bash
pathDatasetEuroc='/mnt/share/slam/dataset' #Example, it is necesary to change it by the dataset path

#------------------------------------
# Stereo Examples
echo "Launching MH01 with Stereo sensor"
./Examples/Stereo/stereo_euroc ./Vocabulary/ORBvoc.txt ./Examples/Stereo/EuRoC.yaml "$pathDatasetEuroc"/MH_01_easy ./Examples/Stereo/EuRoC_TimeStamps/MH01.txt dataset-MH01_stereo
