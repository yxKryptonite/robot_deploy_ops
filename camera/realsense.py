import pyrealsense2 as rs
import cv2
import numpy as np
import time
import os
import sys

if __name__ == '__main__':


    # 确定图像的输入分辨率与帧率
    resolution_width = 640  # pixels
    resolution_height = 360  # pixels
    frame_rate = 60  # fps

    # 注册数据流，并对其图像
    align = rs.align(rs.stream.color)
    rs_config = rs.config()
    rs_config.enable_stream(rs.stream.depth, resolution_width, resolution_height, rs.format.z16, frame_rate)
    rs_config.enable_stream(rs.stream.color, resolution_width, resolution_height, rs.format.bgr8, frame_rate)
    ### d415
    #
    rs_config.enable_stream(rs.stream.infrared, 1, resolution_width, resolution_height, rs.format.y8, frame_rate)
    rs_config.enable_stream(rs.stream.infrared, 2, resolution_width, resolution_height, rs.format.y8, frame_rate)
    # check相机是不是进来了
    connect_device = []
    for d in rs.context().devices:
        print('Found device: ',
              d.get_info(rs.camera_info.name), ' ',
              d.get_info(rs.camera_info.serial_number))
        if d.get_info(rs.camera_info.name).lower() != 'platform camera':
            connect_device.append(d.get_info(rs.camera_info.serial_number))


    if len(connect_device) < 2:
        print('Registrition needs two camera connected.But got one.')
        exit()

    # 确认相机并获取相机的内部参数
    pipeline1 = rs.pipeline()
    rs_config.enable_device(connect_device[0])
    # pipeline_profile1 = pipeline1.start(rs_config)
    pipeline1.start(rs_config)

    pipeline2 = rs.pipeline()
    rs_config.enable_device(connect_device[1])
    # pipeline_profile2 = pipeline2.start(rs_config)
    pipeline2.start(rs_config)

    try:
        time = 0
        os.makedirs("/home/yons/桌面/data_calib/rgb/left",exist_ok=True)
        os.makedirs("/home/yons/桌面/data_calib/rgb/right",exist_ok=True)
        os.makedirs("/home/yons/桌面/data_calib/depth/left",exist_ok=True)
        os.makedirs("/home/yons/桌面/data_calib/depth/right",exist_ok=True)
        while True:

            # 等待数据进来
            frames1 = pipeline1.wait_for_frames()
            frames2 = pipeline2.wait_for_frames()

            # 将进来的RGBD数据对齐
            aligned_frames1 = align.process(frames1)
            aligned_frames2 = align.process(frames2)

            # 将对其的RGB—D图取出来
            color_frame1 = aligned_frames1.get_color_frame()
            color_frame2 = aligned_frames2.get_color_frame()

            color_image1 = np.asanyarray(color_frame1.get_data())
            color_image2 = np.asanyarray(color_frame2.get_data())

            depth_frame1 = aligned_frames1.get_depth_frame()
            depth_frame2 = aligned_frames2.get_depth_frame()

            depth_image1 = np.asanyarray(depth_frame1.get_data())
            depth_image2 = np.asanyarray(depth_frame2.get_data())

            cv2.imshow('RealSense1', color_image1)
            cv2.imshow('RealSense2', color_image2)
            #cv2.imwrite(f'/home/yons/桌面/data_calib/rgb/left/{time}.png', color_image1)
            #cv2.imwrite(f'/home/yons/桌面/data_calib/depth/left/{time}.png', depth_image1)
            cv2.imwrite(f'/home/yons/桌面/data_calib/rgb/right/{time}.png', color_image2)
            cv2.imwrite(f'/home/yons/桌面/data_calib/depth/right/{time}.png', depth_image2)
            time += 1

            key = cv2.waitKey(1)

            if key & 0xFF == ord('q') or key == 27:
                cv2.destroyAllWindows()
                break
    finally:
        pipeline1.stop()
        pipeline2.stop()