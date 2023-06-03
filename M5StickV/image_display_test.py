from machine import I2C
import time
import pca9685
import servo

class mechanical_display:
    def __init__(self, i2c, Layout = [1, 1]):

        self.i2c = i2c
        self.UnitLayout = Layout
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
        self.UnitIDList = []
        n = 0
        for y in range(self.UnitLayout[1]):
            list = []
            for x in range(self.UnitLayout[0]):
                print("x,y",x,y)
                list.append(n)
                n += 1
            self.UnitIDList.append(list)

        temp = []
        for i in range(len(self.UnitIDList[0])):
            list = []
            for j in self.UnitIDList:
                list.append(j[i])
            temp.append(list)
        self.UnitIDList = temp

        print("UnitIDList:",self.UnitIDList)

#Unit内のPixel位置とサーボIDの対応を定義
        self.UnitPixelIDList = [[ 0,  4,  8, 12],
                                [ 1,  5,  9, 13],
                                [ 2,  6, 10, 14],
                                [ 3,  7, 11, 15]]

#UnitIDListとUnitPixelIDListから、displayのPixelとUnitID,各ユニットのPixelIDを対応させるPixelIDListを生成する
        print("set PixelIDList")
        self.PixelIDList = []

        for x in range(self.UnitLayout[0]):
            for k in range(4):
                list = []
                for y in  range(self.UnitLayout[1]):
                    print("x,y",x,y)
                    UnitID = self.UnitIDList[x][y]
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
        for i in range(self.UnitLayout[1]):
            for j in range(self.UnitLayout[0]):
                self.pca.append(servo.Servos(self.i2c, address = self.UnitAddressList[i][j]))

# imageを表示するメソッド
    def setImage(self, img):
        print("set image")
        print(self.UnitLayout[0])
        #imgのサイズとdisplayのサイズがマッチするか確認
        if len(img) != (self.UnitLayout[0] * 4):
            print("image width unmatched")
            return
        elif len(img[1]) != (self.UnitLayout[1] * 4):
            print("image height unmatched")
            return

        #差分を確認



        #変化のあったピクセルだけを動かす
        #リリースする

        #とりあえず4bitGrayでもらって表示するだけ
        for y in range(self.UnitLayout[1]*4):
            for x in range(self.UnitLayout[0]*4):
                print("set pixel",x,y,img[x][y])
                self.pca[self.PixelIDList[x][y][0]].position(self.PixelIDList[x][y][1], us=self.us4bitGrayScalePositionList[img[x][y]][self.PixelIDList[x][y][0]][self.PixelIDList[x][y][1]])

        self.oldImage = img

# 指定ピクセルを表示するメソッド
    #Valueは3bitGrayに限る
    def setPixel(self, value, coordinate):
        x = coordinate[0]
        y = coordinate[1]
        print("set pixcel:",value,coordinate)
        self.pca[self.PixelIDList[x][y][0]].position(self.PixelIDList[x][y][1], us=self.us4bitGrayScalePositionList[value][x][y])

# 全てのパネルをセンター位置に移動する
    def flatPosition(self):
        print("flat position")
        #self.setImage(self.flatImage)

        for y in range(self.UnitLayout[1]*4):
            for x in range(self.UnitLayout[0]*4):
                self.pca[self.PixelIDList[x][y][0]].position(self.PixelIDList[x][y][1], us=self.usCenter[self.PixelIDList[x][y][0]][self.PixelIDList[x][y][1]])

# 全てのパネルを最大位置に移動する
    def maxPosition(self):
        print("max position")
        #self.setImage(self.maxImage)

        for y in range(self.UnitLayout[1]*4):
            for x in range(Layout[0]*4):
                self.pca[self.PixelIDList[x][y][0]].position(self.PixelIDList[x][y][1], us=self.usMax[self.PixelIDList[x][y][0]][self.PixelIDList[x][y][1]])

# 全てのパネルを最小位置に移動する
    def minPosition(self):
        print("min position")
        #self.setImage(self.minImage)

        for y in range(self.UnitLayout[1]*4):
            for x in range(Layout[0]*4):
                self.pca[self.PixelIDList[x][y][0]].position(self.PixelIDList[x][y][1], us=self.usMin[self.PixelIDList[x][y][0]][self.PixelIDList[x][y][1]])

# 全てのサーボをリリースするメソッド
    def Release(self, coordinate = 0):
        #全てのサーボをリリース
        if coordinate == 0:
            print("all servo release")
            for y in range(self.UnitLayout[1]*4):
                for x in range(Layout[0]*4):
                    self.pca[self.PixelIDList[x][y][0]].release(self.PixelIDList[x][y][1])
        else:
            try:
                x = coordinate[0]
                y = coordinate[1]
                self.pca[self.PixelIDList[x][y][0]].release(self.PixelIDList[x][y][1])

            except:
                print("image size unmatched")


