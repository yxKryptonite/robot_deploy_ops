import pyrealsense2 as rs
import numpy as np
import cv2
import os

class Camera():
    def __init__(self, width, height) -> None:
        # 确定图像的输入分辨率与帧率
        resolution_width = width  # pixels
        resolution_height = height  # pixels
        frame_rate = 60  # fps

        self.decimation = rs.decimation_filter()
        self.spatial = rs.spatial_filter()
        self.spatial.set_option(rs.option.filter_magnitude, 5)
        self.spatial.set_option(rs.option.filter_smooth_alpha, 1)
        self.spatial.set_option(rs.option.filter_smooth_delta, 50)
        self.spatial.set_option(rs.option.holes_fill, 3)
        self.hole_filling = rs.hole_filling_filter()
        self.depth_to_disparity = rs.disparity_transform(True)
        self.disparity_to_depth = rs.disparity_transform(False)
        self.thr_filter = rs.threshold_filter()
        self.thr_filter.set_option(rs.option.min_distance,0.01)
        self.thr_filter.set_option(rs.option.max_distance,16.0)


        # 注册数据流，并对其图像
        self.align = rs.align(rs.stream.color)
        rs_config = rs.config()
        rs_config.enable_stream(rs.stream.depth, resolution_width, resolution_height, rs.format.z16, frame_rate)
        rs_config.enable_stream(rs.stream.color, resolution_width, resolution_height, rs.format.bgr8, frame_rate)
        ### d415
        #
        rs_config.enable_stream(rs.stream.infrared, 1, resolution_width, resolution_height, rs.format.y8, frame_rate)
        # rs_config.enable_stream(rs.stream.infrared, 2, resolution_width, resolution_height, rs.format.y8, frame_rate)

        # check相机是不是进来了
        connect_device = []
        for d in rs.context().devices:
            print('Found device: ',
                d.get_info(rs.camera_info.name), ' ',
                d.get_info(rs.camera_info.serial_number))
            if d.get_info(rs.camera_info.name).lower() != 'platform camera':
                connect_device.append(d.get_info(rs.camera_info.serial_number))
        
        # 确认相机并获取相机的内部参数
        self.pipeline = rs.pipeline()
        rs_config.enable_device(connect_device[0])
        # pipeline_profile1 = pipeline1.start(rs_config)
        self.pipeline.start(rs_config)


    def get_image(self):
        # 等待数据进来
        frames = self.pipeline.wait_for_frames()

        # 将进来的RGBD数据对齐
        aligned_frames = self.align.process(frames)

        # 将对其的RGB—D图取出来
        color_frame = aligned_frames.get_color_frame()

        color_image = np.asanyarray(color_frame.get_data())

        return color_image

    def get_image_with_depth(self, depth_filter=True):
        # 等待数据进来
        frames = self.pipeline.wait_for_frames()

        # 将进来的RGBD数据对齐
        aligned_frames = self.align.process(frames)

        # 将对其的RGB—D图取出来
        color_frame = aligned_frames.get_color_frame()

        color_image = np.asanyarray(color_frame.get_data())

        depth_frame = aligned_frames.get_depth_frame()
        
        if depth_filter:
            # depth_frame = self.decimation.process(depth_frame)
            depth_frame = self.thr_filter.process(depth_frame)
            depth_frame = self.depth_to_disparity.process(depth_frame)
            depth_frame = self.spatial.process(depth_frame)
            depth_frame = self.disparity_to_depth.process(depth_frame)
            depth_frame = self.hole_filling.process(depth_frame)

        depth_image = np.asanyarray(depth_frame.get_data())

        return color_image, depth_image
    
    def visualize(self):
        import cv2
        while True:
            c, d = self.get_image_with_depth()
            cv2.imshow('color', c)
            cv2.imshow('depth', d)
            cv2.waitKey(1)
    

if __name__ == "__main__":
    camera = Camera(width=640, height=480)
    c, d = camera.get_image_with_depth()
    print(c.shape, d.shape)
    c, d = camera.get_image_with_depth() # take a second shot
    for i in d:
        for j in i:
            if j > 10 and j < 1000:
                print(j)
    os.makedirs("./color",exist_ok=True)
    os.makedirs("./depth",exist_ok=True)
    cv2.imwrite("./color/1.png", c)
    cv2.imwrite("./depth/1.png", d)
    