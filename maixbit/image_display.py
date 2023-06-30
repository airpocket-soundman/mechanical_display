from machine import I2C
import time
import pca9685
import servo

class mechanical_display:
    def __init__(self, i2c, unit_layout = [1, 1], servo_layout = [4, 4], gray_scale_bit_size = 4):
        print("mechanical_display initialize")

        self.i2c = i2c                                                                              #pca9685と通信するi2c接続のインスタンス
        self.unit_layout = unit_layout                                                              #ディスプレイに使用するユニットのレイアウト[x, y]　x:幅方向 y:縦方向
        self.servo_layout = servo_layout                                                            #１ユニットのサーボのレイアウト[x, y]　x:幅方向 y:縦方向
        self.pixel_layout = [unit_layout[0] * servo_layout[1], unit_layout[1] * servo_layout[1]]    #ディスプレイのpixelのレイアウト[x, y]
        self.gray_scale_bit_size = gray_scale_bit_size                                              #グレースケールの階調数のビット数 2 ** gray_scale_bit_size = 階調数

        img = []
        #フラットイメージを作ってsetImage()関数を使って表示する
        for y in range(self.pixel_layout[1]):
            list = []
            for x in range(self.pixel_layout[0]):
                list.append(2 ** self.gray_scale_bit_size)
            img.append(list)

        self.oldImage = img

#UnitのI2C addressのリスト定義
        self.UnitAddressList = [[64, 65, 66, 67],
                                [68, 69, 70, 71],
                                [72, 73, 74, 75],
                                [76, 77, 78, 79]]
        print("UnitAddressList:", self.UnitAddressList)

#UnitのIDのリスト定義
        print("set unit_id_list")
        self.unit_id_list = []
        n = 0
        for y in range(self.unit_layout[1]):
            list = []
            for x in range(self.unit_layout[0]):
                print("x,y",x,y)
                list.append(n)
                n += 1
            self.unit_id_list.append(list)

        temp = []
        for i in range(len(self.unit_id_list[0])):
            list = []
            for j in self.unit_id_list:
                list.append(j[i])
            temp.append(list)
        self.unit_id_list = temp

        print("unit_id_list:",self.unit_id_list)

#Unit内のPixel位置とサーボIDの対応を定義
        self.unit_pixel_id_list = [[ 0,  4,  8, 12],
                                   [ 1,  5,  9, 13],
                                   [ 2,  6, 10, 14],
                                   [ 3,  7, 11, 15]]

#unit_id_listとunit_pixel_id_listから、displayのPixelとUnitID,各ユニットのPixelIDを対応させるdisplay_pixel_id_listを生成する
        print("set display_pixel_id_list")
        self.display_pixel_id_list = []


        for x in range(self.unit_layout[0]):
            for k in range(self.servo_layout[0]):
                list = []
                for y in  range(self.unit_layout[1]):
                    print("x,y",x,y)
                    UnitID = self.unit_id_list[x][y]
                    print("UnitID", UnitID)
                    print(self.unit_pixel_id_list)
                    for l in range(self.servo_layout[0]):
                        list.append([UnitID,self.unit_pixel_id_list[k][l]])

                self.display_pixel_id_list.append(list)

        #生成されたdisplay_pixel_id_listを確認
#        print("display_pixel_id_list:")
#        for i in range(len(self.display_pixel_id_list)):
#            print(self.display_pixel_id_list[i])

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


        # グレースケール用のポジションリストを生成する メモリをセーブするためにも、都度計算の方が良いかも。

        print("GrayScale List generating")
        #gray_scale_position_list
        self.gray_scale_position_list  = []
        for i in range((2 ** self.gray_scale_bit_size) / 2):
            listUnit = []
            for j in range(2 ** self.gray_scale_bit_size):
                listServo = []
                for k in range(2 ** self.gray_scale_bit_size):
                    listServo.append(int(self.usMin[j][k] + (((self.usCenter[j][k] - self.usMin[j][k]) / ((2 ** self.gray_scale_bit_size) - 1)) * i * 2)))
                listUnit.append(listServo)
            self.gray_scale_position_list.append(listUnit)

        for i in range((2 ** self.gray_scale_bit_size) / 2):
            listUnit = []
            for j in range(2 ** self.gray_scale_bit_size):
                listServo = []
                for k in range(2 ** self.gray_scale_bit_size):
                    listServo.append(int((self.usCenter[j][k] + (((self.usMax[j][k] - self.usCenter[j][k]) / ((2 ** self.gray_scale_bit_size) - 1))) + (((self.usMax[j][k] - self.usCenter[j][k]) / ((2 ** self.gray_scale_bit_size) - 1)) * i * 2))))
                listUnit.append(listServo)
            self.gray_scale_position_list.append(listUnit)

        #9番目にフラット面の座標を追加
        self.gray_scale_position_list.append(self.usCenter)


