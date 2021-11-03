#!/usr/bin/env python
import sys
import os
import rospy
from sensor_msgs.msg import Image
from sensor_msgs.msg import Imu

import cv2
from cv_bridge import CvBridge
import threading
import time
import copy

class UnsycImgLoader(threading.Thread):
    def __init__(self, next_img0_path, next_img1_path):
        threading.Thread.__init__(self)
        self.block = True
        self.kill = False
        self.img_id = 0
        self.img0 = None
        self.img1 = None
        self.next_img0_path = next_img0_path
        self.next_img1_path = next_img1_path

    def run(self):
        while(self.kill == False):
            if(self.block == True):
                #print("read img")
                #load image
                if(self.next_img0_path is None or self.next_img1_path is None):
                    self.kill = True
                    print("file end")
                    break
                self.img0 = cv2.imread(os.path.join(euroc_data_path, "mav0/cam0/data", self.next_img0_path), cv2.IMREAD_GRAYSCALE)
                self.img1 = cv2.imread(os.path.join(euroc_data_path, "mav0/cam1/data", self.next_img1_path), cv2.IMREAD_GRAYSCALE)
                #end load image
                self.img_id += 1
                self.block = False
            else:
                #print("run")
                time.sleep(0.001) #1ms

    def retrieveImgAndReadNextImg(self, next_img0_path, next_img1_path):
        while(self.kill == False and self.block == True):
            #wait until load
            time.sleep(0.001) #1ms
        
        img0_ = copy.deepcopy(self.img0)
        img1_ = copy.deepcopy(self.img1)
        self.next_img0_path = next_img0_path
        self.next_img1_path = next_img1_path
        self.block = True

        return img0_, img1_

    def terminate(self):
        self.kill = True

def publisher(euroc_data_path):
    rospy.init_node('EuRoC_publisher', anonymous=True)
    pub_cam0 = rospy.Publisher('/cam0/image_raw', Image, queue_size=10)
    pub_cam1 = rospy.Publisher('/cam1/image_raw', Image, queue_size=10)
    pub_imu0 = rospy.Publisher('/imu0', Imu, queue_size=10)

    #read data
    euroc_mav0_path = os.path.join(euroc_data_path, "mav0")
    #cam0
    datalist_cam0 = []
    datalist_cam1 = []
    datalist_imu0 = []
    with open(os.path.join(euroc_mav0_path, "cam0/data.csv")) as f:
        for line in f:
           line = line.replace( '\n' , '' )
           line = line.replace( '\r' , '' )
           l = line.split(',')
           datalist_cam0.append(l)
        del datalist_cam0[0]
    #cam1
    with open(os.path.join(euroc_mav0_path, "cam1/data.csv")) as f:
        for line in f:
           line = line.replace( '\n' , '' )
           line = line.replace( '\r' , '' )
           l = line.split(',')
           datalist_cam1.append(l)
        del datalist_cam1[0]
    #imu
    with open(os.path.join(euroc_mav0_path, "imu0/data.csv")) as f:
        for line in f:
           line = line.replace( '\n' , '' )
           line = line.replace( '\r' , '' )
           l = line.split(',')
           #timestamp [ns]	w_RS_S_x [rad s^-1]	w_RS_S_y [rad s^-1]	w_RS_S_z [rad s^-1]	a_RS_S_x [m s^-2]	a_RS_S_y [m s^-2]	a_RS_S_z [m s^-2]
           datalist_imu0.append(l)
        del datalist_imu0[0]

    if(len(datalist_cam0) == 0 or \
        len(datalist_cam1) == 0 or \
        len(datalist_cam0) != len(datalist_cam1)):
        print("invalid data")

    bridge = CvBridge()

    start_nsec = rospy.Time.now().to_nsec()
    data_time_offset = start_nsec - int(datalist_imu0[0][0])
    print(start_nsec)
    print(int(datalist_imu0[0][0]))

    img_loader = UnsycImgLoader(datalist_cam0[0][1], datalist_cam1[1][1])
    img_loader.start()

    img_idx = 0
    imu_idx = 0
    while not rospy.is_shutdown():
        cur_nsec = rospy.Time.now().to_nsec() - data_time_offset
        #print(cur_nsec)

        #data end check
        if(len(datalist_cam0) <= img_idx or len(datalist_imu0) <= imu_idx):
            break

        #imu
        if(int(datalist_imu0[imu_idx][0]) < cur_nsec):
            print("imu", datalist_imu0[imu_idx][0])
            imu_idx += 1

            ros_timestamp_imu0 = rospy.Time.from_sec(float(datalist_imu0[imu_idx][0]) * 1e-9)

            msg_imu0 = Imu()
            msg_imu0.header.stamp = ros_timestamp_imu0
            msg_imu0.header.frame_id = str(imu_idx)
            msg_imu0.angular_velocity.x = float(datalist_imu0[imu_idx][1])
            msg_imu0.angular_velocity.y = float(datalist_imu0[imu_idx][2])
            msg_imu0.angular_velocity.z = float(datalist_imu0[imu_idx][3])
            msg_imu0.linear_acceleration.x = float(datalist_imu0[imu_idx][4])
            msg_imu0.linear_acceleration.y = float(datalist_imu0[imu_idx][5])
            msg_imu0.linear_acceleration.z = float(datalist_imu0[imu_idx][6])

            pub_imu0.publish(msg_imu0)

        #img
        if(int(datalist_cam0[img_idx][0]) < cur_nsec):
            print("img", datalist_cam0[img_idx][0])
            img_idx += 1

            ros_timestamp_cam0 = rospy.Time.from_sec(float(datalist_cam0[img_idx][0]) * 1e-9)
            ros_timestamp_cam1 = rospy.Time.from_sec(float(datalist_cam1[img_idx][0]) * 1e-9)
            
            #img_cam0 = cv2.imread(os.path.join(euroc_data_path, "mav0/cam0/data", datalist_cam0[i][1]), cv2.IMREAD_GRAYSCALE)
            #img_cam1 = cv2.imread(os.path.join(euroc_data_path, "mav0/cam1/data", datalist_cam1[i][1]), cv2.IMREAD_GRAYSCALE)
            img_cam0, img_cam1 = img_loader.retrieveImgAndReadNextImg(datalist_cam0[img_idx + 1][1], datalist_cam1[img_idx + 1][1])

            if(img_cam0 is None or img_cam1 is None):
                break

            #cv2.imshow("cam0", img_cam0)
            #cv2.imshow("cam1", img_cam1)
            #key = cv2.waitKey(16)
            #if(key == 'q'):
            #    print("keyboard interrupt")
            #    break

            msg_cam0 = bridge.cv2_to_imgmsg(img_cam0, encoding="mono8")
            msg_cam0.header.stamp = ros_timestamp_cam0
            msg_cam0.header.frame_id = str(img_idx)
            msg_cam0.height = img_cam0.shape[0]
            msg_cam0.width = img_cam0.shape[1]
            msg_cam1 = bridge.cv2_to_imgmsg(img_cam1, encoding="mono8")
            msg_cam1.header.stamp = ros_timestamp_cam1
            msg_cam1.header.frame_id = str(img_idx)
            msg_cam1.height = img_cam1.shape[0]
            msg_cam1.width = img_cam1.shape[1]

            pub_cam0.publish(msg_cam0)
            pub_cam1.publish(msg_cam1)

    img_loader.terminate()    
    return

if __name__ == '__main__':
    if(len(sys.argv) < 2):
        print("usage: EuRoC path")
    
    euroc_data_path = sys.argv[1]
    try:
        publisher(euroc_data_path)
    except rospy.ROSInterruptException:
        pass