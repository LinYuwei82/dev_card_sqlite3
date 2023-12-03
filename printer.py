import os

from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont, pdfmetrics
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# (os.path.join(BASE_DIR, ""))
x = 62 + 5.5
y = 65 + 6.5

# 注册字体
opposansB = "OPPOSansB"
opposansR = "OPPOSansR"

pdfmetrics.registerFont(TTFont(opposansB, (os.path.join(BASE_DIR, "fonts/OPPOSans-B.ttf"))))
pdfmetrics.registerFont(TTFont(opposansR, (os.path.join(BASE_DIR, "fonts/OPPOSans-R.ttf"))))


class CardModel:
    card_x = 0
    card_y = 0

    def __init__(self, c, card_x, card_y):
        self.c = c
        self.card_x = card_x
        self.card_y = card_y

    def card_model_print(self):
        # 画边框
        self.c.saveState()  # 保存状态
        self.c.setStrokeColorRGB(0, 0, 0, alpha=0.8)
        self.c.setLineWidth(0.8)
        self.c.rect((6.5 + self.card_x) * mm, (8 + self.card_y) * mm, 62 * mm, 65 * mm, stroke=1, fill=0)

        # 画线
        self.c.setLineWidth(0.5)
        self.c.line((28 + self.card_x) * mm, (37.5 + self.card_y) * mm, (63.5 + self.card_x) * mm,
                    (37.5 + self.card_y) * mm)
        self.c.line((28 + self.card_x) * mm, (30.0 + self.card_y) * mm, (63.5 + self.card_x) * mm,
                    (30.0 + self.card_y) * mm)
        self.c.line((28 + self.card_x) * mm, (22.5 + self.card_y) * mm, (63.5 + self.card_x) * mm,
                    (22.5 + self.card_y) * mm)
        self.c.line((28 + self.card_x) * mm, (15.0 + self.card_y) * mm, (63.5 + self.card_x) * mm,
                    (15.0 + self.card_y) * mm)

        # 画logo
        self.c.drawImage((os.path.join(BASE_DIR, "ico/anyelogo.jpg")), (10 + self.card_x) * mm,
                         (58.5 + self.card_y) * mm, width=25, height=25)

        # 公司名
        textobject1 = self.c.beginText()
        textobject1.setTextOrigin((20 + self.card_x) * mm, (62 + self.card_y) * mm)
        textobject1.setFont(opposansB, 11)
        textobject1.setHorizScale(88)
        textobject1.setFillColorCMYK(0.99, 0.85, 0.11, 0)
        textobject1.textLine("深圳市安业物业管理有限公司")
        self.c.drawText(textobject1)

        # 卡名
        textobject2 = self.c.beginText()
        textobject2.setTextOrigin((23 + self.card_x) * mm, (52 + self.card_y) * mm)
        textobject2.setFont(opposansB, 15)
        textobject2.setHorizScale(105)
        textobject2.setCharSpace(2)
        textobject2.setFillColorCMYK(0, 0, 0, 1)
        textobject2.textLine("设备管理卡")
        self.c.drawText(textobject2)

        # 左边字段
        textobject3 = self.c.beginText()
        textobject3.setTextOrigin((10 + self.card_x) * mm, (38.5 + self.card_y) * mm)
        textobject3.setFont(opposansR, 11)
        textobject3.setHorizScale(75)
        textobject3.setCharSpace(0.75)
        textobject3.setFillColorCMYK(0, 0, 0, 1)
        textobject3.textLine("设备名称：")
        self.c.drawText(textobject3)

        textobject4 = self.c.beginText()
        textobject4.setTextOrigin((10 + self.card_x) * mm, (31 + self.card_y) * mm)
        textobject4.setFont(opposansR, 11)
        textobject4.setHorizScale(75)
        textobject4.setCharSpace(0.75)
        textobject4.setFillColorCMYK(0, 0, 0, 1)
        textobject4.textLine("位      置：")
        self.c.drawText(textobject4)

        textobject5 = self.c.beginText()
        textobject5.setTextOrigin((10 + self.card_x) * mm, (23.5 + self.card_y) * mm)
        textobject5.setFont(opposansR, 11)
        textobject5.setHorizScale(75)
        textobject5.setCharSpace(0.75)
        textobject5.setFillColorCMYK(0, 0, 0, 1)
        textobject5.textLine("控制范围：")
        self.c.drawText(textobject5)

        textobject6 = self.c.beginText()
        textobject6.setTextOrigin((10 + self.card_x) * mm, (16 + self.card_y) * mm)
        textobject6.setFont(opposansR, 11)
        textobject6.setHorizScale(75)
        textobject6.setCharSpace(0.75)
        textobject6.setFillColorCMYK(0, 0, 0, 1)
        textobject6.textLine("维护电话：")
        self.c.drawText(textobject6)
        self.c.restoreState()  # 恢复状态


