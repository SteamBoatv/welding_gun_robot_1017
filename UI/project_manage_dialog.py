# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'project_manage_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(406, 194)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("printer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_creator = QtWidgets.QLabel(Dialog)
        self.label_creator.setObjectName("label_creator")
        self.gridLayout.addWidget(self.label_creator, 1, 0, 1, 1)
        self.lineEdit_creator = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_creator.setObjectName("lineEdit_creator")
        self.gridLayout.addWidget(self.lineEdit_creator, 1, 1, 1, 1)
        self.label_project_name = QtWidgets.QLabel(Dialog)
        self.label_project_name.setObjectName("label_project_name")
        self.gridLayout.addWidget(self.label_project_name, 0, 0, 1, 1)
        self.lineEdit_project_name = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_project_name.setObjectName("lineEdit_project_name")
        self.gridLayout.addWidget(self.lineEdit_project_name, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 3, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 2, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 1, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 1, 2, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def get_data(self):
        return self.lineEdit_project_name.text(), self.lineEdit_creator.text()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_creator.setText(_translate("Dialog", "创建人："))
        self.label_project_name.setText(_translate("Dialog", "工程名称："))
