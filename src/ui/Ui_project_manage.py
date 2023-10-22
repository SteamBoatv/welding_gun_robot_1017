import configparser
import os
import traceback
import datetime

from UI import project_manage, project_manage_dialog

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import *

# from src.main import show_mainWindow
from src.project_manage import get_project_list
import src.global_var as glo

class projectManage(QtWidgets.QWidget, project_manage.Ui_Form):
    # 进入工程信号
    show_mainWindow_signal = QtCore.pyqtSignal()
    icon_path = "resource/printer.png"
    project_path = "project/"

    def __init__(self, CommunicationSettingSubUI,
                 FunctionTestSubUI,
                 OperationMonitoringSubUI,
                 SettingSubUI,
                 WeldingGunLibrarySubUI,parent=None):
        super(projectManage, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("工程管理")
        self.setWindowIcon(QtGui.QIcon(self.icon_path))

        self.CommunicationSettingSubUI = CommunicationSettingSubUI
        self.FunctionTestSubUI = FunctionTestSubUI
        self.OperationMonitoringSubUI = OperationMonitoringSubUI
        self.SettingSubUI = SettingSubUI
        self.WeldingGunLibrarySubUI = WeldingGunLibrarySubUI

        # 设置行数
        self.tableWidget_project_manage.setRowCount(0)
        # 全部表格可编辑
        # self.tableWidget_project_manage.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.tableWidget_project_manage.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        # 列宽自动分配
        self.tableWidget_project_manage.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # # 行高自动分配
        # self.tableWidget_project_manage.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # 优化：整行选中
        self.tableWidget_project_manage.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        # 链接信号与槽函数
        self.pushButton_add_project.clicked.connect(self.add_project)
        self.pushButton_delete_project.clicked.connect(self.delete_project)
        self.pushButton_enter_project.clicked.connect(self.enter_project)

        # 设置events_table的右键菜单
        self.tableWidget_project_manage.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # 在tableWidget中点击右键的触发事件
        self.tableWidget_project_manage.customContextMenuRequested[QtCore.QPoint].connect(self.context_menu_of_events_table)

        # 初始化工程表格
        self.init_tableWidget_project_manage()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 右键点击事件
    def context_menu_of_events_table(self, pos):

        pop_menu = QtWidgets.QMenu()
        add_new_project = pop_menu.addAction('新增工程')
        enter_project = pop_menu.addAction('进入工程')
        del_selected_project = pop_menu.addAction('删除工程')

        # 获取右键菜单中当前被点击的是哪一项
        action = pop_menu.exec_(self.tableWidget_project_manage.mapToGlobal(pos))

        # 如果选中的是添加新的工程
        if action == add_new_project:
            self.add_project()

        elif action == del_selected_project:
            self.delete_project()

        elif action == enter_project:
            self.enter_project()

    # 初始化工程表格
    def init_tableWidget_project_manage(self):

        project_list = get_project_list(self.project_path)
        # 倒序遍历
        for i in range(len(project_list)-1, -1, -1):
            # 新增一行
            self.tableWidget_project_manage.insertRow(0)

            # 填写日期时间
            newItem = QtWidgets.QTableWidgetItem("now_time")
            newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget_project_manage.setItem(0, 2, newItem)

            # 填写用户名
            newItem = QtWidgets.QTableWidgetItem("name")
            newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget_project_manage.setItem(0, 1, newItem)

            # 填写工程名
            newItem = QtWidgets.QTableWidgetItem(project_list[i])
            newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget_project_manage.setItem(0, 0, newItem)

    def delete_project(self):
        selected_items = self.tableWidget_project_manage.selectedItems()
        if len(selected_items) == 0:  # 说明没有选中任何行
            QtWidgets.QMessageBox.critical(self, "错误", "请单击选择需要删除的工程")
            return

        messageBox1 = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "提示", "将会删除有关该工程的所有信息，包括历史投票记录数据。")
        messageBox1.setWindowIcon(QtGui.QIcon(self.icon_path))
        messageBox1.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        buttonY1 = messageBox1.button(QtWidgets.QMessageBox.Yes)
        buttonY1.setText('确认')
        buttonN1 = messageBox1.button(QtWidgets.QMessageBox.No)
        buttonN1.setText('取消')
        messageBox1.exec_()

        if messageBox1.clickedButton() == buttonY1:
            messageBox2 = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "请确认", "是否确认删除该工程？")
            messageBox2.setWindowIcon(QtGui.QIcon(self.icon_path))
            messageBox2.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            buttonY2 = messageBox2.button(QtWidgets.QMessageBox.Yes)
            buttonY2.setText('删除')
            buttonN2 = messageBox2.button(QtWidgets.QMessageBox.No)
            buttonN2.setText('取消')
            messageBox2.exec_()
            if messageBox2.clickedButton() == buttonN2:
                return
        else:
            return

        # 删除界面列表中相应的工程文件夹及文件
        if messageBox2.clickedButton() == buttonY2:
            self.selectedRow = list()
            for i in selected_items:
                if self.tableWidget_project_manage.indexFromItem(i).row() not in self.selectedRow:
                    self.selectedRow.append(self.tableWidget_project_manage.indexFromItem(i).row())
            self.selectedRow.reverse()        # 将选定行的行号降序排序，只有从索引大的行开始删除，才不会出现错误

            # 删除相应的工程文件夹及文件
            for i in self.selectedRow:
                project_name = self.tableWidget_project_manage.item(i, 0).text()
                fulldirct = os.path.join(self.project_path, project_name)
                for root, dirs, files in os.walk(fulldirct, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(fulldirct)

                # 删除表格中的工程栏
                self.tableWidget_project_manage.removeRow(i)
        else:
            return

    def add_project(self):
        global ID
        global creator
        global now_time

        #填写工程(多输入)
        self.di = QtWidgets.QDialog()
        d = project_manage_dialog.Ui_Dialog()
        d.setupUi(self.di)
        self.di.show()

        if self.di.exec_():
            project_name, creator = d.get_data()
            if project_name == "":
                return
            if creator == "":
                return
            if '.' in project_name:
                print("违规字符")
                QtWidgets.QMessageBox.information(self, "提示", "工程名不能包含”.”，请重新输入")
                return
            print(project_name)
            print(creator)

            # 创建工程文件夹
            path = os.sep.join([self.project_path, project_name])  # 以分隔符连接路径名
            if not os.path.exists(path):
                os.makedirs(path)
                print(path + '创建成功')

                #新增工程栏，并填入工程信息
                index = self.tableWidget_project_manage.rowCount()
                self.tableWidget_project_manage.insertRow(self.tableWidget_project_manage.rowCount())
                newItem = QtWidgets.QTableWidgetItem(project_name)
                newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget_project_manage.setItem(index, 0, newItem)

                newItem = QtWidgets.QTableWidgetItem(creator)
                newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget_project_manage.setItem(index, 1, newItem)

                # 填写当前日期时间
                now_time = datetime.datetime.now().strftime('%F %T')
                newItem = QtWidgets.QTableWidgetItem(now_time)
                newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget_project_manage.setItem(index, 2, newItem)

                # 填写ID
                ID = str(datetime.datetime.now().year) + str(datetime.datetime.now().month) + str(datetime.datetime.now().day) + str(datetime.datetime.now().hour) + str(datetime.datetime.now().minute) + str(datetime.datetime.now().second)
                newItem = QtWidgets.QTableWidgetItem(ID)
                newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget_project_manage.setItem(index, 3, newItem)

                if self.tableWidget_project_manage.item(0, 0).text() == " ":
                    QtWidgets.QMessageBox.critical(self, "错误", "请输入工程名")

            else:
                # 如果目录存在则不创建，并提示目录已存在
                QtWidgets.QMessageBox.critical(self, "错误", "工程已存在")
                print(path + '目录已存在')
                # return False

            # 创建ballotBoxInformation.ini文件
            fulldirct = os.path.join(self.project_path, project_name, "ballotBoxInformation.ini")
            fw = open(fulldirct, 'w')
            fw.write(" ")  # 把字典转化为str
            fw.close()

    def load_mode2election(self):
        print("load_mode2election")
        global mode2election

        config = configparser.ConfigParser()
        file = config.read(os.path.join(project_path, "election2mode.ini"))
        config_dict = config.defaults()
        for mode in config_dict:
            mode2election[mode] = config_dict[mode]
        pass

    def enter_project(self):
        global ID
        global creator
        global now_time
        global databaseName

        selected_items = self.tableWidget_project_manage.selectedItems()

        if len(selected_items) == 0:  # 说明没有选中任何行，跳出
            QtWidgets.QMessageBox.critical(self, "错误", "请单击选择工程")
            return

        elif len(selected_items) > 4:  # 只能进入一个工程，跳出
            QtWidgets.QMessageBox.critical(self, "错误", "只能进入一个工程")
            return

        self.selectedRow = []
        for i in selected_items:
            if self.tableWidget_project_manage.indexFromItem(i).row() not in self.selectedRow:
                self.selectedRow.append(self.tableWidget_project_manage.indexFromItem(i).row())

        global project_name
        for i in self.selectedRow:
            project_name = self.tableWidget_project_manage.item(i, 0).text()
            # ID = self.tableWidget_project_manage.item(i, 3).text()
            # creator = self.tableWidget_project_manage.item(i, 1).text()
            # now_time = self.tableWidget_project_manage.item(i, 2).text()

            # 设置当前工程路径
            global project_path
            project_path = os.sep.join([self.project_path, project_name])  # 以分隔符连接路径名
            if not os.path.exists(project_path):
                QtWidgets.QMessageBox.information(self, "提示", project_name + "工程文件丢失，若该工程已不再使用则请删除，若仍需使用该工程，请将旧版本的SmartVote/project文件夹覆盖新版本的SmartVote/project文件夹")
                return

            # 发送信号，进入工程
            self.show_mainWindow_signal.emit()
            print("进入" + project_name + "工程")

            glo.set_value("cur_project", project_name)
            glo.set_value("project_path", project_path)
            # 初始化了一个 长度为100*8 的存坐标的数组
            glo.set_value("position", [[None] * 8 for i in range(100)])


        self.CommunicationSettingSubUI.init()
        self.FunctionTestSubUI.init()
        self.OperationMonitoringSubUI.init()
        self.SettingSubUI.init()
        self.WeldingGunLibrarySubUI.init()






