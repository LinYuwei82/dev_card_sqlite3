# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(360, 180)
        font = QtGui.QFont()
        font.setFamily("OPPOSans R")
        font.setPointSize(12)
        Form.setFont(font)
        self.label_user = QtWidgets.QLabel(Form)
        self.label_user.setGeometry(QtCore.QRect(70, 50, 60, 25))
        self.label_user.setObjectName("label_user")
        self.lineEdit_user = QtWidgets.QLineEdit(Form)
        self.lineEdit_user.setGeometry(QtCore.QRect(140, 50, 150, 25))
        self.lineEdit_user.setObjectName("lineEdit_user")
        self.lineEdit_pwd = QtWidgets.QLineEdit(Form)
        self.lineEdit_pwd.setGeometry(QtCore.QRect(140, 90, 150, 25))
        self.lineEdit_pwd.setObjectName("lineEdit_pwd")
        self.label_pwd = QtWidgets.QLabel(Form)
        self.label_pwd.setGeometry(QtCore.QRect(70, 90, 60, 25))
        self.label_pwd.setObjectName("label_pwd")
        self.pushButton_login = QtWidgets.QPushButton(Form)
        self.pushButton_login.setGeometry(QtCore.QRect(80, 140, 75, 30))
        self.pushButton_login.setObjectName("pushButton_login")
        self.pushButton_exit = QtWidgets.QPushButton(Form)
        self.pushButton_exit.setGeometry(QtCore.QRect(200, 140, 75, 30))
        self.pushButton_exit.setObjectName("pushButton_exit")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "系统登录"))
        self.label_user.setText(_translate("Form", "用户名："))
        self.label_pwd.setText(_translate("Form", "密 码："))
        self.pushButton_login.setText(_translate("Form", "登录"))
        self.pushButton_exit.setText(_translate("Form", "退出"))