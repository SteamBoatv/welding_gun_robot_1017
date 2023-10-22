import random
import threading
import time
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QObject, pyqtSignal, QThread

from UI.sub_UI import FunctionTest

import src.global_var as glo
import src.manage_position as manage_position
from selfTools.littleTools import LittleTools

DE_BUG = 1
class FunctionTestSubUI(QtWidgets.QMainWindow, FunctionTest.Ui_MainWindow):
    def __init__(self, parent=None):
        super(FunctionTestSubUI, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("功能测试")

        self.label_time.setHidden(True)

        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 此代码是点击了 “添加位置” 之后，将当前位置添加到表格中
        self.pushButton_add_pos.clicked.connect(self.addPosition)

        # 点击 “删除位置” 之后 触发的函数
        self.pushButton_del_pos.clicked.connect(self.delPosition)
        self.pushButton_save.clicked.connect(self.savePosition)
        self.pushButton_start_get_points.clicked.connect(self.startGetPoints)
        self.pushButton_stop_get_points.clicked.connect(self.stopGetPoints)

    def startGetPoints(self):
        if not self.min.control_class.user_see_is_conncet():
            print("robot dose not connect")
        else:
            if self.min.comboBox_coordinate.currentText() == "关节坐标":
                self.min.control_class.user_set_refresh(0, 1)
                pass
            elif self.min.comboBox_coordinate.currentText() == "直角坐标":
                self.min.control_class.user_set_refresh(1, 1)
                pass
            elif self.min.comboBox_coordinate.currentText() == "工具坐标":
                pass
            elif self.min.comboBox_coordinate.currentText() == "用户坐标":
                pass

            self.min.refreshPointsThreadInstance.start()
            print("thread start")

    def stopGetPoints(self):
        if not self.min.control_class.user_see_is_conncet():
            print("robot dose not connect")
        else:
            self.min.control_class.user_set_refresh(1, 0)
            self.min.control_class.user_set_refresh(0, 0)
            # if self.min.comboBox_coordinate.currentText() == "关节坐标":
            #     self.min.control_class.user_set_refresh(0, 0)
            # elif self.min.comboBox_coordinate.currentText() == "直角坐标":
            #     self.min.control_class.user_set_refresh(1, 0)
            # elif self.min.comboBox_coordinate.currentText() == "工具坐标":
            #     pass
            # elif self.min.comboBox_coordinate.currentText() == "用户坐标":
            #     pass

            self.min.refreshPointsThreadInstance.stop()

    class refreshPointsThread(QThread):
        # 通过类成员对象定义信号
        update_data = pyqtSignal(str)
        flag = 1

        # 处理业务逻辑
        def run(self):
            self.flag=1
            while self.flag == 1:
                self.update_data.emit("1")
                time.sleep(1)

        def stop(self):
            self.flag = 0
            self.wait()
            print("停止刷新线程")

    def refresh_point(self):
        self.bot_point = self.min.control_class.user_get_bot_point()
        self.label_coor.setText("直角" if self.bot_point[0] == 1 else "关节")
        self.label_time.setText(str(self.bot_point[1]))
        self.label_x.setText(str(format(self.bot_point[2], '0.2f')))
        self.label_y.setText(str(format(self.bot_point[3], '0.2f')))
        self.label_z.setText(str(format(self.bot_point[4], '0.2f')))
        self.label_a.setText(str(format(self.bot_point[5], '0.2f')))
        self.label_b.setText(str(format(self.bot_point[6], '0.2f')))
        self.label_c.setText(str(format(self.bot_point[7], '0.2f')))

    def init(self):
        self.initPositionTable()

        # 实例化多线程对象
        self.min.refreshPointsThreadInstance = self.refreshPointsThread()
        self.min.refreshPointsThreadInstance.update_data.connect(self.refresh_point)
        pass

    def initPositionTable(self):
        project_path = glo.get_value("project_path")
        positions_list = manage_position.load_positions(project_path)
        for position in positions_list:
            self.insertPositionTable(position)
        pass

    def insertPositionTable(self, position):
        # 此函数用于将position插入到表格中
        # position是一个列表，包含了一个位置的所有信息
        # 0:坐标系 1:时间 2:x 3:y 4:z 5:a 6:b 7:c
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)

        item = QtWidgets.QTableWidgetItem(str(position[2]))
        self.tableWidget.setItem(row, 0, item)

        item = QtWidgets.QTableWidgetItem(str(position[3]))
        self.tableWidget.setItem(row, 1, item)

        item = QtWidgets.QTableWidgetItem(str(position[4]))
        self.tableWidget.setItem(row, 2, item)

        item = QtWidgets.QTableWidgetItem(str(position[5]))
        self.tableWidget.setItem(row, 3, item)

        item = QtWidgets.QTableWidgetItem(str(position[6]))
        self.tableWidget.setItem(row, 4, item)

        item = QtWidgets.QTableWidgetItem(str(position[7]))
        self.tableWidget.setItem(row, 5, item)

        item = QtWidgets.QTableWidgetItem("关节" if position[0] == 0 else "直角")
        self.tableWidget.setItem(row, 6, item)

    def addPosition(self):
        littleTools = LittleTools()
        # 调用此函数将当前位置添加到表格中
        # 此处获得了main函数中已经定义并且连接好的tcp_socket
        tcp_socket = glo.get_value("tcp_socket")

        position = []
        position.append(0 if self.label_coor.text() == "关节" else 1)
        position.append(self.label_time.text())
        # 这里是保存位置信息，还没有涉及到和QT界面的交流
        # label_x就是右下角的信息，这里要魔改成从机器人那里获取
        tcp_socket.send("getPos".encode("gbk"))
        time.sleep(random.randint(2, 3))
        # 接收到最新的代码
        data = tcp_socket.recv(1024)
        data = data.decode("gbk")
        numbers = littleTools.FANUCpositionToPython(data)
        print(numbers)
        #完美实现了
        # [-26.266, 12.243, -18.454, 76.067, -11.455, -86.993, 1273.161, -644.418, 630.992, -162.447, -68.101, -56.993]
        JPOS = numbers[0:6]
        XPOS = numbers[6:13]
        print(JPOS)
        print("------------")
        print(XPOS)
        position.append(XPOS[0])
        position.append(XPOS[1])
        position.append(XPOS[2])
        position.append(XPOS[3])
        position.append(XPOS[4])
        position.append(XPOS[5])
        # 下方是原作者的内容
        # position.append(self.label_x.text())
        # position.append(self.label_y.text())
        # position.append(self.label_z.text())
        # position.append(self.label_a.text())
        # position.append(self.label_b.text())
        # position.append(self.label_c.text())
        # print(self.tableWidget.rowCount()+1)
        # 设置全局变量”position“的值
        glo.get_value("position")[self.tableWidget.rowCount()+1] = position
        print(f"set Successfully in row: {(self.tableWidget.rowCount()+1)}")
        self.insertPositionTable(position)

    # 点击删除位置之后触发的函数
    def delPosition(self):
        row = self.tableWidget.currentRow()
        print(row)
        glo.get_value("position")[row+1] = None
        self.tableWidget.removeRow(row)
        pass

    def savePosition(self):
        positions = []
        for i in range(self.tableWidget.rowCount()):
            position = []
            position.append(0 if self.tableWidget.item(i, 6).text()=="关节" else 1)
            position.append(0)#时间
            position.append(float(self.tableWidget.item(i, 0).text()))
            position.append(float(self.tableWidget.item(i, 1).text()))
            position.append(float(self.tableWidget.item(i, 2).text()))
            position.append(float(self.tableWidget.item(i, 3).text()))
            position.append(float(self.tableWidget.item(i, 4).text()))
            position.append(float(self.tableWidget.item(i, 5).text()))
            positions.append(position)
        manage_position.save_positions(positions)
        pass

        QtWidgets.QMessageBox.information(self, "提示","保存成功")

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())