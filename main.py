import os
import sys

import pandas as pd
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QFileDialog

import printer
import service
import user
from main_ui import Ui_mainWindow

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class MainWindow(QMainWindow, Ui_mainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.setWindowIcon(QIcon(os.path.join(BASE_DIR, 'ico/app.png')))
        self.setWindowTitle("设备管理卡制作系统 Ver 0.01")
        self.tb_device.setAlternatingRowColors(True)  # 使表格颜色交错显示
        self.tb_device.verticalHeader().setVisible(False)  # 隐藏垂直标题
        # self.tb_device.resizeColumnsToContents()
        datetime = QtCore.QDateTime.currentDateTime()  # 获取当前日期时间
        time = datetime.toString("yyyy-MM-dd HH:mm:ss")  # 对日期时间进行格式化
        # 在状态栏中显示登录用户/登录时间，以及版权信息
        self.statusbar.showMessage("当前登录用户：" + service.userName + " | 登录时间：" + time
                                   + " | 版权所有：深圳市安业物业管理有限公司", 0)
        self.bind_name()
        self.bind_location()
        self.bind_kind()
        self.show_all()
        self.tb_device.itemClicked.connect(self.get_item)
        self.btn_reset.clicked.connect(self.reset)
        self.btn_exit.clicked.connect(self.exit_sys)
        self.btn_user.clicked.connect(self.open_user)
        self.btn_add.clicked.connect(self.add)
        self.btn_edit.clicked.connect(self.edit)
        self.btn_delete.clicked.connect(self.delete)
        self.btn_show_all.clicked.connect(self.show_all)
        self.btn_query.clicked.connect(self.query)
        self.btn_import.clicked.connect(self.import_excel)
        self.btn_export.clicked.connect(self.export_excel)
        self.edit_query.returnPressed.connect(self.query)
        self.btn_delete_all.clicked.connect(self.delete_all)
        self.btn_remove_duplicate.clicked.connect(self.remove_duplicate)
        self.btn_print_preview.clicked.connect(self.print_left)  # 点击打开左边，打印到PDF文件（刷新）窗口
        self.btn_print.clicked.connect(self.print_right)  # 点击打开右，打印到PDF文件（查询）窗口

    def open_user(self):
        self.m = user.UserWindow()  # 建用户窗口实例
        self.m.show()

    def remove_duplicate(self):  # 去除重复数据
        res = service.remove_duplicate_info()
        if res == QMessageBox.Yes:
            result = service.exec_remove_duplicate()
            if result > 0:
                self.show_all()
                QMessageBox.information(None, '提示', '重复数据合并完毕！', QMessageBox.Ok)

    def delete_all(self):
        res = service.delete_all_info()
        if res == QMessageBox.Yes:
            result = service.exec_del('delete from tb_device')
            if result > 0:
                self.show_all()
                QMessageBox.information(None, '提示', '全部数据已清空！', QMessageBox.Ok)

    def bind_name(self):
        self.cmbox_name.addItem('所有')
        result = service.query_db('select dev_name from tb_device')
        existing_name = []
        for i in result:
            key = i[0]
            if key not in existing_name:
                self.cmbox_name.addItem(i[0])
                existing_name.append(key)

    def bind_location(self):
        self.cmbox_location.addItem('所有')
        result = service.query_db('select location from tb_device')
        existing_name = []
        for i in result:
            key = i[0]
            if key not in existing_name:
                self.cmbox_location.addItem(i[0])
                existing_name.append(key)

    def bind_kind(self):
        self.cmbox_kind.addItem('设备名称')
        self.cmbox_kind.addItem('位置')
        self.cmbox_kind.addItem('控制范围')
        self.cmbox_kind.addItem('维护电话')

    def reset(self):
        self.label_id.setText('')
        self.edit_name.setText('')
        self.edit_location.setText('')
        self.edit_range.setText('')
        self.edit_phone.setText('')
        self.select = ''

    def get_item(self, item):
        if item.column() == 0:
            self.select = item.text()
            self.label_id.setText(self.select)
            result = service.query_db('select * from tb_device where dev_id=?', item.text())
            self.edit_name.setText(result[0][1])
            self.edit_location.setText(result[0][2])
            self.edit_range.setText(result[0][3])
            self.edit_phone.setText(result[0][4])

    def get_name(self):
        pass

    def import_excel(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, '导入Excel文件', 'tb_device.xlsx', 'Excel文件 (*.xlsx)',
                                                   options=options)
        if file_name:
            data = pd.read_excel(file_name)
            for i in data.itertuples():
                values = tuple(i[2:])
                sql = 'insert into tb_device (dev_name,location,control_range,phone) values (?,?,?,?)'
                service.exec_db(sql, *values)
            QMessageBox.information(None, '提示', 'Excel文件已成功导入！', QMessageBox.Ok)
            self.show_all()

    def export_excel(self):
        sql = 'select * from tb_device'
        result1, result2 = service.query_desc(sql)  # result1（所有行的列表）和result2（查询结果的描述）
        data = pd.DataFrame(result1, columns=[desc[0] for desc in result2])
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, '导出Excel文件', 'tb_device.xlsx', 'Excel文件 (*.xlsx)',
                                                   options=options)
        if file_name:
            data.to_excel(file_name, index=False)
            QMessageBox.information(None, '提示', '已成功导出Excel文件！', QMessageBox.Ok)

    def show_all(self):  # 精确查询，对应【刷新】按钮
        self.tb_device.setRowCount(0)
        name = self.cmbox_name.currentText()
        location = self.cmbox_location.currentText()
        if name == '所有':
            if location == '所有':
                result = service.query_db('select dev_id, dev_name, location, control_range, phone from tb_device')
            else:
                result = service.query_db('select dev_id, dev_name, location, control_range, phone from tb_device '
                                          'where location=?', location)
        else:
            if location == '所有':
                result = service.query_db('select dev_id, dev_name, location, control_range, phone from tb_device '
                                          'where dev_name=?', name)
            else:
                result = service.query_db('select dev_id, dev_name, location, control_range, phone from tb_device '
                                          'where dev_name=? and location=?', name, location)
        # return result  # 2023年11月29日，为了返回打印值新增测试用
        row = len(result)
        self.tb_device.setRowCount(row)
        self.tb_device.setColumnCount(5)
        self.tb_device.setHorizontalHeaderLabels(['设备编号', '设备名称', '位  置', '控制范围', '维护电话'])
        for i in range(row):
            for j in range(self.tb_device.columnCount()):
                data = QTableWidgetItem(str(result[i][j]))
                # data.setCheckState(False)
                self.tb_device.setItem(i, j, data)
                # self.tb_device.resizeColumnsToContents()
        return result  # 2023年11月29日，为了返回打印值新增测试用

    def query(self):  # 模糊查询，对应【查询】按钮
        self.tb_device.setRowCount(0)
        if self.edit_query.text() == '':
            result = service.query_db('select dev_id, dev_name, location, control_range, phone from tb_device')
        else:
            key = self.edit_query.text()
            if self.cmbox_kind.currentText() == '设备名称':
                sql = 'select dev_id, dev_name, location, control_range, phone from tb_device where dev_name like ' \
                      '"%' + key + '%"'
                result = service.query_db2(sql)
            elif self.cmbox_kind.currentText() == '位置':
                sql = 'select dev_id, dev_name, location, control_range, phone from tb_device where location like ' \
                      '"%' + key + '%"'
                result = service.query_db2(sql)
            elif self.cmbox_kind.currentText() == '控制范围':
                sql = 'select dev_id, dev_name, location, control_range, phone from tb_device where control_range ' \
                      'like "%' + key + '%"'
                result = service.query_db2(sql)
            elif self.cmbox_kind.currentText() == '维护电话':
                sql = 'select dev_id, dev_name, location, control_range, phone from tb_device where phone like ' \
                      '"%' + key + '%"'
                result = service.query_db2(sql)
        row = len(result)
        self.tb_device.setRowCount(row)
        self.tb_device.setColumnCount(5)
        self.tb_device.setHorizontalHeaderLabels(['设备编号', '设备名称', '位  置', '控制范围', '维护电话'])
        for i in range(row):
            for j in range(self.tb_device.columnCount()):
                data = QTableWidgetItem(str(result[i][j]))
                self.tb_device.setItem(i, j, data)
        return result  # 2023年11月29日，为了返回打印值新增测试用

    def print_left(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, '打印到PDF文件', '设备管理卡(刷新).pdf', 'Pdf文件 (*.pdf)',
                                                   options=options)
        if file_name:
            # data.to_excel(file_name, index=False)
            result = self.show_all()
            card = printer.CardReceive(result)
            card.card_data_receive(file_name)
            QMessageBox.information(None, '提示', '已成功打印到PDF文件！', QMessageBox.Ok)

    def print_right(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, '打印到PDF文件', '设备管理卡(查询).pdf', 'Pdf文件 (*.pdf)',
                                                   options=options)
        if file_name:
            # data.to_excel(file_name, index=False)
            result = self.query()
            card = printer.CardReceive(result)
            card.card_data_receive(file_name)
            QMessageBox.information(None, '提示', '已成功打印到PDF文件！', QMessageBox.Ok)

    def add(self):
        dev_name = self.edit_name.text()
        location = self.edit_location.text()
        control_range = self.edit_range.text()
        phone = self.edit_phone.text()
        if dev_name != '' and location != '' and control_range != '' and phone != '':
            sql = 'select count(*) from tb_device where dev_name=? and location=? and control_range=?'
            count = service.query_count(sql, dev_name, location, control_range)
            if count >= 1:
                QMessageBox.information(None, '提示', '你要添加的设备己经存在，请重新输入', QMessageBox.Ok)
                self.edit_range.setText('')
            else:
                sql = 'insert into tb_device (dev_name,location,control_range,phone) values (?,?,?,?)'
                result = service.exec_db(sql, dev_name, location, control_range, phone)
                if result > 0:
                    sql = 'select dev_id from tb_device where dev_name=? and location=? and control_range=? ' \
                          'and phone=?'
                    dev_id = service.query_db(sql, dev_name, location, control_range, phone)
                    self.label_id.setText(str(dev_id[0][0]))
                    self.show_all()
                    QMessageBox.information(None, '提示', '信息添加成功！', QMessageBox.Ok)
                    self.reset()
                    self.select = ''
        else:
            QMessageBox.warning(None, '警告', '请输入数据后，再执行相关操作！', QMessageBox.Ok)

    def edit(self):
        try:
            if self.select != "":
                dev_id = self.select
                dev_name = self.edit_name.text()
                location = self.edit_location.text()
                control_range = self.edit_range.text()
                phone = self.edit_phone.text()
                sql = 'update tb_device set dev_name=?, location=?, control_range=?, phone=? where dev_id=?'
                result = service.exec_db(sql, dev_name, location, control_range, phone, dev_id)
                if result > 0:
                    self.show_all()
                    QMessageBox.information(None, '提示', '信息修改成功！', QMessageBox.Ok)
                    self.reset()
                    self.select = ''
            else:
                QMessageBox.warning(None, '警告', '请先选择要修改的数据！', QMessageBox.Ok)

        except:
            QMessageBox.warning(None, '警告', '请先选择要修改的数据！', QMessageBox.Ok)

    def delete(self):
        try:
            if self.select != '':
                res = service.delete_info()
                if res == QMessageBox.Yes:
                    result = service.exec_db('delete from tb_device where dev_id=?', self.select, )
                    if result > 0:
                        self.show_all()
                        self.reset()
                        QMessageBox.information(None, '提示', '信息删除成功！', QMessageBox.Ok)
                        self.select = ''
            else:
                QMessageBox.warning(None, '警告', '请先选择要删除的数据！', QMessageBox.Ok)
        except:
            QMessageBox.warning(None, '警告', '请先选择要删除的数据！', QMessageBox.Ok)

    def exit_sys(self):  # 退出系统确认窗口
        result = service.exit_info()
        if result == QMessageBox.Yes:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