# ピクセル座標と色調（bit数）と値から、サーボのusの値を計算して返す
    def calcUsValue(self, coodinate = [0, 0], bitNum = 8, value = 0  ):
        print(coodinate,bitNum,value)


#displayのUnit配置数定義
Layout = [2,2]          #[width,height]　現在は[4,4]まで対応。増やす際は、I2Cのaddressリストも修正が必要。

#I2C　初期化
i2c = I2C(I2C.I2C0, freq=100000, scl=34, sda=35)

#I2C 接続されているユニットのアドレス確認
addr = i2c.scan()
print( "address is :" + str(addr) )

#displayのインスタンス生成
display = mechanical_display(i2c,Layout)

#flatポジションを表示する。
display.flatPosition()
time.sleep_ms(300)

"""
#PCA9685のインスタンスに直接指示を投げることもできる
for y in range(display.UnitLayout[1]*4):
    for x in range(display.UnitLayout[0]*4):
        display.pca[display.PixelIDList[x][y][0]].position(display.PixelIDList[x][y][1], us=display.usMax[display.PixelIDList[x][y][0]][display.PixelIDList[x][y][1]])
        time.sleep_ms(50)
        display.pca[display.PixelIDList[x][y][0]].position(display.PixelIDList[x][y][1], us=display.usCenter[display.PixelIDList[x][y][0]][display.PixelIDList[x][y][1]])
        time.sleep_ms(50)
        display.pca[display.PixelIDList[x][y][0]].release(display.PixelIDList[x][y][1])

for x in range(display.UnitLayout[0]*4):
    for y in range(display.UnitLayout[1]*4):
        display.pca[display.PixelIDList[x][y][0]].position(display.PixelIDList[x][y][1], us=display.usMin[display.PixelIDList[x][y][0]][display.PixelIDList[x][y][1]])
        time.sleep_ms(100)
        display.pca[display.PixelIDList[x][y][0]].position(display.PixelIDList[x][y][1], us=display.usCenter[display.PixelIDList[x][y][0]][display.PixelIDList[x][y][1]])
        time.sleep_ms(50)
        display.pca[display.PixelIDList[x][y][0]].release(display.PixelIDList[x][y][1])


for y in range(Layout[1] * 4):
    for x in range(Layout[0] * 4):
        display.setPixel(15,[x,y])
        time.sleep_ms(100)
        display.setPixel(16,[x,y])

for x in range(Layout[0] * 4):
    for y in range(Layout[1] * 4):
        display.setPixel(15,[x,y])
        time.sleep_ms(100)
        display.setPixel(16,[x,y])
"""

print("use method")



#display.flatPosition()
#time.sleep_ms(300)
#display.maxPosition()
#time.sleep_ms(1000)
#display.minPosition()
#time.sleep_ms(300)
#display.minPosition()
#display.Release()

"""
print("pixel control")
display.setPixel(0,[0,0])
time.sleep_ms(100)
display.setPixel(1,[0,0])
time.sleep_ms(100)
display.setPixel(2,[0,0])
time.sleep_ms(100)
display.setPixel(3,[0,0])
time.sleep_ms(100)
display.setPixel(4,[0,0])
time.sleep_ms(100)
display.setPixel(5,[0,0])
time.sleep_ms(100)
display.setPixel(6,[0,0])
time.sleep_ms(100)
display.setPixel(7,[0,0])
time.sleep_ms(100)
display.setPixel(8,[0,0])
time.sleep_ms(100)
display.setPixel(9,[0,0])
time.sleep_ms(100)
display.setPixel(10,[0,0])
time.sleep_ms(100)
display.setPixel(11,[0,0])
time.sleep_ms(100)
display.setPixel(12,[0,0])
time.sleep_ms(100)
display.setPixel(13,[0,0])
time.sleep_ms(100)
display.setPixel(14,[0,0])
time.sleep_ms(100)
display.setPixel(15,[0,0])
time.sleep_ms(100)
display.setPixel(16,[0,0])
time.sleep_ms(100)
display.Release([0,0])
"""

"""
image = [[ 0, 1, 2, 3, 4, 5, 6, 7],
         [ 1, 2, 3, 4, 5, 6, 7, 8],
         [ 2, 3, 4, 5, 6, 7, 8, 9],
         [ 3, 4, 5, 6, 7, 8, 9,10],
         [ 4, 5, 6, 7, 8, 9,10,11],
         [ 5, 6, 7, 8, 9,10,11,12],
         [ 6, 7, 8, 9,10,11,12,13],
         [ 7, 8, 9,10,11,12,13,14]]
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














#display.flatPosition()
#time.sleep_ms(2000)
display.Release()

