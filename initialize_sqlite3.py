import os
import sqlite3

# def open_db(database):
#     db = sqlite3.connect(database)
#     return db
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# (os.path.join(BASE_DIR, ""))

def exec_db(sql, *values):
    db = sqlite3.connect(os.path.join(BASE_DIR, 'devicedb.db'))
    cursor = db.cursor()
    try:
        cursor.execute(sql, values)  # 执行增删改的SQL语句
        db.commit()
        return 1  # 执行成功
    except:
        db.rollback()  # 发生错误时回滚
        return 0
    finally:
        cursor.close()  # 关闭游标
        db.close()  # 关闭数据库连接


def init_data():
    sql1 = 'create table if not exists tb_device (dev_id INTEGER primary key AUTOINCREMENT, dev_name TEXT, ' \
           'location TEXT, control_range TEXT, phone TEXT)'
    sql2 = 'create table if not exists tb_user (userName TEXT primary key , userPwd TEXT)'

    sql3 = 'insert into tb_user (userName, userPwd) values ("root","123456")'
    sql4 = 'insert into tb_user (userName, userPwd) values ("安业物业","123456")'
    sql5 = 'insert into tb_device (dev_id, dev_name, location, control_range, phone) values (1, "配电箱","艺术楼2楼",' \
           '"艺术楼2楼各教室","138 0013 8000")'
    try:
        exec_db(sql1)
        exec_db(sql2)
        exec_db(sql3)
        exec_db(sql4)
        # exec_db(sql5)
        return 1
    except:
        return 0


if __name__ == '__main__':
    init_data()
    print(BASE_DIR)
