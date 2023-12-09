import os
import sys

import pandas as pd
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QFileDialog

import printer
import service
import user
from UI.main_ui import Ui_mainWindow

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class MainWindow(QMainWindow, Ui_mainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.setWindowIcon(QIcon(os.path.join(BASE_DIR, 'resources/icons/app.png')))
        self.setWindowTitle("设备管理卡制作系统" + service.Ver)
        self.tb_device.setAlternatingRowColors(True)  # 使表格颜色交错显示
        self.tb_device.verticalHeader().setVisible(False)  # 隐藏垂直标题
        # self.tb_device.resizeColumnsToContents()
        datetime = QtCore.QDateTime.currentDateTime()  # 获取当前日期时间
        self.time = datetime.toString("yyyy-MM-dd HH:mm:ss")  # 对日期时间进行格式化
        # 在状态栏中显示登录用户/登录时间，以及版权信息/记录数
        self.refresh_status_bar()
        # self.bind_name()
        # self.bind_location()
        self.refresh_cmbox()
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

    def refresh_status_bar(self):  # 刷新service.record的值
        self.statusbar.showMessage("当前登录用户：" + service.userName + "  |  登录时间：" + self.time
                                   + "  |  版权所有：" + service.copyrights +
                                   "                    " + "共计  " + service.record + "  条记录", 0)

    def refresh_cmbox(self):
        self.cmbox_name.clear()
        self.cmbox_location.clear()
        self.cmbox_name.addItem("所有")
        self.cmbox_location.addItem("所有")
        self.existing_name = []
        self.bind_name()
        self.bind_location()


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
                self.refresh_cmbox()
                self.show_all()
                self.reset()
                QMessageBox.information(None, '提示', '全部数据已清空！', QMessageBox.Ok)

    def bind_name(self):
        # self.cmbox_name.addItem('所有')
        result = service.query_db('select dev_name from tb_device')
        # existing_name = []
        for i in result:
            key = i[0]
            if key not in self.existing_name:
                self.cmbox_name.addItem(i[0])
                self.existing_name.append(key)

    def bind_location(self):
        # self.cmbox_location.addItem('所有')
        result = service.query_db('select location from tb_device')
        # existing_name = []
        for i in result:
            key = i[0]
            if key not in self.existing_name:
                self.cmbox_location.addItem(i[0])
                self.existing_name.append(key)

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
            truncated_fields = ['dev_name', 'location', 'control_range', 'phone']  # 由于导入的phone可能是数值类型，而数值类型不支持切片操作
            max_length = [10, 10, 10, 11]
            for field, max_length in zip(truncated_fields, max_length):
                if field == 'phone':  # 对phone字段进行特殊处理，先转换为字符串类型再进行截断
                    data[field] = data[field].apply(lambda x: str(x)[:max_length] if len(str(x)) > max_length else x)
                else:
                    data[field] = data[field].apply(lambda x: x[:max_length] if len(x) > max_length else x)
            line = 0
            for i in data.itertuples():
                values = tuple(i[2:])
                sql = 'insert into tb_device (dev_name,location,control_range,phone) values (?,?,?,?)'
                service.exec_db(sql, *values)
                line += 1
            new_line = 'Excel文件已成功导入  ' + str(line) + '  条记录！'
            QMessageBox.information(None, '提示', new_line, QMessageBox.Ok)
            self.show_all()

    def export_excel(self):
        sql = 'select * from tb_device'
        result1, result2 = service.query_desc(sql)  # result1（所有行的列表）和result2（查询结果的描述）
        row = len(result1)
        new_line = '已成功导出  ' + str(row) + '  条记录到Excel文件！'
        data = pd.DataFrame(result1, columns=[desc[0] for desc in result2])
        # 过滤掉phone字段中的非数字字符
        data['phone'] = data['phone'].apply(lambda x: ''.join(filter(str.isdigit, str(x))))
        # 将phone字段转换为数值类型
        data['phone'] = pd.to_numeric(data['phone'], errors='coerce')  # 设置为coerce可以将无法转换为数值的值设置为NaN

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, '导出Excel文件', 'tb_device.xlsx', 'Excel文件 (*.xlsx)',
                                                   options=options)
        if file_name:
            data.to_excel(file_name, index=False)
            QMessageBox.information(None, '提示', new_line, QMessageBox.Ok)

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
        service.record = str(row)
        self.refresh_status_bar()  # 状态栏刷新记录数
        self.tb_device.setRowCount(row)
        self.tb_device.setColumnCount(5)
        self.tb_device.setHorizontalHeaderLabels(['设备编号', '设备名称', '位  置', '控制范围', '维护电话'])
        for i in range(row):
            for j in range(self.tb_device.columnCount()):
                data = QTableWidgetItem(str(result[i][j]))
                self.tb_device.setItem(i, j, data)
        self.bind_name()
        self.bind_location()
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
        service.record = str(row)
        self.refresh_status_bar()  # 状态栏刷新记录数
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
                    self.refresh_cmbox()
                    self.show_all()
                    QMessageBox.information(None, '提示', '信息修改成功！', QMessageBox.Ok)
                    self.reset()
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
                        self.refresh_cmbox()
                        self.show_all()
                        self.reset()
                        QMessageBox.information(None, '提示', '信息删除成功！', QMessageBox.Ok)

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
