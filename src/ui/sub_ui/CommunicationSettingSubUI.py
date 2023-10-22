import configparser
import os
import threading
import pyqtgraph.opengl as gl
import numpy as np

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QThread, pyqtSignal

from pyqtgraph.opengl import GLViewWidget
from UI.sub_UI import CommunicationSetting
import src.camera.myrvc as myrvc
import src.global_var as glo
import PyRVC as RVC
import open3d as o3d
from testcapture import myrvc

class CommunicationSettingSubUI(QtWidgets.QMainWindow, CommunicationSetting.Ui_MainWindow):
    def __init__(self, parent=None):
        super(CommunicationSettingSubUI, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("通信设置")

        self.pushButton_capture.clicked.connect(self.capture)
        self.pushButton_connect.clicked.connect(self.connectCamera)
        self.pushButton_disconnect.clicked.connect(self.disConnectCamera)
        self.pushButton.clicked.connect(self.acition)

        self.horizontalSlider_exposure_time_2d.valueChanged.connect(self.exposure_time_2d)
        self.horizontalSlider_exposure_time_3d.valueChanged.connect(self.exposure_time_3d)
        self.horizontalSlider_gain_2d.valueChanged.connect(self.gain_2d)
        self.horizontalSlider_gain_3d.valueChanged.connect(self.gain_3d)
        self.horizontalSlider_gamma_2d.valueChanged.connect(self.gamma_2d)
        self.horizontalSlider_gamma_3d.valueChanged.connect(self.gamma_3d)
        self.horizontalSlider_light_contrast_threshold.valueChanged.connect(self.light_contrast_threshold)
        self.horizontalSlider_edge_noise_reduction_threshold.valueChanged.connect(self.edge_noise_reduction_threshold)
        self.horizontalSlider_projector_brightness.valueChanged.connect(self.projector_brightness)

        # 点云显示控件
        self.graphicsView = GLViewWidget(self)

        # 显示坐标轴
        x = gl.GLLinePlotItem(pos=np.asarray([[0, 0, 0], [0.2, 0, 0]]), color=(1, 0, 0, 1), width=0.005)
        y = gl.GLLinePlotItem(pos=np.asarray([[0, 0, 0], [0, 0.2, 0]]), color=(0, 1, 0, 1), width=0.005)
        z = gl.GLLinePlotItem(pos=np.asarray([[0, 0, 0], [0, 0, 0.2]]), color=(0, 0, 1, 1), width=0.005)
        self.graphicsView.addItem(x)
        self.graphicsView.addItem(y)
        self.graphicsView.addItem(z)
        self.graphicsView.setGeometry(0, 110, 1920, 1080)

        # self.gridLayout.addWidget(self.graphicsView_1, 0, 1, 2, 2)
        # self.horizontalLayout_2.addWidget(self.graphicsView)
        self.horizontalLayout_2.insertWidget(1, self.graphicsView)
        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 5)
        self.horizontalLayout_2.setStretch(2, 0)

        self.show_pointCloud()

    def show_pointCloud(self):
        # 读取点云
        # fileName, filetype = QFileDialog.getOpenFileName(self, "请选择图像：", '.', "All Files(*);;")
        # if fileName != '':
        # pcd = o3d.io.read_point_cloud(r"D:\develop\python\code\welding_gun_robot\Car_body.ply")
        pcd = o3d.io.read_point_cloud("./././Data/save_point.ply")
        # 获取 Numpy 数组
        np_points = np.asarray(pcd.points)
        # 创建显示对象
        plot = gl.GLScatterPlotItem()
        # 设置显示数据
        plot.setData(pos=np_points, color=(1, 1, 1, 1), size=0.0005, pxMode=False)
        # 显示点云
        self.graphicsView.addItem(plot)
        pass

    def edge_noise_reduction_threshold(self):
        value = self.horizontalSlider_edge_noise_reduction_threshold.value()
        self.label_edge_noise_reduction_threshold.setText(
            self.label_edge_noise_reduction_threshold.text().split(":")[0] + ":" + str(value))

    def projector_brightness(self):
        value = self.horizontalSlider_projector_brightness.value()
        self.label_projector_brightness.setText(
            self.label_projector_brightness.text().split(":")[0] + ":" + str(value))

    def light_contrast_threshold(self):
        # send = self.sender().text()
        # print(send)
        value = self.horizontalSlider_light_contrast_threshold.value()
        self.label_light_contrast_threshold.setText(
            self.label_light_contrast_threshold.text().split(":")[0] + ":" + str(value))

    def gamma_3d(self):
        value = self.horizontalSlider_gamma_3d.value()
        self.label_gamma_3d.setText(
            self.label_gamma_3d.text().split(":")[0] + ":" + str(value))

    def gamma_2d(self):
        value = self.horizontalSlider_gamma_2d.value()
        self.label_gamma_2d.setText(
            self.label_gamma_2d.text().split(":")[0] + ":" + str(value))

    def gain_2d(self):
        value = self.horizontalSlider_gain_2d.value()
        self.label_gain_2d.setText(
            self.label_gain_2d.text().split(":")[0] + ":" + str(value))

    def gain_3d(self):
        value = self.horizontalSlider_gain_3d.value()
        self.label_gain_3d.setText(
            self.label_gain_3d.text().split(":")[0] + ":" + str(value))

    def exposure_time_2d(self):
        value = self.horizontalSlider_exposure_time_2d.value()
        self.label__exposure_time_2d.setText(
            self.label__exposure_time_2d.text().split(":")[0] + ":" + str(value))

    def exposure_time_3d(self):
        value = self.horizontalSlider_exposure_time_3d.value()
        self.label__exposure_time_3d.setText(
            self.label__exposure_time_3d.text().split(":")[0] + ":" + str(value))

    def cameraOk(self):
        print("参数确认")
        exposure_time_2d = self.horizontalSlider_exposure_time_2d.value()
        exposure_time_3d = self.horizontalSlider_exposure_time_3d.value()
        gain_2d = self.horizontalSlider_gain_2d.value()
        gain_3d = self.horizontalSlider_gain_3d.value()
        gamma_2d = self.horizontalSlider_gamma_2d.value()
        gamma_3d = self.horizontalSlider_gamma_3d.value()
        light_contrast_threshold = self.horizontalSlider_light_contrast_threshold.value()
        edge_noise_reduction_threshold = self.horizontalSlider_edge_noise_reduction_threshold.value()

        if self.comboBox_projector_color.currentText() == "blue":
            projector_color = RVC.ProjectorColor_Blue
        elif self.comboBox_projector_color.currentText() == "red":
            projector_color = RVC.BalanceSelector_Red
        elif self.comboBox_projector_color.currentText() == "green":
            projector_color = RVC.BalanceSelector_Green

        transform_to_camera = RVC.CameraID_Left if self.comboBox_transform_to_camera.currentText() == "左相机坐标系" else RVC.CameraID_Right
        projector_brightness = self.horizontalSlider_projector_brightness.value()
        use_projector_capturing_2d_image = True if self.comboBox_use_projector_capturing_2d_image.currentText() == "是" else False

        self.min.camera = myrvc.myrvc(exposure_time_2d, exposure_time_3d, gain_2d, gain_3d, gamma_2d, gamma_3d,
                                      light_contrast_threshold,
                                      edge_noise_reduction_threshold, projector_color, transform_to_camera,
                                      projector_brightness, use_projector_capturing_2d_image)

    class captureThread(QThread):
        # 处理业务逻辑
        update_data = pyqtSignal(str)
        flag = 1

        # 处理业务逻辑
        def run(self):
            self.update_data.emit("1")

    def capture(self):
        #点击拍摄 按钮后 相机开始拍摄
        rcv = glo.get_value("rcv")
        rcv.capture("./Data", "save_point")
        self.show_pointCloud()
        # 下面是原作者的内容
        #
        # self.pushButton_capture.setDisabled(True)
        # print("拍摄")
        # # self.th = self.captureThread()
        # # self.th.update_data.connect(self.min.camera.capture)
        # # self.th.start()
        #
        # t = threading.Thread(target=self._capture)
        # t.start()
        #
        # self.pushButton_capture.setDisabled(False)

    def _capture(self):
        # point = self.min.camera.capture("Data")
        point = self.min.camera.capture(glo.get_value("project_path"))
        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(point)
        point_cloud.paint_uniform_color([0.5, 0.5, 0.5])
        o3d.visualization.draw_geometries([point_cloud])

    def connectCamera(self):
        # 点击前端连接相机之后 调用该函数
        print("连接相机")
        rcv = glo.get_value("rcv")
        rcv.opencamera()
        glo.set_value("rcv",rcv)
        # 下面是原作者的内容
        # # instance
        # self.cameraOk()
        # try:
        #     self.min.camera.opencamera()
        #     self.label_camera_state.setText("连接")
        # except SystemExit as msg:
        #     self.label_camera_state.setText("断开")
        #     print(msg.with_traceback())
        #     return msg.code

    def disConnectCamera(self):
        # 断开相机链接
        rcv = glo.get_value("rcv")
        rcv.closecamera()
        print("相机关闭")
        # 原作者的内容
        # self.min.camera.closecamera()
        # self.label_camera_state.setText("断开")

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def init(self):
        self.load_para()

        self.edge_noise_reduction_threshold()
        self.projector_brightness()
        self.light_contrast_threshold()
        self.gamma_3d()
        self.gamma_2d()
        self.gain_2d()
        self.gain_3d()
        self.exposure_time_2d()
        self.exposure_time_3d()

        self.pushButton.setText("修改")
        self.frame_3.setDisabled(True)
        pass

    def acition(self):
        if self.pushButton.text() == "修改":
            self.change()
        elif self.pushButton.text() == "保存":
            self.save()

    def save(self):
        self.save_para()

        self.pushButton.setText("修改")
        self.frame_3.setDisabled(True)

    def change(self):
        self.pushButton.setText("保存")
        self.frame_3.setDisabled(False)

    def load_para(self):
        """
        read config.ini to load para
        """
        project_path = glo.get_value("project_path")
        # 在当前文件路径下查找.ini文件
        configPath = os.path.join(project_path, "camera_config.ini")
        print(configPath)
        conf = configparser.ConfigParser()
        # 读取.ini文件
        conf.read(configPath)

        section = "camera"
        exposure_time_2d = conf.get(section, "exposure_time_2d")
        exposure_time_3d = conf.get(section, "exposure_time_3d")
        gain_2d = conf.get(section, "gain_2d")
        gain_3d = conf.get(section, "gain_3d")
        gamma_2d = conf.get(section, "gamma_2d")
        gamma_3d = conf.get(section, "gamma_3d")
        light_contrast_threshold = conf.get(section, "light_contrast_threshold")
        edge_noise_reduction_threshold = conf.get(section, "edge_noise_reduction_threshold")
        projector_brightness = conf.get(section, "projector_brightness")
        projector_color = conf.get(section, "projector_color")
        transform_to_camera = conf.get(section, "transform_to_camera")
        use_projector_capturing_2d_image = conf.get(section, "use_projector_capturing_2d_image")

        self.horizontalSlider_exposure_time_2d.setValue(int(exposure_time_2d))
        self.horizontalSlider_exposure_time_3d.setValue(int(exposure_time_3d))
        self.horizontalSlider_gain_2d.setValue(int(gain_2d))
        self.horizontalSlider_gain_3d.setValue(int(gain_3d))
        self.horizontalSlider_gamma_2d.setValue(int(gamma_2d))
        self.horizontalSlider_gamma_3d.setValue(int(gamma_3d))
        self.horizontalSlider_light_contrast_threshold.setValue(int(light_contrast_threshold))
        self.horizontalSlider_edge_noise_reduction_threshold.setValue(int(edge_noise_reduction_threshold))
        self.horizontalSlider_projector_brightness.setValue(int(projector_brightness))
        self.comboBox_projector_color.setCurrentText(projector_color)
        self.comboBox_transform_to_camera.setCurrentText(transform_to_camera)
        self.comboBox_use_projector_capturing_2d_image.setCurrentText(use_projector_capturing_2d_image)

    def save_para(self):
        # 当前文件路径
        project_path = glo.get_value("project_path")
        # 在当前文件路径下查找.ini文件
        configPath = os.path.join(project_path, "camera_config.ini")
        print(configPath)
        conf = configparser.ConfigParser()

        section = "camera"
        conf.add_section(section)
        conf.set(section, "exposure_time_2d", str(self.horizontalSlider_exposure_time_2d.value()))
        conf.set(section, "exposure_time_3d", str(self.horizontalSlider_exposure_time_3d.value()))
        conf.set(section, "gain_2d", str(self.horizontalSlider_gain_2d.value()))
        conf.set(section, "gain_3d", str(self.horizontalSlider_gain_3d.value()))
        conf.set(section, "gamma_2d", str(self.horizontalSlider_gamma_2d.value()))
        conf.set(section, "gamma_3d", str(self.horizontalSlider_gamma_3d.value()))
        conf.set(section, "light_contrast_threshold", str(self.horizontalSlider_light_contrast_threshold.value()))
        conf.set(section, "edge_noise_reduction_threshold",
                 str(self.horizontalSlider_edge_noise_reduction_threshold.value()))
        conf.set(section, "projector_brightness", str(self.horizontalSlider_projector_brightness.value()))
        conf.set(section, "projector_color", str(self.comboBox_projector_color.currentText()))
        conf.set(section, "transform_to_camera", str(self.comboBox_transform_to_camera.currentText()))
        conf.set(section, "use_projector_capturing_2d_image",
                 str(self.comboBox_use_projector_capturing_2d_image.currentText()))

        conf.write(open(configPath, 'w+'))
