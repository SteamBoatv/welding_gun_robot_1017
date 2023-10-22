from PyQt5 import QtWidgets, QtGui

from UI.sub_UI import WeldingGunLibrary

class WeldingGunLibrarySubUI(QtWidgets.QMainWindow, WeldingGunLibrary.Ui_MainWindow):
    def __init__(self, parent=None):
        super(WeldingGunLibrarySubUI, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("焊接包")

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def init(self):
        pass