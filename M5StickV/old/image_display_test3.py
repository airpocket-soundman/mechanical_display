from machine import I2C
import time
import pca9685
import servo

class mechanical_display:
    def __init__(self, i2c, unit_layout = [1, 1],servo_layout = [4, 4], gray_scale_bit_value = 4):

        self.i2c = i2c
        self.unit_layout = unit_layout
        self.servo_layout = servo_layout
        self.gray_scale_bit_value = gray_scale_bit_value
#UnitのI2C addressのリスト定義
        self.UnitAddressList = [[64, 65, 66, 67],
                                [68, 69, 70, 71],
                                [72, 73, 74, 75],
                                [76, 77, 78, 79]]
#        self.UnitAddressList = [[64, 68, 72, 76],
#                                [65, 69, 73, 77],
#                                [66, 70, 74, 78],
#                                [67, 71, 75, 79]]

#UnitのIDのリスト定義
        print("set UnitIDList")
        self.unit_ID_list = []
        n = 0
        for y in range(self.unit_layout[1]):
            list = []
            for x in range(self.unit_layout[0]):
                print("x,y",x,y)
                list.append(n)
                n += 1
            self.unit_ID_list.append(list)

        temp = []
        for i in range(len(self.unit_ID_list[0])):
            list = []
            for j in self.unit_ID_list:
                list.append(j[i])
            temp.append(list)
        self.unit_ID_list = temp

        print("unit_ID_list:",self.unit_ID_list)

#Unit内のPixel位置とサーボIDの対応を定義
        self.UnitPixelIDList = [[ 0,  4,  8, 12],
                                [ 1,  5,  9, 13],
                                [ 2,  6, 10, 14],
                                [ 3,  7, 11, 15]]

#unit_ID_listとUnitPixelIDListから、displayのPixelとUnitID,各ユニットのPixelIDを対応させるPixelIDListを生成する
        print("set PixelIDList")
        self.PixelIDList = []

        for x in range(self.unit_layout[0]):
            for k in range(4):
                list = []
                for y in  range(self.unit_layout[1]):
                    print("x,y",x,y)
                    UnitID = self.unit_ID_list[x][y]
                    print("UnitID", UnitID)
                    print(self.UnitPixelIDList)
                    for l in range(4):
                        list.append([UnitID,self.UnitPixelIDList[k][l]])

                self.PixelIDList.append(list)

        #生成されたPixelIDListを確認
        print("PixelIDList:")
        for i in range(len(self.PixelIDList)):
            print(self.PixelIDList[i])