#サーボドライバ初期化
        self.pca = []
        for i in range(self.unit_layout[1]):
            for j in range(self.unit_layout[0]):
                self.pca.append(servo.Servos(self.i2c, address = self.UnitAddressList[i][j]))

#　フラット位置表示
        self.setImage(img)

# imageを表示するメソッド
    def setImage(self, img):
        print("set image")
        #imgのサイズとdisplayのサイズがマッチするか確認
        if len(img) != (self.pixel_layout[0]):
            print("image width unmatched")
            return
        elif len(img[1]) != (self.pixel_layout[1]):
            print("image height unmatched")
            return

        #差分を確認



        #変化のあったピクセルだけを動かす
        #リリースする

        """
        #自力でイメージ表示
        for y in range(self.pixel_layout[1]):
            for x in range(self.pixel_layout[0]):
                print("set pixel",x,y,img[x][y])
                self.pca[self.display_pixel_id_list[x][y][0]].position(self.display_pixel_id_list[x][y][1], us=self.gray_scale_position_list[img[x][y]][self.display_pixel_id_list[x][y][0]][self.display_pixel_id_list[x][y][1]])
        """

        #setPixel関数に投げてイメージ表示
        for y in range(self.pixel_layout[1]):
            for x in range(self.pixel_layout[0]):
                print("set pixel",x,y,img[x][y])
                self.setPixel(img[x][y],[x, y])

# 指定ピクセルを表示するメソッド value = -1 でリリース coordinate = Noneで画面全体をvalueの値を表示する
    def setPixel(self, value, coordinate = None):
        x1 = coordinate[0]
        x2 = coordinate[0]
        y1 = coordinate[1]
        y2 = coordinate[1]
        print("set pixcel:",value,coordinate)

        if (value < -1) and (value > 2 ** self.gray_scale_bit_size):
            print("gray scale value is out of range >",value)
            return

        if (coordinate[0] < 0) and (coordinate[0] > self.pixel_layout[0]):
            print("coodinate x is out of range >",coordinate[0])
            return

        if (coordinate[1] < 0) and (coordinate[1] > self.pixel_layout[1]):
            print("coodinate y is out of range >",coordinate[1])
            return


        if coordinate == None:
            x1 = 0
            x2 = self.pixel_layout[0]
            y1 = 0
            y2 = self.pixel_layout[1]

        else:
            x1 = coordinate[0]
            x2 = coordinate[0] + 1
            y1 = coordinate[1]
            y2 = coordinate[1] + 1

            for y in range(y1, y2 ,1):
                for x in range(x1, x2, 1):
                    if value == -1:
                        print("release")
                        self.pca[self.display_pixel_id_list[x][y][0]].release(self.display_pixel_id_list[x][y][1])

                    else:
                        print("self.display_pixel_id_list[x][y][0]",self.display_pixel_id_list[x][y][0])
                        print("self.display_pixel_id_list[x][y][1]",self.display_pixel_id_list[x][y][1])
                        print("self.gray_scale_position_list[value][self.display_pixel_id_list[x][y][0]][self.display_pixel_id_list[x][y][1]]",self.gray_scale_position_list[value][self.display_pixel_id_list[x][y][0]][self.display_pixel_id_list[x][y][1]])
                        self.pca[self.display_pixel_id_list[x][y][0]].position(self.display_pixel_id_list[x][y][1], us=self.gray_scale_position_list[value][self.display_pixel_id_list[x][y][0]][self.display_pixel_id_list[x][y][1]])
                        self.oldImage[x][y] = value

        # self.oldImg 生成


# ディスプレイ一面を指定色で塗りつぶす
    def setDisplay(self, value = None):
        print("set Display value color")
        for y in range(self.pixel_layout[1]):
            for x in range(self.pixel_layout[0]):
                print(x,y)
                self.setPixel(value,[x, y])


