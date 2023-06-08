from machine import I2C
import time
import pca9685
import servo
import font

from Maix import GPIO
rom fpioa_manager import fm, board_info
import lcd
import sensor

class mechanical_display:
    def __init__(self, i2c, unit_layout = [1, 1],servo_layout = [4, 4], gray_scale_bit_value = 4):

        self.i2c = i2c
        self.unit_layout = unit_layout
        self.servo_layout = servo_layout
        self.gray_scale_bit_value = gray_scale_bit_value
        self.gray_scale_level = 2 ** gray_scale_bit_value
        self.pixel_layout = [self.unit_layout[0] * self.servo_layout[0], self.unit_layout[1] * self.servo_layout[1]]
#UnitのI2C addressのリスト定義
        self.UnitAddressList = [[64, 65, 66, 67],
                                [68, 69, 70, 71],
                                [72, 73, 74, 75],
                                [76, 77, 78, 79]]

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
            for k in range(self.servo_layout[0]):
                list = []
                for y in  range(self.unit_layout[1]):
                    print("x,y",x,y)
                    UnitID = self.unit_ID_list[x][y]
                    print("UnitID", UnitID)
                    print(self.UnitPixelIDList)
                    for l in range(self.servo_layout[1]):
                        list.append([UnitID,self.UnitPixelIDList[k][l]])

                self.PixelIDList.append(list)

        #生成されたPixelIDListを確認
        print("PixelIDList:")
        for i in range(len(self.PixelIDList)):
            time.sleep_ms(10)
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

#サーボドライバ初期化
        self.pca = []
        for i in range(self.unit_layout[1]):
            for j in range(self.unit_layout[0]):
                self.pca.append(servo.Servos(self.i2c, address = self.UnitAddressList[i][j]))

# 初期配置としてflat状態を表示
        self.old_image = []
        print("old_image")
        for x in range(self.pixel_layout[0]):
            listb = []
            for y in range(self.pixel_layout[1]):
                list.append(self.gray_scale_level)
            self.old_image.append(list)

        self.setImage(self.old_image)

# imageを表示する（差分表示作成中
    def setImage(self, img):
        #imgのサイズとdisplayのサイズがマッチするか確認
        if len(img) != (self.pixel_layout[0]):
            print("image width unmatched", len(img))
            return
        elif len(img[0]) != (self.pixel_layout[1]):
            print("image height unmatched", len(img[0]))
            return

        #書き換えるイメージの差分のみ書き換える
        for y in range(self.pixel_layout[1]):
            for x in range(self.pixel_layout[0]):
                if img[x][y] != self.old_image[x][y]:
                    self.setPixel([x,y],img[x][y])

# 単ピクセルを表示する 座標指定なしの場合、全ピクセル。色指定なしの場合release

    def setPixel(self, coordinate = None, value = None):

        #指定座標がレンジ外の場合の処理
        if coordinate != None:
            if int(coordinate[0]) > int(self.pixel_layout[0]):
                print("x is out of range", x)
                return
            if int(coordinate[1]) > int(self.pixel_layout[1]):
                print("y is out of range", y)
                return

        #座標が未入力の場合、全ピクセル範囲を指定
        if coordinate == None:
            x1 = 0
            x2 = self.pixel_layout[0]
            y1 = 0
            y2 = self.pixel_layout[1]

        #座標入力が有る場合は指定ピクセルのみをrange()指定
        else:
            x1 = coordinate[0]
            x2 = coordinate[0] + 1
            y1 = coordinate[1]
            y2 = coordinate[1] + 1

        #print("x1,x2,y1,y2",x1,x2,y1,y2)

        for y in range(y1, y2, 1):
            for x in range(x1, x2, 1):
                if value == None:
                    self.pca[self.PixelIDList[x][y][0]].release(self.PixelIDList[x][y][1])
                else:
                    usValue = self.usValue([x, y], value)
                    self.pca[self.PixelIDList[x][y][0]].position(self.PixelIDList[x][y][1], us=usValue)
                    self.old_image[x][y] = value

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
        self.setPixel(value = gray_scale_level)

# 全てのパネルを最大位置に移動する
    def maxPosition(self):
        print("max position")
        self.setPixel(value = self.gray_scale_level - 1)

# 全てのパネルを最小位置に移動する
    def minPosition(self):
        print("min position")
        self.setPixel(value = 0)