# サーボのキャリブレーションデータ 4*4ユニット対応版

        self.usCenter= [[1550, 1480, 1430, 1450,  1650, 1530, 1460, 1440,  1430, 1410, 1560, 1440,  1440, 1420, 1430, 1550],
                        [1440, 1560, 1460, 1580,  1500, 1445, 1580, 1390,  1470, 1430, 1460, 1370,  1520, 1480, 1500, 1600],
                        [1420, 1550, 1570, 1525,  1500, 1640, 1480, 1580,  1550, 1680, 1515, 1420,  1550, 1590, 1515, 1550],
                        [1590, 1680, 1500, 1420,  1590, 1420, 1500, 1370,  1540, 1470, 1470, 1530,  1485, 1500, 1650, 1490],

                        [1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500],
                        [1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500],
                        [1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500],
                        [1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500],

                        [1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500],
                        [1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500],
                        [1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500],
                        [1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500],

                        [1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500],
                        [1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500],
                        [1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500],
                        [1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500]]


        self.usMax   = [[2020, 1880, 1800, 1840,  2120, 1960, 1850, 1830,  1890, 1860, 1980, 1840,  1900, 1840, 1830, 1930],
                        [1830, 1940, 1840, 1970,  1890, 1870, 1920, 1770,  1870, 1850, 1860, 1770,  1900, 1870, 1910, 1990],
                        [1910, 1960, 1950, 1920,  1980, 2060, 1870, 1990,  2030, 2060, 1890, 1860,  1980, 2020, 1930, 1960],
                        [1980, 2020, 1870, 1800,  1960, 1820, 1880, 1740,  1930, 1890, 1900, 1900,  1880, 1900, 2000, 1860],

                        [1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900],
                        [1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900],
                        [1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900],
                        [1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900],

                        [1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900],
                        [1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900],
                        [1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900],
                        [1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900],

                        [1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900],
                        [1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900],
                        [1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900],
                        [1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900]]


        self.usMin   = [[1180, 1080, 1060, 1080,  1290, 1130, 1050, 1030,  1080, 1010, 1220, 1020,  1080, 1000, 1030, 1100],
                        [1050, 1170, 1060, 1200,  1100, 1030, 1210, 1010,  1100, 1000, 1070,  980,  1170, 1070, 1140, 1170],
                        [1050, 1100, 1190, 1080,  1180, 1230, 1100, 1190,  1190, 1260, 1140,  970,  1200, 1100, 1120, 1100],
                        [1200, 1280, 1150, 1040,  1220, 1050, 1170, 1000,  1180, 1070, 1120, 1140,  1150, 1130, 1290, 1130],

                        [1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100],
                        [1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100],
                        [1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100],
                        [1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100],

                        [1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100],
                        [1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100],
                        [1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100],
                        [1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100],

                        [1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100],
                        [1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100],
                        [1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100],
                        [1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100]]


        # 4bitグレースケール用のポジションリストを生成する

        print("4bit GrayScale List generating")
        self.us4bitGrayScalePositionList  = []
        for i in range(8):
            listUnit = []
            for j in range(16):
                listServo = []
                for k in range(16):
                    listServo.append(int(self.usMin[j][k] + (((self.usCenter[j][k] - self.usMin[j][k]) / 15) * i * 2)))
                listUnit.append(listServo)
            self.us4bitGrayScalePositionList.append(listUnit)

        for i in range(8):
            listUnit = []
            for j in range(16):
                listServo = []
                for k in range(16):
                    listServo.append(int((self.usCenter[j][k] + (((self.usMax[j][k] - self.usCenter[j][k]) / 15)) + (((self.usMax[j][k] - self.usCenter[j][k]) / 15) * i * 2))))
                listUnit.append(listServo)
            self.us4bitGrayScalePositionList.append(listUnit)

        #9番目にフラット面の座標を追加
        self.us4bitGrayScalePositionList.append(self.usCenter)

        print("4bit GrayScale List generate complete.")
        print("unit 0, scale 7")
        for i in range(8):
            print(self.us4bitGrayScalePositionList[7][i])
        print("unit 0, scale 8")
        for i in range(8):
            print(self.us4bitGrayScalePositionList[8][i])

#サーボドライバ初期化
        self.pca = []
        for i in range(self.unit_layout[1]):
            for j in range(self.unit_layout[0]):
                self.pca.append(servo.Servos(self.i2c, address = self.UnitAddressList[i][j]))

# imageを表示するメソッド
    def setImage(self, img):
        #print("set image")
        #print(self.unit_layout[0])
        #imgのサイズとdisplayのサイズがマッチするか確認
        if len(img) != (self.unit_layout[0] * 4):
            print("image width unmatched")
            return
        elif len(img[1]) != (self.unit_layout[1] * 4):
            print("image height unmatched")
            return

        #差分を確認



        #変化のあったピクセルだけを動かす
        #リリースする

        #とりあえず4bitGrayでもらって表示するだけ
        for y in range(self.unit_layout[1]*4):
            for x in range(self.unit_layout[0]*4):
                self.setPixel([x,y],img[x][y])
        self.oldImage = img

# 指定ピクセルを表示するメソッド
    #Valueは3bitGrayに限る
    def setPixel(self, coordinate, value):
        x = coordinate[0]
        y = coordinate[1]
        usValue = self.usValue(coordinate, value)
        self.pca[self.PixelIDList[x][y][0]].position(self.PixelIDList[x][y][1], us=usValue)

# ピクセル座標と色調（bit数）と値から、サーボのusの値を計算して返す
    def usValue(self, coordinate = [0, 0], gray_scale_color = 0):
        x = coordinate[0]
        y = coordinate[1]
        unit_ID  = self.PixelIDList[x][y][0]
        servo_ID = self.PixelIDList[x][y][1]
        usCenter = self.usCenter[unit_ID][servo_ID]
        usMax = self.usMax[unit_ID][servo_ID]
        usMin = self.usMin[unit_ID][servo_ID]
        gray_scale_level = 2 ** self.gray_scale_bit_value

        if gray_scale_color < (gray_scale_level / 2):
            us = int(usMin + (((usCenter - usMin) / (gray_scale_level - 1)) * gray_scale_color * 2))
        elif gray_scale_color == gray_scale_level:
            us = usCenter
        else:
            us = int(usMax - (((usMax - usCenter) / (gray_scale_level - 1)) * (gray_scale_level - 1 - gray_scale_color) * 2))
        return us