class CardData:
    card_x = 0
    card_y = 0

    def __init__(self, c, card_x, card_y):
        self.c = c
        self.card_x = card_x
        self.card_y = card_y

    def card_data_print(self, dev_name, location, control_range, phone):
        self.c.saveState()  # 保存状态

        textobject1 = self.c.beginText()
        textobject1.setTextOrigin((30 + self.card_x) * mm, (38.5 + self.card_y) * mm)
        textobject1.setFont(opposansB, 11)
        textobject1.setHorizScale(90)
        textobject1.setCharSpace(0.9)
        textobject1.setFillColorCMYK(0, 0, 0, 1)
        textobject1.textLine(dev_name)
        self.c.drawText(textobject1)

        textobject2 = self.c.beginText()
        textobject2.setTextOrigin((30 + self.card_x) * mm, (31 + self.card_y) * mm)
        textobject2.setFont(opposansB, 11)
        textobject2.setHorizScale(90)
        textobject2.setCharSpace(0.9)
        textobject2.setFillColorCMYK(0, 0, 0, 1)
        textobject2.textLine(location)
        self.c.drawText(textobject2)

        textobject3 = self.c.beginText()
        textobject3.setTextOrigin((30 + self.card_x) * mm, (23.5 + self.card_y) * mm)
        textobject3.setFont(opposansB, 11)
        textobject3.setHorizScale(90)
        textobject3.setCharSpace(0.9)
        textobject3.setFillColorCMYK(0, 0, 0, 1)
        textobject3.textLine(control_range)
        self.c.drawText(textobject3)

        textobject4 = self.c.beginText()
        textobject4.setTextOrigin((30 + self.card_x) * mm, (16 + self.card_y) * mm)
        textobject4.setFont(opposansB, 11)
        textobject4.setHorizScale(90)
        textobject4.setCharSpace(0.9)
        textobject4.setFillColorCMYK(0, 0, 0, 1)
        textobject4.textLine(phone)
        self.c.drawText(textobject4)

        self.c.restoreState()  # 恢复状态


class CardReceive:
    def __init__(self, result):
        self.result = result

    def card_data_receive(self, file_name):
        # sql = 'select * from tb_device'
        row = len(self.result)
        # 开始循环
        data_list = []
        for ii in range(row):
            data = []  # 每读完一组就清空当前列表
            for jj in range(1, 5):
                data.append(self.result[ii][jj])
            data_list.append(data)

        # 建立PDF文档
        c1 = canvas.Canvas(file_name)
        # 移动页面原点到左上角
        c1.translate(0 * mm, y * 3 * mm)
        k = 0
        while k < row:
            for i in range(4):  # 从上到下
                for j in range(3):  # 从左到右
                    if k < row:
                        c1_instance = CardModel(c1, j * x, (0 - i * y))
                        c1_instance.card_model_print()
                        c2_instance = CardData(c1, j * x, (0 - i * y))
                        c2_instance.card_data_print(data_list[k][0], data_list[k][1], data_list[k][2],
                                                    data_list[k][3])
                        k += 1
                        # print(k)
                        if k % 12 == 0:  # 满12组换下一页
                            c1.showPage()
                            c1.translate(0 * mm, y * 3 * mm)  # 移动页面原点到新页面左上角
            # print(k)
            # print(row)
        c1.save()


if __name__ == '__main__':
    pass
    # sql = 'select * from tb_device'

    # result = service.query_db(sql)
    # card1 = CardReceive(result)
    # card1.card_data_receive()

    # main1 = main.MainWindow()
    # result = main1.show_all()
    # print(result)
    # len(result)
