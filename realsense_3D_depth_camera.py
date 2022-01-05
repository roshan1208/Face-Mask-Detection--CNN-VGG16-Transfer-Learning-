import pyrealsense2 as rs
import numpy as np


class RealsenseCamera:
    def __init__(self):

        self.pc = rs.pointcloud()
        self.points = rs.points()
        self.pipeline = rs.pipeline()
        config = rs.config()

        config.enable_stream(rs.stream.depth, 1280,720,rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 1280,720,rs.format.bgr8, 30)

        self.pipe_profile = self.pipeline.start(config)
        align_to = rs.stream.color
        self.align = rs.align(align_to)


    def get_frame_stream(self):
        frames = self.pipeline.wait_for_frames()
        aligned_frames = self.align.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        # Apply filter to fill the Holes in the depth image
        spatial = rs.spatial_filter()
        spatial.set_option(rs.option.holes_fill, 3)
        filtered_depth = spatial.process(depth_frame)

        hole_filling = rs.hole_filling_filter()
        filled_depth = hole_filling.process(filtered_depth)

        
        # Create colormap to show the depth of the Objects
        colorizer = rs.colorizer()
        depth_colormap = np.asanyarray


        img_color = np.asanyarray(color_frame.get_data())
        img_depth = np.asanyarray(filled_depth.get_data())
        depth_intrin = depth_frame.profile.as_video_stream_profile().intrinsics
        color_intrin = color_frame.profile.as_video_stream_profile().intrinsics
        depth_to_color_extrin = depth_frame.profile.get_extrinsics_to(color_frame.profile)

        depth_sensor = self.pipe_profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()

        return True, depth_intrin, depth_scale, img_color, img_depth

    def release(self):
        self.pipeline.stop()

