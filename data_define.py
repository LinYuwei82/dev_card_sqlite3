class Device:
    def __init__(self, dev_name, location, control_range, phone, dev_id=None):
        self.dev_name = dev_name
        self.location = location
        self.control_range = control_range
        self.phone = phone
        self.dev_id = dev_id

    def __str__(self):
        return f"{self.dev_id}, {self.dev_name}, {self.location}, {self.control_range}, {self.phone}"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.dev_name == other.dev_name) and (self.location == other.location) and (
                    self.control_range == other.control_range) and (
                    self.phone == other.phone)
        else:
            return NotImplemented

# 建立数据库：
# create database if not exists devicedb;
#
# 建立表：
# create table if not exists tb_device (dev_id int primary key auto_increment, dev_name varchar(20),
# location varchar(20), control_range varchar(20), phone varchar(20));
# create table if not exists tb_user (userName varchar(20) primary key , userPwd varchar(20))
