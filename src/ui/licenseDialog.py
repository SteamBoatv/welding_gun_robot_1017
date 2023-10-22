from UI import license_dialog
from PyQt5 import QtWidgets, QtGui
from src import auth

class licenseDialog(QtWidgets.QDialog, license_dialog.Ui_Dialog):
    def __init__(self, parent=None):
        super(licenseDialog, self).__init__(parent)
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
