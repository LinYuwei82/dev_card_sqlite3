import os
import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QMessageBox

import service
from user_ui import Ui_MainWindow

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class UserWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.setWindowIcon(QIcon(os.path.join(BASE_DIR, 'resources/icons/app.png')))
        self.setStatusBar(None)
        self.tableWidget_user.setAlternatingRowColors(True)  # 使表格颜色交错显示
        self.tableWidget_user.verticalHeader().setVisible(False)  # 隐藏垂直标题
        self.query_db()
        self.btn_add.clicked.connect(self.add)
        self.tableWidget_user.itemClicked.connect(self.get_item)
        self.btn_modify.clicked.connect(self.edit)
        self.btn_delete.clicked.connect(self.delete)
        self.btn_exit.clicked.connect(self.close)

    def query_db(self):
        self.tableWidget_user.setRowCount(0)
        result = service.query_db('select * from tb_user')
        row = len(result)
        self.tableWidget_user.setRowCount(row)
        self.tableWidget_user.setColumnCount(2)
        self.tableWidget_user.setHorizontalHeaderLabels(['用户名', '密码'])
        for i in range(row):
            for j in range(self.tableWidget_user.columnCount()):
                date = QTableWidgetItem(str(result[i][j]))
                self.tableWidget_user.setItem(i, j, date)

    def get_item(self, item):
        if item.column() == 0:
            self.select = item.text()
            self.lineEdit_name.setText(self.select)

    def add(self):
        userName = self.lineEdit_name.text()
        userPwd = self.lineEdit_pwd.text()
        if userName != '' and userPwd != '':
            result = service.exec_db('insert into tb_user (userName, userPwd) values (?, ?)',
                                     userName, userPwd)
            if result > 0:
                self.query_db()
                QMessageBox.information(None, '提示', '信息添加成功！', QMessageBox.Ok)
        else:
            QMessageBox.warning(None, '警告', '请输入数据后，再执行相关操作！', QMessageBox.Ok)

    def edit(self):
        try:
            if self.select != '':
                userPwd = self.lineEdit_pwd.text()
                if userPwd != '':
                    result = service.exec_db('update tb_user set userPwd=? '
                                             'where userName=?', userPwd, self.select, )
                    if result > 0:
                        self.query_db()
                        QMessageBox.information(None, '捍示', '信息修改成功！', QMessageBox.Ok)
        except:
            QMessageBox.warning(None, '警告', '请先选择需要修改的数据！', QMessageBox.Ok)

    def delete(self):
        try:
            if self.select != '':
                result = service.exec_db('delete from tb_user where userName=?', self.select, )
                if result > 0:
                    self.query_db()
                    QMessageBox.information(None, '提示', '信息删除成功！', QMessageBox.Ok)
        except:
            QMessageBox.warning(None, '警告', '请选择要删除的数据！', QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = UserWindow()
    main_window.show()
    sys.exit(app.exec())
