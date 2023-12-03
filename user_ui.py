# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'user_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(330, 248)
        font = QtGui.QFont()
        font.setFamily("OPPOSans R")
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 0, 311, 241))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget_user = QtWidgets.QTableWidget(self.layoutWidget)
        self.tableWidget_user.setObjectName("tableWidget_user")
        self.tableWidget_user.setColumnCount(0)
        self.tableWidget_user.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget_user)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_name = QtWidgets.QLabel(self.layoutWidget)
        self.label_name.setObjectName("label_name")
        self.horizontalLayout.addWidget(self.label_name)
        self.lineEdit_name = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.horizontalLayout.addWidget(self.lineEdit_name)
        self.label_pwd = QtWidgets.QLabel(self.layoutWidget)
        self.label_pwd.setObjectName("label_pwd")
        self.horizontalLayout.addWidget(self.label_pwd)
        self.lineEdit_pwd = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_pwd.setObjectName("lineEdit_pwd")
        self.horizontalLayout.addWidget(self.lineEdit_pwd)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.btn_add = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_add.setObjectName("btn_add")
        self.horizontalLayout_2.addWidget(self.btn_add)
        self.btn_modify = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_modify.setObjectName("btn_modify")
        self.horizontalLayout_2.addWidget(self.btn_modify)
        self.btn_delete = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_delete.setObjectName("btn_delete")
        self.horizontalLayout_2.addWidget(self.btn_delete)
        self.btn_exit = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_exit.setObjectName("btn_exit")
        self.horizontalLayout_2.addWidget(self.btn_exit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "用户信息维护"))
        self.label_name.setText(_translate("MainWindow", "用户名称："))
        self.label_pwd.setText(_translate("MainWindow", "用户密码："))
        self.btn_add.setText(_translate("MainWindow", "添加"))
        self.btn_modify.setText(_translate("MainWindow", "修改"))
        self.btn_delete.setText(_translate("MainWindow", "删除"))
        self.btn_exit.setText(_translate("MainWindow", "退出"))
