import PyRVC as RVC
import numpy as np
import cv2
import os
import open3d as o3d

def RemoveNan(points):
    """ remove nan value of point clouds

    Args:
        points (ndarray): N x 3 point clouds

    Returns:
        [ndarray]: N x 3 point clouds
    """
    find_index = ~np.isnan(points[:, 0])

    return points[find_index]
def Truncate(pc, xr=[-5, 5], yr=[-5, 5], zr=[5, 5]):
    """ crop point cloud by range

    Args:
        pc (ndarray): N x 3 point clouds
        xr (list, optional): Defaults to [-1, 1].
        yr (list, optional): Defaults to [-1, 1].
        zr (list, optional): Defaults to [0, 2].
    """
    def TruncateOne(pc, c, r):
        return np.logical_and(pc[:, c] > r[0], pc[:, c] < r[1])
    xb = TruncateOne(pc, 0, xr)
    yb = TruncateOne(pc, 1, yr)
    zb = TruncateOne(pc, 2, zr)

    return pc[np.logical_and(np.logical_and(xb, yb), zb)]
#if __name__ == "__main__":


class myrvc:
    def __init__(self, exposure_time_2d,exposure_time_3d,gain_2d=0,gain_3d=0,gamma_2d=1,gamma_3d=1, light_contrast_threshold=4,
                 edge_noise_reduction_threshold = 1,projector_color = RVC.ProjectorColor_Blue,transform_to_camera = RVC.CameraID_Left,
                 projector_brightness = 240,use_projector_capturing_2d_image = True):

        RVC.SystemInit()
        self.cap_opt = RVC.X2_CaptureOptions()
        self.cap_opt.exposure_time_2d = exposure_time_2d
        self.cap_opt.exposure_time_3d = exposure_time_3d
        self.cap_opt.gain_2d = gain_2d
        self.cap_opt.gain_3d = gain_3d
        # Set 2d and 3d gamma. the default value is 1. The gamma value of each series cameras is different, you can call function GetGammaRange() to get specific range.
        self.cap_opt.gamma_2d = gamma_2d
        self.cap_opt.gamma_3d = gamma_3d
        # range in [0, 10]. the default value is 3. The contrast of point less than this value will be treat * as invalid point and be removed.
        self.cap_opt.light_contrast_threshold = light_contrast_threshold
        # edge control after point matching, range in [0, 10], default = 2. The big the value, the more edge * noise to be
        # removed.
        self.cap_opt.edge_noise_reduction_threshold = edge_noise_reduction_threshold
        # Set projector color. the default value is RVC.ProjectorColor_Blue.
        self.cap_opt.projector_color = projector_color
        self.cap_opt.transform_to_camera = transform_to_camera
        self.cap_opt.projector_brightness = projector_brightness
        # Set 2d image whether use projector. Only gray camera setting this option work.
        self.cap_opt.use_projector_capturing_2d_image = use_projector_capturing_2d_image

            # Open RVC X Camera


            # Set capture parameters

            # Transform point map's coordinate to left/right(RVC.CameraID_Left/RVC.CameraID_Right) camera or reference
            # plane(RVC.CameraID_NONE)

    def camera_is_connect(self):
        """
        check connect state of camera
        :returns 0:正常连接
                str:运行出错具体情况
        """
        if len(self.devices) == 0:
            return "Can not find any RVC X Camera!"
        elif self.x.IsValid() == False:
            return "RVC X Camera is not valid!"
        elif self.x.IsOpen() == False:
            return "RVC X Camera is not opened!"
        return 0


    def opencamera(self):
        # Choose RVC X Camera type (USB or GigE)
        opt = RVC.SystemListDeviceTypeEnum.GigE

        # Scan all RVC X Camera devices
        ret, self.devices = RVC.SystemListDevices(opt)
        print("RVC X Camera devices number:", len(self.devices))

        # Find whether any RVC X Camera is connected or not
        if len(self.devices) == 0:
            print("Can not find any RVC X Camera!")
            RVC.SystemShutdown()
            exit(1)

            # Create a RVC X Camera
        self.x = RVC.X2.Create(self.devices[0])

        # Test RVC X Camera is valid or not
        if self.x.IsValid() == False:
            print("RVC X Camera is not valid!")
            RVC.X2.Destroy(self.x)
            RVC.SystemShutdown()
            exit(1)
        self.ret1 = self.x.Open()

        # Test RVC X Camera is opened or not
        if self.x.IsOpen() == False:
            print("RVC X Camera is not opened!")
            RVC.X2.Destroy(self.x)
            RVC.SystemShutdown()
            exit(1)

    def capture(self, path):
        self.ret2 = self.x.Capture(self.cap_opt)
        if self.ret2 == True:
            # Get image data. choose left or right side. the point map is map to left image.
            # Create saving address of image and point map.
            save_dir = "Data"
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            img = self.x.GetImage(RVC.CameraID_Left)

            # Convert image to array and save it.
            img = np.array(img, copy=False)
            cv2.imwrite("{}/test.png".format(save_dir), img)
            print("Save image successed!")

            # Convert point map to array and save it.
            pm = np.array(self.x.GetPointMap(), copy=False).reshape(-1, 3)
            pts = RemoveNan(pm)
            print("before truncate pts num:{}".format(pts.shape[0]))
            # Truncate points.You can set :X,Y and Z range
            pts = Truncate(pts, xr=[-1, 1], yr=[-1, 1], zr=[-1, 1])
            print("after truncate pts num:{}".format(pts.shape[0]))
            save_point = o3d.geometry.PointCloud()
            save_point.points = o3d.utility.Vector3dVector(pts)

            o3d.io.write_point_cloud(path + "/save_point.ply", save_point)
            return pts

        else:
            print("RVC X Camera capture failed!")
            self.x.Close()
            RVC.X2.Destroy(self.x)
            RVC.SystemShutdown()
            exit(0)
        # Close RVC X Camera



    def closecamera(self):
        self.x.Close()

            # Destroy RVC X Camera
        RVC.X2.Destroy(self.x)

            # Shut Down RVC X System
        RVC.SystemShutdown()

            # Capture a point map and a image.


