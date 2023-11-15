import pyrealsense2 as rs
import numpy as np

class TwoCameras():
    def __init__(self) -> None:
        # 确定图像的输入分辨率与帧率
        resolution_width = 640  # pixels
        resolution_height = 360  # pixels
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
        self.thr_filter.set_option(rs.option.min_distance,0.29)
        self.thr_filter.set_option(rs.option.max_distance,10.0)


        # 注册数据流，并对其图像
        self.align = rs.align(rs.stream.color)
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
        
        # 确认相机并获取相机的内部参数
        self.pipeline1 = rs.pipeline()
        rs_config.enable_device(connect_device[0])
        # pipeline_profile1 = pipeline1.start(rs_config)
        self.pipeline1.start(rs_config)

        self.pipeline2 = rs.pipeline()
        rs_config.enable_device(connect_device[1])
        # pipeline_profile2 = pipeline2.start(rs_config)
        self.pipeline2.start(rs_config)


    def get_image(self):
        # 等待数据进来
        frames1 = self.pipeline1.wait_for_frames()
        frames2 = self.pipeline2.wait_for_frames()

        # 将进来的RGBD数据对齐
        aligned_frames1 = self.align.process(frames1)
        aligned_frames2 = self.align.process(frames2)

        # 将对其的RGB—D图取出来
        color_frame1 = aligned_frames1.get_color_frame()
        color_frame2 = aligned_frames2.get_color_frame()

        color_image1 = np.asanyarray(color_frame1.get_data())
        color_image2 = np.asanyarray(color_frame2.get_data())

        return color_image1, color_image2 # left, right

    def get_image_with_depth(self):
        # 等待数据进来
        frames1 = self.pipeline1.wait_for_frames()
        frames2 = self.pipeline2.wait_for_frames()

        # 将进来的RGBD数据对齐
        aligned_frames1 = self.align.process(frames1)
        aligned_frames2 = self.align.process(frames2)

        # 将对其的RGB—D图取出来
        color_frame1 = aligned_frames1.get_color_frame()
        color_frame2 = aligned_frames2.get_color_frame()

        color_image1 = np.asanyarray(color_frame1.get_data())
        color_image2 = np.asanyarray(color_frame2.get_data())

        depth_frame1 = frames1.get_depth_frame()
        '''
        depth_frame1 = self.thr_filter.process(depth_frame1)
        depth_frame1 = self.depth_to_disparity.process(depth_frame1)
        depth_frame1 = self.spatial.process(depth_frame1)
        depth_frame1 = self.disparity_to_depth.process(depth_frame1)
        depth_frame1 = self.hole_filling.process(depth_frame1)
        '''

        depth_frame2 = frames2.get_depth_frame()
        '''
        depth_frame2 = self.thr_filter.process(depth_frame2)
        depth_frame2 = self.depth_to_disparity.process(depth_frame2)
        depth_frame2 = self.spatial.process(depth_frame2)
        depth_frame2 = self.disparity_to_depth.process(depth_frame2)
        depth_frame2 = self.hole_filling.process(depth_frame2)
        '''

        depth_image1 = np.asanyarray(depth_frame1.get_data())
        depth_image2 = np.asanyarray(depth_frame2.get_data())

        return color_image1, color_image2, depth_image1, depth_image2# left, right
    

if __name__ == "__main__":
    cameras = TwoCameras()
    c1, c2 = cameras.get_image()
    print(c1.shape, c2.shape)