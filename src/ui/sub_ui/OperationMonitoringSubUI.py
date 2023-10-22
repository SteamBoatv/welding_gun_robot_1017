import os
import time

from PyQt5 import QtWidgets, QtGui

from UI.sub_UI import OperationMonitoring
import pyqtgraph.opengl as gl
import numpy as np
import open3d as o3d
import src.global_var as glo
from pyqtgraph.opengl import GLViewWidget
from selfTools.littleTools import LittleTools
from src.ui.sub_ui.CommunicationSettingSubUI import CommunicationSettingSubUI
from rascn import point_cal


class OperationMonitoringSubUI(QtWidgets.QMainWindow, OperationMonitoring.Ui_MainWindow):
    def __init__(self, parent=None):
        super(OperationMonitoringSubUI, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("运行检测")

        self.pushButton_show_pointcloud.clicked.connect(self.show_pointCloud)
        self.pushButton_run.clicked.connect(self.run)

        # 点云显示控件
        self.graphicsView = GLViewWidget(self)

        # 显示坐标轴
        x = gl.GLLinePlotItem(pos=np.asarray([[0, 0, 0], [0.2, 0, 0]]), color=(1, 0, 0, 1), width=0.005)
        y = gl.GLLinePlotItem(pos=np.asarray([[0, 0, 0], [0, 0.2, 0]]), color=(0, 1, 0, 1), width=0.005)
        z = gl.GLLinePlotItem(pos=np.asarray([[0, 0, 0], [0, 0, 0.2]]), color=(0, 0, 1, 1), width=0.005)
        self.graphicsView.addItem(x)
        self.graphicsView.addItem(y)
        self.graphicsView.addItem(z)

        self.horizontalLayout_2.addWidget(self.graphicsView)
        # self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 5)

    # 自己写的函数 实现功能为:
    # 2.TCP 移动到第"一"个相机坐标点
    # 3.拍照
    # 4.python算法计算直线两端点位置 P1 P2
    # 5.TCP 发消息移动到 P1->P2 (之后改为焊接)
    # 6.TCP 发消息 移动回第"一"个相机坐标点
    def moveAndCaptureAndWelding(self, whichPoint):
        # whichPoint代表的是 TCP原点 不带工具坐标系
        communicationsettingsubui = CommunicationSettingSubUI()
        littletools = LittleTools()
        # 1.找到四个相机坐标点 存在程序里的参数
        # 此处的positon是 8列 第2-7列才是有效的
        position = glo.get_value("position")
        position = np.asarray(position)
        position = position[:, 2:]
        print("in moveAndCaptureAndWelding")
        # 获取对应焊接行的坐标信息
        temp = position[whichPoint]
        # 将焊接数组转化为焊接字符串 准备给机器人传参
        temp = littletools.formatTo9(temp)
        # 2.TCP 移动到第"一"个相机坐标点
        # str1 : '+',‘1’,‘6’,'0',0.000-0027.013-0231.983....
        str1 = ''.join([str(x) for x in temp])

        curWPR = littletools.convert_to_number_array(str1)
        curWPR = curWPR[3:]

        FUNUC_moveToCamera = "movpXYZWPR" + str1
        cameraPosition = str1
        # 2.1 发送坐标进行移动
        result = littletools.tcp_send_and_recv(FUNUC_moveToCamera)
        time.sleep(20)
        print("result in LittleTools.tcp_send_and_recv(temp)1 : " + result)
        # 3.拍照
        communicationsettingsubui.capture()
        # 4.python算法计算直线两端点位置 P1 P2
        pass
        # 4.1 给FANUC 发送getTcp 获取当前工具坐标系信息
        FANUCtcpPosition = littletools.tcp_send_and_recv("getTcp")
        FANUCtcpPosition = littletools.FANUCpositionToPython(FANUCtcpPosition)
        print(FANUCtcpPosition)
        point1, point2 = point_cal(FANUCtcpPosition)
        # 5.TCP 发消息移动到 P1->P2 (之后改为焊接)
        point1 = list(point1)
        point2 = list(point2)
        point1.extend(curWPR)
        point2.extend(curWPR)
        # point1 : [1249.504,359.842,42.905,178.901,39.843,139.187]
        weldPoint1, weldPoint2 = littletools.formatToAtoB(point1, point2)
        # 焊接 ab俩个点 用纯移动来代替
        FANUC_weldBegin = "moveXYZWPR" + weldPoint1
        littletools.tcp_send_and_recv(FANUC_weldBegin)
        time.sleep(8)
        FANUC_weldEnd = "moveXYZWPR" + weldPoint2
        littletools.tcp_send_and_recv(FANUC_weldEnd)
        time.sleep(10)
        print("successfully weld")
        # 6. TCP发消息 返回点
        print("whichPoint is :")
        print(whichPoint)
        if whichPoint == 1:
            bias_x = -30
            bias_y = 30
            bias_point1 = point1[:]
            bias_point1[0] += bias_x
            bias_point1[1] += bias_y

            bias_point2 = point2[:]
            bias_point2[0] += bias_x
            bias_point2[1] += bias_y
        if whichPoint == 2:
            bias_x = 30
            bias_y = 30
            bias_point1 = point1[:]
            bias_point1[0] += bias_x
            bias_point1[1] += bias_y

            bias_point2 = point2[:]
            bias_point2[0] += bias_x
            bias_point2[1] += bias_y

        weldBiasPoint1, weldBiasPoint2 = littletools.formatToAtoB(bias_point1, bias_point2)

        FAUNC_moveToBiasPoint2 = "moveXYZWPR" + weldBiasPoint2
        littletools.tcp_send_and_recv(FAUNC_moveToBiasPoint2)
        time.sleep(8)
        print("FAUNC_moveToBiasPoint2:")
        print(FAUNC_moveToBiasPoint2)
        FAUNC_moveToBiasPoint1 = "moveXYZWPR" + weldBiasPoint1
        littletools.tcp_send_and_recv(FAUNC_moveToBiasPoint1)
        time.sleep(8)
        print("FAUNC_moveToBiasPoint1:")
        print(FAUNC_moveToBiasPoint1)

        # 7.TCP 发消息 移动回第"一"个相机坐标点
        temp = "movpXYZWPR" + cameraPosition
        result = littletools.tcp_send_and_recv(temp)
        print("result in LittleTools.tcp_send_and_recv(temp)3 : " + result)
        time.sleep(8)
    def run(self):
        # 点击红色 ”一键启动“之后运行的代码：
        # 1.找到四个相机坐标点 存在程序里的参数
        for i in range(4):
            self.moveAndCaptureAndWelding(i + 1)
        # 7.开始第二次循环

        # 作者的源码：
        # self.min.run()

    def init(self):
        pass

    def show_pointCloud(self):
        # 读取点云 并显示在右侧界面上
        # fileName, filetype = QFileDialog.getOpenFileName(self, "请选择图像：", '.', "All Files(*);;")
        # if fileName != '':
        # pcd = o3d.io.read_point_cloud(os.path.join(glo.get_value("project_path"), "save_point.ply"))
        pcd = o3d.io.read_point_cloud(os.path.join("./././Data", "save_point.ply"))
        # 获取 Numpy 数组
        np_points = np.asarray(pcd.points)
        # 创建显示对象
        plot = gl.GLScatterPlotItem()
        # 设置显示数据
        plot.setData(pos=np_points, color=(1, 1, 1, 1), size=0.0005, pxMode=False)
        # 显示点云
        self.graphicsView.addItem(plot)
        pass

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