# 全てのパネルをセンター位置に移動する
    def flatPosition(self):
        print("flat position")
        #self.setImage(self.flatImage)

        for y in range(self.unit_layout[1]*4):
            for x in range(self.unit_layout[0]*4):
                self.pca[self.PixelIDList[x][y][0]].position(self.PixelIDList[x][y][1], us=self.usCenter[self.PixelIDList[x][y][0]][self.PixelIDList[x][y][1]])

# 全てのパネルを最大位置に移動する
    def maxPosition(self):
        print("max position")
        #self.setImage(self.maxImage)

        for y in range(self.unit_layout[1]*4):
            for x in range(Layout[0]*4):
                self.pca[self.PixelIDList[x][y][0]].position(self.PixelIDList[x][y][1], us=self.usMax[self.PixelIDList[x][y][0]][self.PixelIDList[x][y][1]])

# 全てのパネルを最小位置に移動する
    def minPosition(self):
        print("min position")
        #self.setImage(self.minImage)

        for y in range(self.unit_layout[1]*4):
            for x in range(Layout[0]*4):
                self.pca[self.PixelIDList[x][y][0]].position(self.PixelIDList[x][y][1], us=self.usMin[self.PixelIDList[x][y][0]][self.PixelIDList[x][y][1]])

# 全てのサーボをリリースするメソッド
    def Release(self, coordinate = 0):
        #全てのサーボをリリース
        if coordinate == 0:
            print("all servo release")
            for y in range(self.unit_layout[1]*4):
                for x in range(self.unit_layout[0]*4):
                    self.pca[self.PixelIDList[x][y][0]].release(self.PixelIDList[x][y][1])
        else:
            try:
                x = coordinate[0]
                y = coordinate[1]
                self.pca[self.PixelIDList[x][y][0]].release(self.PixelIDList[x][y][1])

            except:
                print("image size unmatched")


#displayのUnit配置数定義
unit_layout  = [2, 2]          #[width,height]　現在は[4,4]まで対応。増やす際は、I2Cのaddressリストも修正が必要。
servo_layout = [4, 4]
gray_scale_bit_value = 8
gray_scale_level = 2**gray_scale_bit_value

#I2C　初期化
i2c = I2C(I2C.I2C0, freq=100000, scl=34, sda=35)

#I2C 接続されているユニットのアドレス確認
addr = i2c.scan()
print( "address is :" + str(addr) )

#displayのインスタンス生成
display = mechanical_display(i2c, unit_layout, servo_layout, gray_scale_bit_value)

#flatポジションを表示する。
display.flatPosition()
time.sleep_ms(300)


