from PyQt5 import QtWidgets, QtGui, Qt

from UI import processingDialog


class ProcessDialog(QtWidgets.QDialog, processingDialog.Ui_Dialog):
    def __init__(self, parent=None):
        super(ProcessDialog, self).__init__(parent)
        self.setupUi(self)
        # self.setWindowIcon(QtGui.QIcon('printer.png'))

        # 进度条繁忙
        self.progressBar.setInvertedAppearance(False)  # 进度条走向
        # self.progressBar.setOrientation(Qt.Horizontal)  # 进度条的方向
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(0)
        self.progressBar.setValue(0)

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
