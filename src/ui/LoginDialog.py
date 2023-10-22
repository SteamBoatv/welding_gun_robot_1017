import configparser
import os

from UI import login_dialog, reset_password_dialog
from PyQt5 import QtWidgets, QtGui, QtCore

ADMINISTRATOR_PASSWORD = "root"

class LoginDialog(QtWidgets.QDialog, login_dialog.Ui_Dialog):

    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)
        self.setting_path = 'resource/setting.ini'
        self.user_path = 'resource/user.ini'
        self.icon_path = 'resource/printer.png'

        self.setupUi(self)
        self.setWindowTitle("登录界面")
        self.setWindowIcon(QtGui.QIcon(self.icon_path))
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushButton_login.clicked.connect(self.login)
        self.pushButton_reset_password.clicked.connect(self.reset_password)
        self.load_config()

        # self.groupBox.setStyleSheet("#groupBox{border-image: url(:/pic_rc/背景2.jpg);}")

        # 设置events_table的右键菜单
        self.groupBox.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # 在tableWidget中点击右键的触发事件
        self.groupBox.customContextMenuRequested[QtCore.QPoint].connect(self.context_menu_of_events_table)

    def init(self):
        config = configparser.ConfigParser()
        file = config.read(self.setting_path)
        config_dict = config.defaults()

        # icon = QtGui.QPixmap(config_dict["symbol"])
        # self.label_symbol.setPixmap(icon)
        # self.label_symbol.setScaledContents(True)

        background_path = config_dict["background"]
        self.groupBox.setStyleSheet("#groupBox{border-image: url("+ background_path +");}")

        company = config_dict["company"]
        self.label_company.setText(company)

        # 右键点击事件
    def context_menu_of_events_table(self,pos):

        pop_menu = QtWidgets.QMenu()
        # setIcon = pop_menu.addAction('设置标题图标')
        setBackground = pop_menu.addAction('设置背景')
        setCompany = pop_menu.addAction('设置公司名称')

        # 获取右键菜单中当前被点击的是哪一项
        action = pop_menu.exec_(self.groupBox.mapToGlobal(pos))

        # 如果选中的是添加新的工程
        # if action == setIcon:
        #     self.set_icon()

        if action == setBackground:
            self.set_background()

        elif action == setCompany:
            self.set_company()

    def set_company(self):
        settingFileIsExist = os.path.exists(self.setting_path)
        if settingFileIsExist == True:
            company, ok = QtWidgets.QInputDialog.getText(self, '请输入新的公司名称', '输入公司名称：')
            if ok and company:
                self.label_company.setText(company)

            # 存储icon链接
            config = configparser.ConfigParser()
            file = config.read(self.setting_path)
            config_dict = config.defaults()
            config["DEFAULT"] = {
                "company": company,
                "symbol": config_dict['symbol'],
                "background": config_dict['background']
            }
            with open(self.setting_path, 'w') as configfile:
                config.write(configfile)
        else:
            pass

    def set_icon(self):
        settingFileIsExist = os.path.exists(self.setting_path)
        if settingFileIsExist == True:
            # 获取icon链接
            icon_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open files', './', 'jpg Files (*.jpg)')
            if icon_path == "":
                print("没有获取icon文件")
                return

            # 更换icon
            icon = QtGui.QPixmap(icon_path)
            self.label_symbol.setPixmap(icon)
            self.label_symbol.setScaledContents(True)

            # 存储icon链接
            config = configparser.ConfigParser()
            file = config.read(self.setting_path)
            config_dict = config.defaults()
            config["DEFAULT"] = {
                "company": config_dict['company'],
                "symbol": icon_path,
                "background": config_dict['background']
            }

            with open(self.setting_path, 'w') as configfile:
                config.write(configfile)
        else:
            pass

    def set_background(self):
        settingFileIsExist = os.path.exists(self.setting_path)
        if settingFileIsExist == True:
            # 获取icon链接
            background_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open files', './', 'jpg Files (*.jpg)')
            if background_path == "":
                print("没有获取背景图片")
                return

            # 更换背景
            self.groupBox.setStyleSheet("#groupBox{border-image: url(" + background_path + ");}")
            # mainWin.gridFrame.setStyleSheet("#gridFrame{border-image: url(" + background_path + ");}")

            # 存储icon链接
            config = configparser.ConfigParser()
            file = config.read(self.setting_path)
            config_dict = config.defaults()
            config["DEFAULT"] = {
                "company": config_dict['company'],
                "symbol": config_dict['symbol'],
                "background": background_path
            }

            with open(self.setting_path, 'w') as configfile:
                config.write(configfile)
        else:
            pass

    def load_config(self):
        config = configparser.ConfigParser()
        file = config.read(self.user_path)
        config_dict = config.defaults()
        self.user_name = config_dict['user_name']
        self.password = config_dict['password']
        self.lineEdit__account.setText(self.user_name)

        if config_dict['remember'] == 'True':
            self.lineEdit_password.setText(self.password)
            self.checkBox_remember_password.setChecked(True)
        else:
            self.checkBox_remember_password.setChecked(False)

    def reset_password(self):
        self.user_name = self.lineEdit__account.text()
        self.password = self.lineEdit_password.text()

        di = QtWidgets.QDialog()
        d = ChangePasswordDialog()
        d.setupUi(di)
        d.lineEdit_oldpassword.setFocus()
        di.show()
        if di.exec_():
            oldpassword, newpassword, reconfirm_password = d.return_imformation()

            config = configparser.ConfigParser()
            file = config.read(self.user_path)
            config_dict = config.defaults()
            if (oldpassword == config_dict['password'] and newpassword == reconfirm_password) or (oldpassword == ADMINISTRATOR_PASSWORD):
                config["DEFAULT"] = {
                    "user_name": config_dict['user_name'],
                    "password": newpassword,
                    "remember": self.checkBox_remember_password.isChecked()
                }
                with open(self.user_path, 'w')as configfile:
                    config.write(configfile)

                QtWidgets.QMessageBox.information(self, "提示", "密码修改成功")
                self.lineEdit__account.setText(self.user_name)
                self.lineEdit_password.clear()
            else:
                QtWidgets.QMessageBox.critical(self, "错误", "原始密码不正确或两次输入的新密码不相同。")

    def login(self):
        self.user_name = self.lineEdit__account.text()
        self.password = self.lineEdit_password.text()
        config = configparser.ConfigParser()
        file = config.read(self.user_path)
        config_dict = config.defaults()
        if self.password == config_dict['password'] and self.user_name == config_dict['user_name']:

            if self.checkBox_remember_password.isChecked():
                config["DEFAULT"] = {
                    "user_name": config_dict['user_name'],
                    "password": config_dict['password'],
                    "remember": self.checkBox_remember_password.isChecked()
                }
            else:
                config["DEFAULT"] = {
                    "user_name": config_dict['user_name'],
                    "password": config_dict['password'],
                    "remember": self.checkBox_remember_password.isChecked()
                }
            with open('user.ini', 'w')as configfile:
                config.write(configfile)

            self.accept()
        else:
            print("密码或用户名错误")
            QtWidgets.QMessageBox.critical(self, "错误", "密码或用户名错误")

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class ChangePasswordDialog(reset_password_dialog.Ui_Dialog):

    def return_imformation(self):
        return self.lineEdit_oldpassword.text(), self.lineEdit_newpassword.text(), self.lineEdit_reconfirm_password.text()
