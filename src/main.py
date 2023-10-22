import configparser
import os
import sys
import time
import logging
import socket

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QSplashScreen, QApplication
from PyQt5.QtCore import QThread, pyqtSignal

from UI import license_dialog, menu, reset_password_dialog, login_dialog, bottom_layer
# import src.ui.LoginDialog as LoginDialog
import src.auth as auth
from src import manage_position
from src import MyQThread
from src.camera import rascn
from src.ui.LoginDialog import LoginDialog
from src.ui.Ui_project_manage import projectManage
from src.ui.sub_ui.OperationMonitoringSubUI import OperationMonitoringSubUI
from src.ui.sub_ui.WeldingGunLibrarySubUI import WeldingGunLibrarySubUI
from src.ui.sub_ui.FunctionTestSubUI import FunctionTestSubUI
from src.ui.sub_ui.SettingSubUI import SettingSubUI
from src.ui.sub_ui.CommunicationSettingSubUI import CommunicationSettingSubUI

import src.ctrl_bot.ctrl_inexbot as ctrl_inexbot
from testcapture import myrvc
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

SETTING_PATH = "resource/setting.ini"

# 定义全局变量管理模块
import src.global_var as glo

glo._init()


class Menu(QtWidgets.QWidget, menu.Ui_Form):
    # 自定义RVC相机
    rcv = myrvc(exposure_time_2d=20, exposure_time_3d=30)
    glo.set_value("rcv", rcv)


    # 自定义信号
    show_ballot_box_manage_signal = QtCore.pyqtSignal()
    show_template_manage_signal = QtCore.pyqtSignal()
    show_item_manage_signal = QtCore.pyqtSignal()
    show_parameter_setting_signal = QtCore.pyqtSignal()
    show_manually_review_signal = QtCore.pyqtSignal()
    show_vote_data_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        # 定义了 __init__() 构造函数，其中调用了父类的构造函数 super(Menu, self).__init__(parent)，
        # 以及 setupUi() 方法，用于初始化菜单界面的 UI 界面。还设置了窗口标题和图标。
        super(Menu, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("首页菜单")
        self.setWindowIcon(QtGui.QIcon('printer.png'))

        # self.PushButton_ballot_box_manage.clicked.connect(self.ballot_box_manage)
        # self.PushButton_template_manage.clicked.connect(self.template_manage)
        # self.PushButton_item_manage.clicked.connect(self.item_manage)
        # self.PushButton_parameter_setting.clicked.connect(self.parameter_setting)
        # self.PushButton_manually_review.clicked.connect(self.manually_review)
        # self.PushButton_vote_data.clicked.connect(self.vote_data)

        self.init()

    def stop(self):
        print("guanbixiance")

    def init(self):
        config = configparser.ConfigParser()
        file = config.read(SETTING_PATH)
        config_dict = config.defaults()

        background_path = config_dict["background"]
        self.gridFrame.setStyleSheet("#gridFrame{border-image: url(" + background_path + ");}")

    def ballot_box_manage(self):
        print('进入票箱管理')
        self.show_ballot_box_manage_signal.emit()

    def template_manage(self):
        print('进入模板管理')
        self.show_template_manage_signal.emit()

    def item_manage(self):
        print('进入候选人管理')
        self.show_item_manage_signal.emit()

    def parameter_setting(self):
        print('进入参数设置')
        self.show_parameter_setting_signal.emit()

    def manually_review(self):
        print('进入人工审核')
        self.show_manually_review_signal.emit()

    def vote_data(self):
        print('进入选票数据')
        self.show_vote_data_signal.emit()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


# def return_project_manage():
#     try:
#         Ui_ballot_box_manage.controlThread.stop()
#     except Exception:
#         print(traceback.print_exc())
#
#     try:
#         Ui_ballot_box_manage.reThread.stop()
#     except Exception:
#         print(traceback.print_exc())
#
#     try:
#         Ui_vote_data.reThread.stop()
#     except Exception:
#         print(traceback.print_exc())
#
#     try:
#         Ui_manually_review.reThread.stop()
#     except Exception:
#         print(traceback.print_exc())
#     # 项目管理界面数据清空
#     Ui_item_manage.clear_info_in_UI()
#
#     # 模板管理界面数据清空
#     Ui_template_manage.clear_info_in_UI()
#
#     # 选票数据界面数据清空
#     Ui_vote_data.clear_info_in_UI()
#
#     #票箱管理数据清空
#     Ui_ballot_box_manage.tableWidget_ballot_box_manage.setRowCount(0)
#
#     # 人工审核界面数据清空
#     Ui_manually_review.clear_info_in_UI()
#
#     # 选票参数界面数据清空
#     Ui_parameter_setting.clear_info_in_UI()
#
#     global candidates
#     global classesOfCandidate
#     global classes
#     global project_path
#     global project_name
#     global current_mode
#     global result
#     global data
#     global useless_vote
#     global binary_th
#     global sobel
#     global area_th0
#     global area_th1
#     global LXTR_th0
#     global LXTR_th1
#     global num_item
#     global type_symbol
#     global flag_recognition
#     global license_flag
#     global ID
#     global creator
#     global now_time
#     global vote
#     global databaseName
#
#     candidates = []
#     classesOfCandidate = []
#     classes = []
#     project_path = []
#     project_name = []
#     current_mode = ""
#     result = []
#     data = []
#     mode2election = {}
#     useless_vote = []
#     binary_th = 120
#     sobel = 3
#     area_th0 = 500
#     area_th1 = 2500
#     LXTR_th0 = 8000
#     LXTR_th1 = 30000
#     num_item = 6
#     type_symbol = 1
#     flag_recognition = False
#     license_flag = False
#     ID = None
#     creator = None
#     now_time = None
#     vote = []
#     databaseName = []
#
#     # 清空Auditing/static/Config_Ballot
#     for root, dirs, files in os.walk(r"Auditing\static\Config_Ballot", topdown=False):
#         for file in files:
#             os.remove(os.path.join(root, file))
#
#     # min.close()
#     mainWin.close()
#     print("返回工程管理")
#     Ui_project_manage.center()
#     Ui_project_manage.show()

class LicenseDialog(QtWidgets.QDialog, license_dialog.Ui_Dialog):
    def __init__(self, parent=None):
        super(LicenseDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("序列号验证界面")
        # self.setWindowIcon(QtGui.QIcon('printer.png'))

        self.pushButton_cancel.clicked.connect(self.cancel)
        self.pushButton_OK.clicked.connect(self.OK)

        mac = auth.get_mac_address()
        self.lineEdit_mac.setText(mac)

    def OK(self):
        serial = self.lineEdit_number.text()
        print("序列号为", serial)

        # 判断输入格式是否正确
        if serial == "":
            QtWidgets.QMessageBox.information(self, "提示", "请输入序列号！")
            return
        elif not (len(serial) == 19 and len(serial.replace("-", "")) == 16):
            QtWidgets.QMessageBox.information(self, "提示", "序列号格式错误！")
            return

        insert_result, insert_str = auth.insert_datatable(serial)
        if insert_result:
            pass
        elif not insert_result:
            QtWidgets.QMessageBox.information(self, "提示", insert_str)

        authorize_result, error_code = auth.Authorize()

        if authorize_result and error_code == 0:
            self.accept()
        elif not authorize_result and error_code == 1:
            QtWidgets.QMessageBox.information(self, "提示", "数据库表为空")
            sys.exit(app.exec_())
        elif not authorize_result and error_code == 2:
            QtWidgets.QMessageBox.information(self, "提示", "MAC地址不一致")
            sys.exit(app.exec_())
        elif not authorize_result and error_code == 3:
            QtWidgets.QMessageBox.information(self, "提示", "序列号已过期")
            sys.exit(app.exec_())

    def cancel(self):
        print("cancel")
        sys.exit(app.exec_())

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class Min(QtWidgets.QMainWindow, bottom_layer.Ui_MainWindow):
    def __init__(self, CommunicationSettingSubUI,
                 FunctionTestSubUI,
                 OperationMonitoringSubUI,
                 SettingSubUI,
                 WeldingGunLibrarySubUI, parent=None):
        super(Min, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("智能焊接系统")
        # self.setWindowIcon(QtGui.QIcon('printer.png'))

        # 始终置于最顶层
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # 设置堆叠布局
        self.qsl = QtWidgets.QStackedLayout(self.frame)

        self.qsl.addWidget(FunctionTestSubUI)
        self.qsl.addWidget(OperationMonitoringSubUI)
        self.qsl.addWidget(WeldingGunLibrarySubUI)
        self.qsl.addWidget(SettingSubUI)
        self.qsl.addWidget(CommunicationSettingSubUI)

        # self.pushButton_project_manage.clicked.connect(return_project_manage)
        # self.pushButton_mainwindow.clicked.connect(return_mainWindow)
        self.pushButton_test_manage_subUI.clicked.connect(self.show_panel)
        self.pushButton_run_manage_subUI.clicked.connect(self.show_panel)
        self.pushButton_package_setting_subUI.clicked.connect(self.show_panel)
        self.pushButton_parameter_setting_subUI.clicked.connect(self.show_panel)
        self.pushButton_tele_setting_subUI.clicked.connect(self.show_panel)

        self.comboBox_coordinate.currentTextChanged.connect(self.setCoordinate)
        self.comboBox_speed.currentTextChanged.connect(self.setSpeed)
        self.comboBox_servo_sta.currentTextChanged.connect(self.setServoState)
        self.comboBox_cur_mode.currentTextChanged.connect(self.setCurMode)

        self.pushButton_deadman_on.clicked.connect(self.deadman_on_button)
        # 点击 “下电”按钮后
        self.pushButton_deadman_down.clicked.connect(self.deadman_down_button)
        self.pushButton_connect_robot.clicked.connect(self.conncet_bot)

        # buttons are released
        self.pushButton_x0.clicked.connect(self.x_minus_released)
        self.pushButton_y0.clicked.connect(self.y_minus_released)
        self.pushButton_z0.clicked.connect(self.z_minus_released)
        self.pushButton_a0.clicked.connect(self.a_minus_released)
        self.pushButton_b0.clicked.connect(self.b_minus_released)
        self.pushButton_c0.clicked.connect(self.c_minus_released)

        self.pushButton_x1.clicked.connect(self.x_plus_released)
        self.pushButton_y1.clicked.connect(self.y_plus_released)
        self.pushButton_z1.clicked.connect(self.z_plus_released)
        self.pushButton_a1.clicked.connect(self.a_plus_released)
        self.pushButton_b1.clicked.connect(self.b_plus_released)
        self.pushButton_c1.clicked.connect(self.c_plus_released)

        # buttons are pressed
        self.pushButton_x0.pressed.connect(self.x_minus_pressed)
        self.pushButton_y0.pressed.connect(self.y_minus_pressed)
        self.pushButton_z0.pressed.connect(self.z_minus_pressed)
        self.pushButton_a0.pressed.connect(self.a_minus_pressed)
        self.pushButton_b0.pressed.connect(self.b_minus_pressed)
        self.pushButton_c0.pressed.connect(self.c_minus_pressed)

        self.pushButton_x1.pressed.connect(self.x_plus_pressed)
        self.pushButton_y1.pressed.connect(self.y_plus_pressed)
        self.pushButton_z1.pressed.connect(self.z_plus_pressed)
        self.pushButton_a1.pressed.connect(self.a_plus_pressed)
        self.pushButton_b1.pressed.connect(self.b_plus_pressed)
        self.pushButton_c1.pressed.connect(self.c_plus_pressed)

        # initial global var
        self.init()

    def run(self):
        self.project_path = glo.get_value("project_path")
        positions_list = manage_position.load_positions(self.project_path)

        # check camera
        try:
            res = self.camera.camera_is_connect()
        except AttributeError:
            QtWidgets.QMessageBox.information(self, "提示", "没有连接相机")
            return
        if res != 0:
            QtWidgets.QMessageBox.information(self, "提示", res)

        # check robot
        if not self.control_class.user_see_is_conncet():
            QtWidgets.QMessageBox.information(self, "提示", "机械臂未连接")
            return

        self.control_class.user_set_refresh(1, 1)
        time.sleep(1)

        self.control_class.user_set_socket_ctrl(1)
        time.sleep(0.2)
        self.control_class.user_set_speed(100)
        ################################
        if self.control_class.user_socket_movj(pos=positions_list[2][2:], vel=10) != 0:
            return
        else:
            time.sleep(0.5)
        # wait
        while True:
            if self.control_class.user_get_bot_state("bot_programrun_status") != 2:
                break
            else:
                print("wait for stop")
                time.sleep(1)

        # get origin point
        origin_point = self.control_class.user_get_bot_state("bot_xyz_point")[1:]
        print(origin_point)

        for i in range(len(positions_list) - 1):
            print("position " + str(i))
            print(positions_list[i])

            # move
            # speed = self.comboBox_speed.currentText()
            if self.control_class.user_socket_movj(pos=positions_list[i][2:], vel=10) != 0:
                return
            else:
                time.sleep(0.5)
            # wait
            while True:
                if self.control_class.user_get_bot_state("bot_programrun_status") != 2:
                    break
                else:
                    print("wait for stop")
                    time.sleep(1)

            # capture
            try:
                self.camera.capture(self.project_path)
            except:
                # todo
                return

            capture_point = self.control_class.user_get_bot_state("bot_xyz_point")[1:]
            cur_point = [x / 1000 for x in capture_point[0:3]] + capture_point[3:]
            print(cur_point)

            # progress
            new_dian1, new_dian2, a, b, c = rascn.hanfengtiqu(cur_point,
                                                              os.path.join(self.project_path, "save_point.ply"))
            new_dian1 *= 1000
            new_dian2 *= 1000
            new_dian1 = list(new_dian1) + cur_point[3:]
            new_dian2 = list(new_dian2) + cur_point[3:]
            print("progress result：{}，{}，{}，{}，{}".format(new_dian1, new_dian2, a, b, c))
            if (i == 1):
                new_dian1[0] -= 10
                new_dian1[1] -= 10
                new_dian2[0] -= 10
                new_dian2[1] -= 10

            # weld start -------------------------------
            if self.control_class.user_socket_movj(pos=new_dian1, vel=10) != 0:
                return
            else:
                time.sleep(0.5)
            # wait
            while True:
                if self.control_class.user_get_bot_state("bot_programrun_status") == 0:
                    break
                else:
                    print("wait for stop")
                    time.sleep(1)

            if self.control_class.user_socket_movl(pos=new_dian2, vel=30) != 0:
                return
            else:
                time.sleep(0.5)
            # wait
            while True:
                if self.control_class.user_get_bot_state("bot_programrun_status") == 0:
                    break
                else:
                    print("wait for stop")
                    time.sleep(1)

            if self.control_class.user_socket_movj(pos=capture_point, vel=10) != 0:
                return
            else:
                time.sleep(0.5)
            # wait
            while True:
                if self.control_class.user_get_bot_state("bot_programrun_status") == 0:
                    break
                else:
                    print("wait for stop")
                    time.sleep(1)

            if self.control_class.user_socket_movj(pos=origin_point, vel=10) != 0:
                return
            else:
                time.sleep(0.5)
            # wait
            while True:
                if self.control_class.user_get_bot_state("bot_programrun_status") == 0:
                    break
                else:
                    print("wait for stop")
                    time.sleep(1)
            # weld end ----------------------------------

        self.control_class.user_set_speed(10)
        self.control_class.user_set_socket_ctrl(0)

    def x_minus_released(self):
        print("x_minus_released")
        print('stop axis 1,dir=-1')
        self.control_class.user_start_moving_jog(1, -1, 0)

    def x_minus_pressed(self):
        print("x_minus_pressed")
        print('start axis 1,dir=-1')
        self.control_class.user_start_moving_jog(1, -1, 1)

    def x_plus_released(self):
        # print("x_plus_released")
        # print('stop axis 1,dir=1')
        print(glo.get_value("position"))
        # self.control_class.user_start_moving_jog(1, 1, 0)

    def x_plus_pressed(self):
        print("x_plus_pressed")
        print('start axis 1,dir=1')
        self.control_class.user_start_moving_jog(1, 1, 1)

    def y_minus_released(self):
        print("y_minus_released")
        print('stop axis 2,dir=-1')
        self.control_class.user_start_moving_jog(2, -1, 0)

    def y_minus_pressed(self):
        print("y_minus_pressed")
        print('start axis 2,dir=-1')
        self.control_class.user_start_moving_jog(2, -1, 1)

    def y_plus_released(self):
        print("y_plus_released")
        print('stop axis 2,dir=1')
        self.control_class.user_start_moving_jog(2, 1, 0)

    def y_plus_pressed(self):
        print("y_plus_pressed")
        print('start axis 2,dir=1')
        self.control_class.user_start_moving_jog(2, 1, 1)

    def z_minus_released(self):
        print("z_minus_released")
        print('stop axis 3,dir=-1')
        self.control_class.user_start_moving_jog(3, -1, 0)

    def z_minus_pressed(self):
        print("z_minus_pressed")
        print('start axis 3,dir=-1')
        self.control_class.user_start_moving_jog(3, -1, 1)

    def z_plus_released(self):
        print("z_plus_released")
        print('stop axis 3,dir=1')
        self.control_class.user_start_moving_jog(3, 1, 0)

    def z_plus_pressed(self):
        print("z_plus_pressed")
        print('start axis 3,dir=1')
        self.control_class.user_start_moving_jog(3, 1, 1)

    def a_minus_released(self):
        print("a_minus_released")
        print('stop axis 4,dir=-1')
        self.control_class.user_start_moving_jog(4, -1, 0)

    def a_minus_pressed(self):
        print("a_minus_pressed")
        print('start axis 4,dir=-1')
        self.control_class.user_start_moving_jog(4, -1, 1)

    def a_plus_released(self):
        print("a_plus_released")
        print('stop axis 4,dir=1')
        self.control_class.user_start_moving_jog(4, 1, 0)

    def a_plus_pressed(self):
        print("a_plus_pressed")
        print('start axis 4,dir=1')
        self.control_class.user_start_moving_jog(4, 1, 1)

    def b_minus_released(self):
        print("b_minus_released")
        print('stop axis 5,dir=-1')
        self.control_class.user_start_moving_jog(5, -1, 0)

    def b_minus_pressed(self):
        print("b_minus_pressed")
        print('start axis 5,dir=-1')
        self.control_class.user_start_moving_jog(5, -1, 1)

    def b_plus_released(self):
        print("b_plus_released")
        print('stop axis 5,dir=1')
        self.control_class.user_start_moving_jog(5, 1, 0)

    def b_plus_pressed(self):
        print("b_plus_pressed")
        print('start axis 5,dir=1')
        self.control_class.user_start_moving_jog(5, 1, 1)

    def c_minus_released(self):
        print("c_minus_released")
        print('stop axis 6,dir=-1')
        self.control_class.user_start_moving_jog(6, -1, 0)

    def c_minus_pressed(self):
        print("c_minus_pressed")
        print('start axis 6,dir=-1')
        self.control_class.user_start_moving_jog(6, -1, 1)

    def c_plus_released(self):
        print("c_plus_released")
        print('stop axis 6,dir=1')
        self.control_class.user_start_moving_jog(6, 1, 0)

    def c_plus_pressed(self):
        print("c_plus_pressed")
        print('start axis 6,dir=1')
        self.control_class.user_start_moving_jog(6, 1, 1)

    def init(self):
        """
            init after enter project
        """
        # 实例化机器人控制对象
        self.control_class = ctrl_inexbot.control_thread_class()
        self.is_connect = self.control_class.user_see_is_conncet()

        self.setCoordinate()
        self.setServoState()
        self.setSpeed()
        self.setCurMode()

        self.th = self.RefreshConnectStateThread()
        self.th.update_data.connect(self.refresh_connet_state)
        self.th.start()

    def conncet_bot(self):
        # 点击 连接机械臂 按钮后的触发的函数
        """
            connect_robot
        """
        # 1.创建socket
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 2. 链接服务器
        server_addr = ("192.168.0.1", 5233)
        tcp_socket.connect(server_addr)
        # 此处会默认发来一个 connect successful
        data = tcp_socket.recv(1024)
        print("message in main.py: \n" + data.decode("gbk"))
        # 设置全局变量
        glo.set_value("tcp_socket", tcp_socket)
        self.label_robot_state.setText("连接")
        # 3. 发送数据
        # send_data = input("请输入要发送的数据：")
        # tcp_socket.send(send_data.encode("gbk"))

        # 4. 关闭套接字
        # tcp_socket.close()
        # 下面三行是原作者的东西
        # self.control_class.conncet()
        # time.sleep(0.5)
        # self.control_class.user_set_tool(1)

    class RefreshConnectStateThread(MyQThread.MyQThread):
        """
        Refresh every 5 seconds
        """
        sleep_time = 5
        thread_name = "RefreshConnectStateThread"

    def refresh_connet_state(self):
        # 这里是设置按钮的位置 机械臂连接状态断开/链接
        # 初始化的时候被设置为断开
        # 原作者是在实时监测是否连接上，我们不检测
        # 这个代码会在点击链接之后 一直循环检测是否连接上
        # print("refresh_connet_state")
        pass
        # if self.control_class.user_see_is_conncet():
        #     self.label_robot_state.setText("连接")
        # else:
        #     self.label_robot_state.setText("断开")

    # 点击 “下电”按钮后触发的函数
    def deadman_down_button(self):
        tcp_socket = glo.get_value("tcp_socket")
        tcp_socket.send("STOP".encode("gbk"))

        print("已发送 STOP 指令")
        # 下面是原作者的内容
        # self.control_class.user_set_deadman_status(0)
        # self.control_class.user_ctrl_tech_keepmoving_class(0)

    def deadman_on_button(self):
        coordinate = glo.get_value("coordinate")
        if coordinate != None:
            if self.control_class.user_set_coord_mode(coordinate) == 0:
                print("关节坐标系设置正常")
            time.sleep(0.2)
        else:
            return

        if glo.get_value("mode") != None:
            if self.control_class.user_set_operate_mode(0) == 0:
                print("模式设置正常")
            time.sleep(0.2)
        else:
            return

        # todo
        if glo.get_value("servo_state") == 1:
            if self.control_class.user_set_servo_status(1) == 0:
                self.comboBox_servo_sta.setCurrentText("伺服运行")
                print("伺服就绪")
            time.sleep(0.2)
        else:
            QtWidgets.QMessageBox.information(self, "提示", "伺服未就绪")
            return

        if self.control_class.user_set_deadman_status(1) == 0:
            print("上电成功")
        time.sleep(0.2)

        if glo.get_value("speed") != None:
            if self.control_class.user_set_speed(10) == 0:
                print("速度{}设置成功".format("10"))
            time.sleep(0.2)
        else:
            return

        self.control_class.user_ctrl_tech_keepmoving_class(1)

    def setCurMode(self):
        temp = self.comboBox_cur_mode.currentText()
        print("mode：", temp)

        # 0：示教模式
        # 1：远程模式
        # 2：运行模式
        if temp == "示教模式":
            self.control_class.user_set_operate_mode(0)
            glo.set_value("mode", 0)
        elif temp == "远程模式":
            self.control_class.user_set_operate_mode(1)
            glo.set_value("mode", 1)
        elif temp == "运行模式":
            self.control_class.user_set_operate_mode(2)
            glo.set_value("mode", 2)
        time.sleep(0.2)

    def setSpeed(self):
        temp = self.comboBox_speed.currentText()
        print("speed：", temp)

        if temp[-1] == '%':
            self.control_class.user_set_speed(int(temp.split("%")[0]))
            glo.set_value("speed", int(temp.split("%")[0]))
        elif temp == "0.1°":
            self.control_class.user_set_speed(101)
            glo.set_value("speed", 101)
        elif temp == "0.01°":
            self.control_class.user_set_speed(102)
            glo.set_value("speed", 102)
        time.sleep(0.2)

    def setServoState(self):
        temp = self.comboBox_servo_sta.currentText()
        print("servo：", temp)

        if temp == "伺服停止":
            self.control_class.user_set_servo_status(0)
            glo.set_value("servo_state", 0)
        elif temp == "伺服就绪":
            self.control_class.user_set_servo_status(1)
            glo.set_value("servo_state", 1)
        time.sleep(0.2)

    def setCoordinate(self):
        test = self.comboBox_coordinate.currentText()
        print("当前坐标系：", test)

        # 0：关节坐标
        # 1：直角坐标
        # 2：工具坐标
        # 3：用户坐标
        if test == "关节坐标":
            self.control_class.user_set_coord_mode(0)
            glo.set_value("coordinate", 0)
        elif test == "直角坐标":
            self.control_class.user_set_coord_mode(1)
            glo.set_value("coordinate", 1)
        elif test == "工具坐标":
            self.control_class.user_set_coord_mode(2)
            glo.set_value("coordinate", 2)
        elif test == "用户坐标":
            self.control_class.user_set_coord_mode(3)
            glo.set_value("coordinate", 3)
        time.sleep(0.2)

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, '提示', "请确认是否关闭软件？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        #     这里的关闭软件 可以加上关闭套接字的操作
        else:
            event.ignore()

    def show_panel(self):

        # self.pushButton_test_manage_subUI.clicked.connect(self.show_panel)
        # self.pushButton_run_manage_subUI.clicked.connect(self.show_panel)
        # self.pushButton_package_setting_subUI.clicked.connect(self.show_panel)

        dic = {
            "pushButton_test_manage_subUI": 0,
            "pushButton_run_manage_subUI": 1,
            "pushButton_package_setting_subUI": 2,
            "pushButton_parameter_setting_subUI": 3,
            "pushButton_tele_setting_subUI": 4
        }
        index = dic[self.sender().objectName()]
        self.qsl.setCurrentIndex(index)

        # if index == 0:
        #     functiontestsubui.init()
        # elif index == 1:
        #     operationmonitoringsubui.init()
        # elif index == 2:
        #     weldinggunlibrarysubui.init()
        # elif index == 3:
        #     settingsubui.init()
        # elif index == 4:
        #     communicationsettingsubui.init()

        # if index == 0:
        #     self.pushButton_ballot_box.setStyleSheet(
        #         "QPushButton{background-color: rgb(170, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(170, 255, 255);}\n"
        #         )
        #     self.pushButton_item_manage.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
        #     self.pushButton_manually_review.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
        #     self.pushButton_parameter_manage.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
        #     self.pushButton_template_manage.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
        #     self.pushButton_vote_data.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
        #
        # elif index == 1:
        #     self.pushButton_item_manage.setStyleSheet(
        #         "QPushButton{background-color: rgb(170, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(170, 255, 255);}\n"
        #         )
        #     self.pushButton_ballot_box.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
        #     self.pushButton_manually_review.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
        #     self.pushButton_parameter_manage.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
        #     self.pushButton_template_manage.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
        #     self.pushButton_vote_data.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
        #
        # elif index == 2:
        #     self.pushButton_manually_review.setStyleSheet(
        #         "QPushButton{background-color: rgb(170, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(170, 255, 255);}\n"
        #         )
        #     self.pushButton_item_manage.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
        #     self.pushButton_ballot_box.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
        #     self.pushButton_parameter_manage.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
        #     self.pushButton_template_manage.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
        #     self.pushButton_vote_data.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
        #
        #     Ui_manually_review.comboBox_choose_template.setCurrentText(mode2election[current_mode.split('\\')[-1]])
        #     Ui_manually_review.choose_template()
        #
        # elif index == 3:
        #     self.pushButton_parameter_manage.setStyleSheet(
        #         "QPushButton{background-color: rgb(170, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(170, 255, 255);}\n"
        #         )
        #     self.pushButton_item_manage.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
        #     self.pushButton_manually_review.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
        #     self.pushButton_ballot_box.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
        #     self.pushButton_template_manage.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
        #     self.pushButton_vote_data.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
        #
        #     Ui_parameter_setting.comboBox_choose_template.setCurrentText(mode2election[current_mode.split('\\')[-1]])
        #     Ui_parameter_setting.choose_template()
        #
        # elif index == 4:
        #     self.pushButton_template_manage.setStyleSheet(
        #         "QPushButton{background-color: rgb(170, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(170, 255, 255);}\n"
        #         )
        #     self.pushButton_item_manage.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
        #     self.pushButton_manually_review.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
        #     self.pushButton_parameter_manage.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
        #     self.pushButton_ballot_box.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
        #     self.pushButton_vote_data.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
        #
        #     # try:
        #     Ui_template_manage.comboBox_choose_template.setCurrentText(mode2election[current_mode.split('\\')[-1]])
        #     Ui_template_manage.choose_template()
        #     Ui_template_manage.label_show_vote.clear_data()
        #     if Ui_template_manage.pixmap != []:
        #         Ui_template_manage.label_show_vote.load_xml_and_set_data(os.path.join(current_mode, 'location.xml'),
        #                                                                  Ui_template_manage.pixmap.width(),
        #                                                                  Ui_template_manage.pixmap.height())
        #
        #     Ui_template_manage.lineEdit_affirmative.setText(AFFIRMATIVE)
        #     Ui_template_manage.lineEdit_oppose.setText(OPPOSE)
        #     Ui_template_manage.lineEdit_abstention.setText(ABSTENTION)
        #     # except:
        #     #     pass
        #
        # elif index == 5:
        #     self.pushButton_vote_data.setStyleSheet(
        #         "QPushButton{background-color: rgb(170, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(170, 255, 255);}\n"
        #         )
        #     self.pushButton_item_manage.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
        #     self.pushButton_manually_review.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
        #     self.pushButton_parameter_manage.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
        #     self.pushButton_template_manage.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
        #     self.pushButton_ballot_box.setStyleSheet(
        #         "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
        #         "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


# 控制台输出记录到文件
class Logger(object):
    def __init__(self, file_name="Default.log", stream=sys.stdout):
        self.terminal = stream
        self.log = open(file_name, "a")  # 追加写，只写，不存在则创建

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


def show_mainWindow():
    Ui_project_manage.close()
    print("关闭工程管理页面，进入主页面")
    mainWin.center()
    mainWin.show()


# def show_current_UI(index):
#     if index == 0:
#         min.pushButton_ballot_box.setStyleSheet(
#             "QPushButton{background-color: rgb(170, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(170, 255, 255);}\n"
#         )
#         min.pushButton_item_manage.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
#         min.pushButton_manually_review.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
#         min.pushButton_parameter_manage.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
#         min.pushButton_template_manage.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
#         min.pushButton_vote_data.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
#
#     elif index == 1:
#         min.pushButton_item_manage.setStyleSheet(
#             "QPushButton{background-color: rgb(170, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(170, 255, 255);}\n"
#         )
#         min.pushButton_ballot_box.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
#         min.pushButton_manually_review.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
#         min.pushButton_parameter_manage.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
#         min.pushButton_template_manage.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
#         min.pushButton_vote_data.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
#
#     elif index == 2:
#         min.pushButton_manually_review.setStyleSheet(
#             "QPushButton{background-color: rgb(170, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(170, 255, 255);}\n"
#         )
#         min.pushButton_item_manage.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
#         min.pushButton_ballot_box.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
#         min.pushButton_parameter_manage.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
#         min.pushButton_template_manage.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
#         min.pushButton_vote_data.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
#
#     elif index == 3:
#         min.pushButton_parameter_manage.setStyleSheet(
#             "QPushButton{background-color: rgb(170, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(170, 255, 255);}\n"
#         )
#         min.pushButton_item_manage.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
#         min.pushButton_manually_review.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
#         min.pushButton_ballot_box.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
#         min.pushButton_template_manage.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
#         min.pushButton_vote_data.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
#
#     elif index == 4:
#         min.pushButton_template_manage.setStyleSheet(
#             "QPushButton{background-color: rgb(170, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(170, 255, 255);}\n"
#         )
#         min.pushButton_item_manage.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
#         min.pushButton_manually_review.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
#         min.pushButton_parameter_manage.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
#         min.pushButton_ballot_box.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
#         min.pushButton_vote_data.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
#
#     elif index == 5:
#         min.pushButton_vote_data.setStyleSheet(
#             "QPushButton{background-color: rgb(170, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(170, 255, 255);}\n"
#         )
#         min.pushButton_item_manage.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
#         min.pushButton_manually_review.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
#         min.pushButton_parameter_manage.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
#         min.pushButton_template_manage.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")
#         min.pushButton_ballot_box.setStyleSheet(
#             "QPushButton{background-color: rgb(255, 255, 255);border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 255, 255);}\n"
#             "QPushButton:hover{border-width: 4px;border-style: solid;border-bottom-color: rgb(255, 0, 0);}")

def show_functiontest_subUI():
    mainWin.close()
    print('已经进入功能测试界面')
    min.qsl.setCurrentIndex(0)
    # show_current_UI(0)
    min.center()
    min.show()


def show_operation_monitoring_subUI():
    mainWin.close()
    print('已经进入运行检测界面')
    min.qsl.setCurrentIndex(1)
    # show_current_UI(1)
    min.center()
    min.show()


def show_weldinggun_library_subUI():
    mainWin.close()
    print('已经进入焊接包界面')
    min.qsl.setCurrentIndex(2)
    # show_current_UI(2)
    min.center()
    min.show()


def show_setting_subUI():
    mainWin.close()
    print('已经进入参数设置界面')
    min.qsl.setCurrentIndex(3)
    # show_current_UI(3)
    min.center()
    min.show()


def show_communicationsetting_subUI():
    mainWin.close()
    print('已经进入通信设置界面')
    min.qsl.setCurrentIndex(4)
    # show_current_UI(3)
    min.center()
    min.show()


# 重写QSplashScreen类
class MySplashScreen(QSplashScreen):
    # 鼠标点击事件
    def mousePressEvent(self, event):
        pass


if __name__ == '__main__':
    tim = time.time()
    # app = QtWidgets.QApplication(sys.argv) -- 源码
    app = QApplication([])

    # 开机动画
    # 设置启动界面
    # 注释：重写了QSplashScreen类,该类是为了展示开机进度条
    splash = MySplashScreen()
    #     def mousePressEvent(self, event):
    #         pass

    # 初始图片
    # splash.setPixmap(QPixmap(r'C:\Users\87058\Desktop\dog_detected.jpg'))  # 设置背景图片
    # 初始文本
    splash.showMessage("加载... 0%", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
    # 设置字体
    splash.setFont(QtGui.QFont('微软雅黑', 10))
    # 显示启动界面
    splash.show()
    app.processEvents()  # 处理主进程事件 - 貌似也是QSplashScreen里自带的一套写作流程

    # 自定义目录存放日志文件
    log_path = '../Logs/'
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    # 日志文件名按照程序运行时间设置
    log_file_name = log_path + 'log-' + time.strftime("%Y%m%d-%H%M%S", time.localtime()) + '.log'
    # 记录正常的 print 信息
    sys.stdout = Logger(log_file_name)
    # 记录 traceback 异常信息
    sys.stderr = Logger(log_file_name)

    splash.showMessage("加载... {0}%".format(1 * 10), QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
    app.processEvents()  # 处理主进程事件

    #     # license_flag = False
    #     # flag = False
    #
    #     # from src import auth
    #     #
    #     # license_flag, error_num = auth.Authorize()
    #     # license = LicenseDialog()
    #     # """
    #     # :return: Boolean值，通过核验则为True，反之则为False
    #     # # 当状态为True，错误码都为0
    #     # # 当状态为False，错误码中1代表数据表为空，2代表MAC地址不一致，3代表试用序列号已过期
    #     # """
    #     # if license_flag and error_num == 0:
    #     #     flag = True
    #     # elif not license_flag:
    #     #     if error_num == 1:
    #     #         license.center()
    #     #         license.show()
    #     #     elif error_num == 2:
    #     #         license.center()
    #     #         license.show()
    #     #         QtWidgets.QMessageBox.information(license, "提示", "MAC地址不一致。")
    #     #         # 清空auth表
    #     #         auth.re_Authorize()
    #     #     elif error_num == 3:
    #     #         license.center()
    #     #         license.show()
    #     #         QtWidgets.QMessageBox.information(license, "提示", "序列号已过期。")
    #
    #     # if flag or license.exec_() == QtWidgets.QDialog.Accepted:
    if True:
        # system进行初始化
        import src.InitResource

        # 生成了四部分ini配置文件，分别存储了如 用户，公司信息等
        init = src.InitResource.InitResource()

        # 实例化子页面
        mainWin = Menu()
        # 在src/ui/sub_ui文件下
        operationmonitoringsubui = OperationMonitoringSubUI()
        functiontestsubui = FunctionTestSubUI()
        weldinggunlibrarysubui = WeldingGunLibrarySubUI()
        settingsubui = SettingSubUI()
        communicationsettingsubui = CommunicationSettingSubUI()
        Ui_project_manage = projectManage(communicationsettingsubui,
                                          functiontestsubui,
                                          operationmonitoringsubui,
                                          settingsubui,
                                          weldinggunlibrarysubui)

        min = Min(communicationsettingsubui,
                  functiontestsubui,
                  operationmonitoringsubui,
                  settingsubui,
                  weldinggunlibrarysubui)

        # 组合
        functiontestsubui.min = min
        communicationsettingsubui.min = min
        operationmonitoringsubui.min = min

        dialog = LoginDialog()
        dialog.init()

        splash.showMessage("加载... {0}%".format(2 * 10), QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom,
                           QtCore.Qt.black)
        app.processEvents()  # 处理主进程事件

        # 连接子页面
        mainWin.pushButton_test_manage_subUI.clicked.connect(show_functiontest_subUI)
        mainWin.pushButton_run_manage_subUI.clicked.connect(show_operation_monitoring_subUI)
        mainWin.pushButton_package_setting_subUI.clicked.connect(show_weldinggun_library_subUI)
        mainWin.pushButton_parameter_setting_subUI.clicked.connect(show_setting_subUI)
        mainWin.pushButton_tele_setting_subUI.clicked.connect(show_communicationsetting_subUI)
        Ui_project_manage.show_mainWindow_signal.connect(show_mainWindow)

        splash.showMessage("加载... {0}%".format(10 * 10), QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom,
                           QtCore.Qt.black)
        app.processEvents()  # 处理主进程事件

        dialog.center()
        dialog.show()
        splash.finish(dialog)  # 隐藏启动界面
        splash.deleteLater()
        tim2 = time.time()
        print("载入系统耗时", tim2 - tim, "秒")

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            print('密码正确进入主页面')
            Ui_project_manage.center()
            Ui_project_manage.show()
            sys.exit(app.exec_())
