# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reset_password_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(542, 230)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("printer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_c = QtWidgets.QLabel(Dialog)
        self.label_c.setObjectName("label_c")
        self.gridLayout.addWidget(self.label_c, 1, 0, 1, 1)
        self.lineEdit_newpassword = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_newpassword.setObjectName("lineEdit_newpassword")
        self.gridLayout.addWidget(self.lineEdit_newpassword, 1, 1, 1, 1)
        self.label_p = QtWidgets.QLabel(Dialog)
        self.label_p.setObjectName("label_p")
        self.gridLayout.addWidget(self.label_p, 0, 0, 1, 1)
        self.lineEdit_oldpassword = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_oldpassword.setObjectName("lineEdit_oldpassword")
        self.gridLayout.addWidget(self.lineEdit_oldpassword, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.lineEdit_reconfirm_password = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_reconfirm_password.setObjectName("lineEdit_reconfirm_password")
        self.gridLayout.addWidget(self.lineEdit_reconfirm_password, 2, 1, 1, 1)
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

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_c.setText(_translate("Dialog", "新密码："))
        self.label_p.setText(_translate("Dialog", "原登录密码："))
        self.label.setText(_translate("Dialog", "再次输入新的密码："))