"""
l16 = [16,16,16,16,16,16,16,16]
l15 = [15,15,15,15,15,15,15,15]
l14 = [14,14,14,14,14,14,14,14]
l13 = [13,13,13,13,13,13,13,13]
l12 = [12,12,12,12,12,12,12,12]
l11 = [11,11,11,11,11,11,11,11]
l10 = [10,10,10,10,10,10,10,10]
l9 = [9,9,9,9,9,9,9,9]
l8 = [8,8,8,8,8,8,8,8]
l7 = [7,7,7,7,7,7,7,7]
l6 = [6,6,6,6,6,6,6,6]
l5 = [5,5,5,5,5,5,5,5]
l4 = [4,4,4,4,4,4,4,4]
l3 = [3,3,3,3,3,3,3,3]
l2 = [2,2,2,2,2,2,2,2]
l1 = [1,1,1,1,1,1,1,1]
l0 = [0,0,0,0,0,0,0,0]

image = [l16,l16,l16,l16,l16,l16,l16,l16]
display.setImage(image)

time.sleep_ms(100)
image = [l16,l16,l16,l16,l16,l16,l16,l8]
display.setImage(image)

time.sleep_ms(100)
image = [l16,l16,l16,l16,l16,l16,l8,l9]
display.setImage(image)

time.sleep_ms(100)
image = [l16,l16,l16,l16,l16,l8,l9,l10]
display.setImage(image)

time.sleep_ms(100)
image = [l16,l16,l16,l16,l8,l9,l10,l11]
display.setImage(image)

time.sleep_ms(100)
image = [l16,l16,l16,l8,l9,l10,l11,l12]
display.setImage(image)

time.sleep_ms(100)
image = [l16,l16,l8,l9,l10,l11,l12,l13]
display.setImage(image)

time.sleep_ms(100)
image = [l16,l8,l9,l10,l11,l12,l13,l14]
display.setImage(image)





for i in range(1):


    time.sleep_ms(100)
    image = [l8,l9,l10,l11,l12,l13,l14,l15]
    display.setImage(image)

    time.sleep_ms(100)
    image = [l9,l10,l11,l12,l13,l14,l15,l0]
    display.setImage(image)

    time.sleep_ms(100)
    image = [l10,l11,l12,l13,l14,l15,l0,l1]
    display.setImage(image)

    time.sleep_ms(100)
    image = [l11,l12,l13,l14,l15,l0,l1,l2]
    display.setImage(image)

    time.sleep_ms(100)
    image = [l12,l13,l14,l15,l0,l1,l2,l3]
    display.setImage(image)

    time.sleep_ms(100)
    image = [l13,l14,l15,l0,l1,l2,l3,l4]
    display.setImage(image)

    time.sleep_ms(100)
    image = [l14,l15,l0,l1,l2,l3,l4,l5]
    display.setImage(image)

    time.sleep_ms(100)
    image = [l15,l0,l1,l2,l3,l4,l5,l6]
    display.setImage(image)

    time.sleep_ms(100)
    image = [l0,l1,l2,l3,l4,l5,l6,l7]
    display.setImage(image)

    time.sleep_ms(100)
    image = [l1,l2,l3,l4,l5,l6,l7,l8]
    display.setImage(image)

    time.sleep_ms(100)
    image = [l2,l3,l4,l5,l6,l7,l8,l9]
    display.setImage(image)

    time.sleep_ms(100)
    image = [l3,l4,l5,l6,l7,l8,l9,l10]
    display.setImage(image)

    time.sleep_ms(100)
    image = [l4,l5,l6,l7,l8,l9,l10,l11]
    display.setImage(image)

    time.sleep_ms(100)
    image = [l5,l6,l7,l8,l9,l10,l11,l12]
    display.setImage(image)

    time.sleep_ms(100)
    image = [l6,l7,l8,l9,l10,l11,l12,l13]
    display.setImage(image)

    time.sleep_ms(100)
    image = [l7,l8,l9,l10,l11,l12,l13,l14]
    display.setImage(image)








time.sleep_ms(100)
image = [l8,l9,l10,l11,l12,l13,l14,l15]
display.setImage(image)

time.sleep_ms(100)
image = [l9,l10,l11,l12,l13,l14,l15,l0]
display.setImage(image)

time.sleep_ms(100)
image = [l10,l11,l12,l13,l14,l15,l0,l1]
display.setImage(image)

time.sleep_ms(100)
image = [l11,l12,l13,l14,l15,l0,l1,l2]
display.setImage(image)

time.sleep_ms(100)
image = [l12,l13,l14,l15,l0,l1,l2,l3]
display.setImage(image)

time.sleep_ms(100)
image = [l13,l14,l15,l0,l1,l2,l3,l4]
display.setImage(image)

time.sleep_ms(100)
image = [l14,l15,l0,l1,l2,l3,l4,l5]
display.setImage(image)

time.sleep_ms(100)
image = [l15,l0,l1,l2,l3,l4,l5,l6]
display.setImage(image)

time.sleep_ms(100)
image = [l0,l1,l2,l3,l4,l5,l6,l7]
display.setImage(image)

time.sleep_ms(100)
image = [l1,l2,l3,l4,l5,l6,l7,l16]
display.setImage(image)
time.sleep_ms(100)
image = [l2,l3,l4,l5,l6,l7,l16,l16]
display.setImage(image)

time.sleep_ms(100)
image = [l3,l4,l5,l6,l7,l16,l16,l16]
display.setImage(image)

time.sleep_ms(100)
image = [l4,l5,l6,l7,l16,l16,l16,l16]
display.setImage(image)

time.sleep_ms(100)
image = [l5,l6,l7,l16,l16,l16,l16,l16]
display.setImage(image)

time.sleep_ms(100)
image = [l6,l7,l16,l16,l16,l16,l16,l16]
display.setImage(image)

time.sleep_ms(100)
image = [l7,l16,l16,l16,l16,l16,l16,l16]
display.setImage(image)

time.sleep_ms(100)
image = [l16,l16,l16,l16,l16,l16,l16,l16]
display.setImage(image)

"""






for i in range(gray_scale_level):
    display.setPixel([7,7],i)
#    print(i)
    time.sleep_ms(12)
#time.sleep_ms(100)

for i in range(gray_scale_level):
    display.setPixel([7,7],gray_scale_level - 1 - i)
#    print(i)
    time.sleep_ms(12)

#time.sleep_ms(100)

for i in range(gray_scale_level):
    display.setPixel([7,7],i)
#    print(i)
    time.sleep_ms(12)
time.sleep_ms(100)
display.setPixel([7,7],gray_scale_level)

#display.flatPosition()
time.sleep_ms(1000)
display.Release()