# 全てのサーボをリリースするメソッド
    def release(self, coordinates = None):
        #全てのサーボをリリース
        if coordinates == None:
            print("all servo release")
            self.setPixel()

        else:
            self.setPixel(coordinate = coordinates)

    def textOverlay(self, text_image ,offset = [0,0], text_color = None, bg_color = 0, transparent = True):
        if text_color == None:
            text_color = self.gray_scale_color -1
        text_size = [len(text_image), len(text_image[0])]

        image = []

        for x in range(self.pixel_layout[0]):
            list = []
            for y in range(self.pixel_layout[1]):
                list.append(bg_color)
            image.append(list)

        for y in range(text_size[1]):
            if y + offset[1] < self.pixel_layout[1] and y + offset[1] >= 0:
                for x in range(text_size[0]):
                    if x + offset[0] < self.pixel_layout[0] and x + offset[0] >= 0:
                        if transparent == False:
                            image[x + offset[0]][y + offset[1]] = text_image[x][y] * text_color
                        else:
                            if text_image[x][y] == 1:
#                                print("text overlay image size", len(image),len(image[0]),x,y)
#                                print("check",image[x + offset[0]][y + offset[1]])
                                image[x + offset[0]][y + offset[1]] = text_image[x][y] * text_color
#        print(len(image),len(image[0]))
        return image

#=======================================================================================================================

#ボタン設定
fm.register(board_info.BUTTON_A, fm.fpioa.GPIO1)
button_a = GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP)
fm.register(board_info.BUTTON_B, fm.fpioa.GPIO2)
button_b = GPIO(GPIO.GPIO2, GPIO.IN, GPIO.PULL_UP)


#LCD設定
lcd.init(freq=15000000)
lcd.direction(lcd.YX_LRDU)

#カメラ設定
sensor.reset()                      # Reset and initialize the sensor. It will
                                    # run automatically, call sensor.run(0) to stop
sensor.set_pixformat(sensor.GRAYSCALE) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)   # Set frame size to QVGA (320x240) QQVGA (160x120)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
sensor.set_contrast(+2)             # Contrast +2 to -2
#sensor.set_brightness(-2)           # Brightness +2 to -2
#sensor.set_saturation(-2)           # Saturation +2 to -2
sensor.set_auto_gain(0,20)           # enable,gain_db enable=1:auto,0:off
#sensor.set_vflip(1)                 # 1:enable 0:disable
sensor.set_hmirror(1)                 # 1:enable 0:disable




#displayのUnit配置数定義
unit_layout  = [2, 1]          #[width,height]　現在は[4,4]まで対応。増やす際は、I2Cのaddressリストも修正が必要。
servo_layout = [4, 4]
pixel_layout = [unit_layout[0] * servo_layout[0], unit_layout[1] * servo_layout[1]]
gray_scale_bit_value = 8
gray_scale_level = 2**gray_scale_bit_value

#I2C　初期化
i2c = I2C(I2C.I2C0, freq=100000, scl=34, sda=35)

#I2C 接続されているユニットのアドレス確認
addr = i2c.scan()
print( "address is :" + str(addr) )

#displayのインスタンス生成
display = mechanical_display(i2c, unit_layout, servo_layout, gray_scale_bit_value)

#5Pフォントのインスタンス生成
Font = font.font_5P()

#flatポジションを表示する。
display.flatPosition()
time.sleep_ms(300)


#=====================================================================================================

# テキスト表示テスト

"""
# テキストイメージ表示
text_image = Font.genTextImage(text = "A",monospace = False)
image = display.textOverlay(text_image,offset = [0,0],text_color = 255, bg_color = 0, transparent = True)
display.setImage(image)
time.sleep_ms(2000)


# テキストイメージはみだし有り表示
text_image = Font.genTextImage(text = "AB",monospace = False)
image = display.textOverlay(text_image,offset = [0,0],text_color = 255, bg_color = 0, transparent = True)
display.setImage(image)
time.sleep_ms(2000)
"""
# テキストイメージスクロール表示

text_image = Font.genTextImage(text = "    hallo",monospace = False)
for x in range(len(text_image)):
    image = display.textOverlay(text_image, offset = [-x, 0], text_color = 200, bg_color = 55, transparent = True)
    print("image", x)
    for i in range(len(image)):
        print(image[i])
    display.setImage(image)
    time.sleep_ms(300)



# 4bit wave表示
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
"""

# カメラ画像表示
while True:
    if button_a.value() == 1:
        break
    
    camera_image = sensor.snapshot()         # Take a picture and return the image.
    camera_image = camera_image.copy((20,0,140,120))
    camera_image = camera_image.resize(8,8)
    for i in range(len(image)):
        print(image[i])
    display.setImage(image)
    time.sleep_ms(300)


display.flatPosition()
time.sleep_ms(1000)
display.release()