# 全てのパネルをセンター位置に移動する
    def flatPosition(self):
        print("flat position")

        img = []
        #フラットイメージを作ってsetImage()関数を使って表示する
        for y in range(self.pixel_layout[1]):
            list = []
            for x in range(self.pixel_layout[0]):
                list.append(2 ** self.gray_scale_bit_size)
            img.append(list)

        self.setImage(img)

        """
        #サーボを直接制御する
        for y in range(self.pixel_layout[1]):
            for x in range(self.pixel_layout[0]):
                self.pca[self.display_pixel_id_list[x][y][0]].position(self.display_pixel_id_list[x][y][1], us=self.usCenter[self.display_pixel_id_list[x][y][0]][self.display_pixel_id_list[x][y][1]])
        """


# 全てのパネルを最大位置に移動する
    def maxPosition(self):
        print("max position")
        #self.setImage(self.maxImage)

        img = []
        #maxイメージを作ってsetImage()関数を使って表示する
        for y in range(self.pixel_layout[1]):
            list = []
            for x in range(self.pixel_layout[0]):
                list.append((2 ** self.gray_scale_bit_size - 1))
            img.append(list)

        self.setImage(img)

        """
        #サーボを直接制御する
        for y in range(self.pixel_layout[1]):
            for x in range(self.pixel_layout[0]):
                self.pca[self.display_pixel_id_list[x][y][0]].position(self.display_pixel_id_list[x][y][1], us=self.usMax[self.display_pixel_id_list[x][y][0]][self.display_pixel_id_list[x][y][1]])
        """

# 全てのパネルを最小位置に移動する
    def minPosition(self):
        print("min position")
        #self.setImage(self.minImage)

        for y in range(self.pixel_layout[1]):
            for x in range(self.pixel_layout[0]):
                self.pca[self.display_pixel_id_list[x][y][0]].position(self.display_pixel_id_list[x][y][1], us=self.usMin[self.display_pixel_id_list[x][y][0]][self.display_pixel_id_list[x][y][1]])

# 全てのサーボをリリースするメソッド
    def Release(self, coordinate = 0):
        # 全てのサーボをリリース
        if coordinate == 0:
            print("all servo release")
            for y in range(self.pixel_layout[1]):
                for x in range(self.pixel_layout[0]):
                    self.pca[self.display_pixel_id_list[x][y][0]].release(self.display_pixel_id_list[x][y][1])
        #
        else:
            try:
                x = coordinate[0]
                y = coordinate[1]
                self.pca[self.display_pixel_id_list[x][y][0]].release(self.display_pixel_id_list[x][y][1])

            except:
                print("image size unmatched")

    """
# ピクセル座標と色調（bit数）と値から、サーボのusの値を計算して返す　現在はclass初期化時にリストを作って参照しているため不使用
    def calcUsValue(self, coodinate = [0, 0], bitNum = 8, value = 0  ):
        print(coodinate,bitNum,value)
    """
    def text2image(self, text):
        for i in text:
            print(text)


#テストアニメーションなど======================================================================================================================================
def wave01():
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

    for i in range(3):

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



#メインプログラムはここから====================================================================================================================================
#displayのUnit配置数定義
unit_layout  = [2, 2]          #[width,height]　現在は[4,4]まで対応。増やす際は、I2Cのaddressリストとキャリブレーション用データの修正が必要。
servo_layout = [4, 4]
gray_scale_bit_size = 1

#I2C　初期化
i2c = I2C(I2C.I2C0, freq=100000, scl=34, sda=35)

#I2C 接続されているユニットのアドレス確認
addr = i2c.scan()
print( "address is :" + str(addr) )

#displayのインスタンス生成
display = mechanical_display(i2c, unit_layout, servo_layout, gray_scale_bit_size)

#flatポジションを表示する。
#display.flatPosition() #display.flatPosition()は廃止する display.setPixel(2**gray_scale_bit_size)　へ
display.setPixel(2 ** gray_scale_bit_size)
time.sleep_ms(300)
display.setPixel()

#初期化完了====================================================================================================================================================

#wave01()

#display.flatPosition()
#time.sleep_ms(2000)
#display.Release() #display.Release()は廃止display.setPixel()へ
display.setPixel()

