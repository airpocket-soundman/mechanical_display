from machine import I2C
import time
import pca9685
import servo
import font
import ds3231

from Maix import GPIO
#from fpioa_manager import fm, board_info
#import lcd
#import sensor

class mechanical_display:
    def __init__(self, i2c0, i2c1, unit_layout = [1, 1],servo_layout = [4, 4], gray_scale_bit_value = 4):

        #self.i2c0 = i2c0

        self.unit_layout = unit_layout
        self.servo_layout = servo_layout
        self.gray_scale_bit_value = gray_scale_bit_value
        self.gray_scale_level = 2 ** gray_scale_bit_value
        self.pixel_layout = [self.unit_layout[0] * self.servo_layout[0], self.unit_layout[1] * self.servo_layout[1]]
#UnitのI2C addressのリスト定義
        self.unit_address_list = [[64, 65, 66, 67],
                                  [68, 69, 70, 71],
                                  [72, 73, 74, 75],
                                  [76, 77, 78, 79]]

#UnitのI2C BUSのリスト定義
        self.unit_I2C_BUS_list = [[i2c0, i2c0, i2c0, i2c0],
                                  [i2c0, i2c0, i2c0, i2c0],
                                  [i2c1, i2c1, i2c1, i2c1],
                                  [i2c1, i2c1, i2c1, i2c1]]


#UnitのIDのリスト定義
        print("set unit_ID_list")
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
        self.unit_pixel_ID_list = [[ 0,  4,  8, 12],
                                   [ 1,  5,  9, 13],
                                   [ 2,  6, 10, 14],
                                   [ 3,  7, 11, 15]]

#unit_ID_listとunit_pixel_ID_listから、displayのPixelとunit_ID,各ユニットのPixelIDを対応させるpixel_ID_listを生成する
        print("set pixel_ID_list")
        self.pixel_ID_list = []

        for x in range(self.unit_layout[0]):
            for k in range(self.servo_layout[0]):
                list = []
                for y in  range(self.unit_layout[1]):
                    unit_ID = self.unit_ID_list[x][y]
                    for l in range(self.servo_layout[1]):
                        list.append([unit_ID,self.unit_pixel_ID_list[k][l]])

                self.pixel_ID_list.append(list)

        #生成されたpixel_ID_listを確認
#        print("pixel_ID_list:")
#        for i in range(len(self.pixel_ID_list)):
#            time.sleep_ms(10)
#            print(self.pixel_ID_list[i])

# サーボのキャリブレーションデータ 4*4ユニット対応版
#       データ配列[ユニットのy座標][ユニットのx座標][サーボID]

        self.us_center= [[[1550, 1480, 1430, 1450,  1650, 1530, 1460, 1440,  1430, 1410, 1560, 1440,  1440, 1420, 1430, 1550],
                          [1480, 1600, 1500, 1660,  1530, 1490, 1620, 1430,  1530, 1470, 1500, 1410,  1560, 1520, 1540, 1660],
                          [1390, 1450, 1410, 1450,  1550, 1500, 1500, 1420,  1400, 1500, 1400, 1550,  1450, 1600, 1440, 1500],
                          [1590, 1620, 1710, 1660,  1680, 1640, 1680, 1490,  1520, 1550, 1670, 1680,  1630, 1690, 1600, 1600]],

                         [[1420, 1550, 1570, 1510,  1500, 1640, 1480, 1580,  1550, 1680, 1515, 1420,  1550, 1590, 1515, 1550],
                          [1560, 1680, 1500, 1420,  1590, 1420, 1500, 1370,  1540, 1470, 1470, 1530,  1485, 1500, 1650, 1490],
                          [1500, 1540, 1650, 1600,  1460, 1600, 1660, 1620,  1600, 1530, 1450, 1560,  1540, 1620, 1650, 1500],
                          [1640, 1690, 1610, 1690,  1650, 1530, 1640, 1670,  1650, 1640, 1720, 1690,  1600, 1650, 1560, 1620]],

                         [[1510, 1640, 1600, 1680,  1580, 1630, 1640, 1500,  1490, 1530, 1630, 1590,  1540, 1530, 1610, 1640],
                          [1540, 1560, 1640, 1640,  1600, 1620, 1510, 1710,  1690, 1500, 1480, 1480,  1600, 1600, 1610, 1680],
                          [1640, 1610, 1720, 1650,  1610, 1560, 1490, 1750,  1510, 1620, 1610, 1670,  1530, 1510, 1670, 1620],
                          [1530, 1510, 1590, 1400,  1380, 1510, 1380, 1520,  1560, 1620, 1540, 1460,  1540, 1540, 1630, 1460]],

                         [[1580, 1550, 1490, 1550,  1560, 1580, 1580, 1580,  1590, 1550, 1620, 1540,  1400, 1470, 1540, 1490],
                          [1520, 1600, 1690, 1630,  1630, 1610, 1620, 1550,  1650, 1560, 1710, 1510,  1680, 1770, 1660, 1600],
                          [1580, 1490, 1590, 1510,  1560, 1640, 1520, 1380,  1460, 1640, 1540, 1650,  1570, 1580, 1530, 1530],
                          [1570, 1590, 1590, 1550,  1580, 1430, 1480, 1550,  1490, 1610, 1550, 1620,  1430, 1500, 1530, 1680]]]

        self.us_max   = [[[2020, 1880, 1800, 1840,  2120, 1960, 1850, 1830,  1890, 1860, 1980, 1840,  1900, 1840, 1830, 1930],
                          [1830, 1940, 1840, 1970,  1890, 1870, 1920, 1770,  1870, 1850, 1860, 1770,  1900, 1870, 1910, 1990],
                          [1780, 1800, 1780, 1860,  1910, 1860, 1900, 1830,  1760, 1850, 1790, 1940,  1820, 1930, 1830, 1870],
                          [2020, 2050, 2110, 2100,  2120, 2060, 2070, 1910,  1980, 1960, 2080, 2060,  2120, 2160, 1990, 2000]],

                         [[1910, 1960, 1950, 1920,  1980, 2060, 1870, 1990,  2030, 2060, 1890, 1860,  1980, 2020, 1930, 1960],
                          [1980, 2020, 1870, 1800,  1960, 1820, 1880, 1740,  1930, 1890, 1900, 1900,  1880, 1900, 2000, 1860],
                          [1880, 1940, 2090, 1970,  1850, 1940, 2060, 1980,  1980, 1900, 1840, 1930,  1900, 1950, 2060, 1880],
                          [2130, 2120, 2020, 2050,  2100, 2100, 2030, 2070,  2100, 2100, 2080, 2050,  2100, 2100, 1960, 2010]],

                         [[1900, 2020, 2020, 2080,  2000, 2030, 2040, 1950,  1880, 1970, 2000, 1970,  1980, 1990, 2070, 2000],
                          [1970, 1990, 2100, 2080,  2020, 2030, 1970, 2160,  2060, 1980, 1920, 1910,  2040, 2060, 2020, 2120],
                          [2060, 1940, 2120, 2010,  1980, 2000, 1900, 2100,  1960, 2000, 2000, 2070,  1960, 1890, 2040, 1990],
                          [1930, 1940, 1950, 1770,  1830, 1940, 1780, 1920,  1960, 2010, 1930, 1800,  1960, 1960, 1990, 1840]],

                         [[1960, 1950, 1850, 1930,  1950, 1920, 1950, 1920,  1940, 1900, 2000, 1930,  1760, 1880, 1880, 1920],
                          [1980, 1980, 2120, 2030,  2080, 2020, 2090, 2020,  2080, 2010, 2140, 1930,  2070, 2170, 2070, 2050],
                          [1980, 1830, 1960, 1890,  1900, 2000, 1890, 1780,  1820, 2010, 1910, 2040,  1970, 1930, 1910, 1910],
                          [2000, 2020, 1950, 1900,  1950, 1860, 1870, 1890,  1880, 1970, 1940, 1990,  1880, 1880, 1940, 2040]]]


        self.us_min   = [[[1180, 1080, 1060, 1080,  1290, 1130, 1050, 1030,  1080, 1010, 1220, 1020,  1080, 1000, 1030, 1100],
                          [1050, 1170, 1120, 1200,  1100, 1030, 1240, 1010,  1140, 1000, 1110,  980,  1220, 1110, 1180, 1170],
                          [1000, 1070, 1040, 1050,  1190, 1120, 1110, 1000,  1030, 1130, 1000, 1160,  1080, 1250, 1070, 1150],
                          [1170, 1160, 1320, 1240,  1250, 1230, 1300, 1100,  1070, 1200, 1250, 1280,  1200, 1280, 1200, 1180]],

                         [[1050, 1100, 1190, 1080,  1180, 1230, 1100, 1190,  1190, 1260, 1140,  970,  1200, 1100, 1120, 1100],
                          [1200, 1280, 1150, 1040,  1220, 1050, 1170, 1000,  1180, 1070, 1120, 1140,  1150, 1130, 1290, 1130],
                          [1120, 1180, 1270, 1180,  1110, 1250, 1320, 1260,  1250, 1180, 1080, 1190,  1210, 1230, 1320, 1110],
                          [1190, 1330, 1240, 1330,  1230, 1110, 1270, 1280,  1210, 1260, 1370, 1300,  1210, 1260, 1210, 1240]],

                         [[1150, 1230, 1180, 1240,  1200, 1210, 1220, 1060,  1130, 1100, 1260, 1180,  1180, 1100, 1210, 1260],
                          [1150, 1100, 1240, 1260,  1240, 1200, 1130, 1280,  1320, 1180, 1140, 1080,  1240, 1240, 1280, 1310],
                          [1250, 1250, 1390, 1260,  1280, 1120, 1150, 1370,  1140, 1270, 1270, 1310,  1190, 1170, 1270, 1330],
                          [1180, 1120, 1240, 1020,  1000, 1140, 1020, 1170,  1180, 1260, 1200, 1100,  1200, 1190, 1270, 1130]],

                         [[1240, 1140, 1150, 1170,  1200, 1140, 1260, 1240,  1250, 1160, 1260, 1140,  1080, 1040, 1210, 1120],
                          [1140, 1230, 1340, 1280,  1260, 1220, 1260, 1190,  1280, 1180, 1360, 1180,  1360, 1380, 1290, 1260],
                          [1260, 1150, 1220, 1180,  1260, 1280, 1170, 1070,  1120, 1280, 1190, 1310,  1250, 1200, 1170, 1200],
                          [1240, 1260, 1240, 1220,  1240, 1030, 1170, 1220,  1140, 1270, 1220, 1280,  1110, 1160, 1200, 1310]]]

        #4x4ユニットのキャリブレーションデータのうち、使用しているユニットのデータのみ抽出。
        list = []
        for y in range(unit_layout[1]):
            for x in range(unit_layout[0]):
                list.append(self.us_center[y][x])
        self.us_center = list
        list = []
        for y in range(unit_layout[1]):
            for x in range(unit_layout[0]):
                list.append(self.us_max[y][x])
        self.us_max = list
        list = []
        for y in range(unit_layout[1]):
            for x in range(unit_layout[0]):
                list.append(self.us_min[y][x])
        self.us_min = list

#サーボドライバ初期化
        self.pca = []
        for i in range(self.unit_layout[1]):
            for j in range(self.unit_layout[0]):
                self.pca.append(servo.Servos(self.unit_I2C_BUS_list[i][j], address = self.unit_address_list[i][j]))

# 初期配置としてflat状態を表示
        self.old_image = []
        print("old_image")
        for x in range(self.pixel_layout[0]):
            list = []
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
                    self.pca[self.pixel_ID_list[x][y][0]].release(self.pixel_ID_list[x][y][1])
                else:
                    #print(x,y,value)
                    usValue = self.usValue([x, y], value)
                    self.pca[self.pixel_ID_list[x][y][0]].position(self.pixel_ID_list[x][y][1], us=usValue)
                    self.old_image[x][y] = value

# ピクセル座標と色調（bit数）と値から、サーボのusの値を計算して返す
    def usValue(self, coordinate = [0, 0], gray_scale_color = 0):
        x = coordinate[0]
        y = coordinate[1]
#        print(x,y)
#        print(self.pixel_ID_list[x])
#        time.sleep_ms(50)
        unit_ID  = self.pixel_ID_list[x][y][0]
        servo_ID = self.pixel_ID_list[x][y][1]
        us_center = self.us_center[unit_ID][servo_ID]
        us_max = self.us_max[unit_ID][servo_ID]
        us_min = self.us_min[unit_ID][servo_ID]
        gray_scale_level = 2 ** self.gray_scale_bit_value

        if gray_scale_color < (gray_scale_level / 2):
            us = int(us_min + (((us_center - us_min) / (gray_scale_level - 1)) * gray_scale_color * 2))
        elif gray_scale_color == gray_scale_level:
            us = us_center
        else:
            us = int(us_max - (((us_max - us_center) / (gray_scale_level - 1)) * (gray_scale_level - 1 - gray_scale_color) * 2))

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

# color で受け取った色のグレースケールimageを作る
    def bg_image_generate(self, color = 0):
        bg_image =[]
        for x in range(self.pixel_layout[0]):
            list = []
            for y in range(self.pixel_layout[1]):
                list.append(color)
            bg_image.append(list)
        return bg_image

# bg_imageにtext_imageを合成する
    def textOverlay(self, bg_image, text_image ,offset = [0,0], text_color = None, transparent = True):
        if text_color == None:
            text_color = self.gray_scale_color -1
        text_size = [len(text_image), len(text_image[0])]

        image = bg_image

        for y in range(text_size[1]):
            if y + offset[1] < self.pixel_layout[1] and y + offset[1] >= 0:
                for x in range(text_size[0]):
                    if x + offset[0] < self.pixel_layout[0] and x + offset[0] >= 0:
                        if transparent == False:
                            image[x + offset[0]][y + offset[1]] = text_image[x][y] * text_color
                        else:
                            print(x,y,text_image[x][y])
                            if text_image[x][y] == 1:
                                image[x + offset[0]][y + offset[1]] = text_image[x][y] * text_color
        print(image)
        return image

#コマ間を補完するメソッド
    def interpolation(self, start_image, finish_image, frame_number):
        if len(start_image) != len(finish_image) or len(start_image[0]) != len(finish_image[0]):
            print("image1 & image2 size unmatched")
            return

        film = []
        for i in range(frame_number):
            frame = []
            for x in range(len(start_image)):
                list = []
                for y in range(len(start_image[1])):
                    list.append[int(start_image[x][y] + ((finish_image[x][y] - start_image[x][y]) / frame_number))]
                frame.append(list)
            film.append(frame)
        return film

    def invert_color(self, image):
        for x in range(len(image)):
            for y in range(len(image[0])):
                if image[x][y] != self.gray_scale_level:
                    image[x][y] = self.gray_scale_level - image[x][y] - 1
        return image


#=======================================================================================================================


#displayのUnit配置数定義
unit_layout  = [4, 4]          #[width,height]　現在は[4,4]まで対応。増やす際は、I2Cのaddressリストも修正が必要。
servo_layout = [4, 4]
pixel_layout = [unit_layout[0] * servo_layout[0], unit_layout[1] * servo_layout[1]]
gray_scale_bit_value = 8
gray_scale_level = 2**gray_scale_bit_value



#I2C　初期化
i2c0 = I2C(I2C.I2C0, freq=100000, scl=34, sda=35)
i2c1 = I2C(I2C.I2C1, freq=100000, scl=32, sda=33)

#I2C 接続されているユニットのアドレス確認
addr0 = i2c0.scan()
addr1 = i2c1.scan()
print("address is :" + str(addr0))
print("address is :" + str(addr1))
#displayのインスタンス生成
display = mechanical_display(i2c0, i2c1, unit_layout, servo_layout, gray_scale_bit_value)

#5Pフォントのインスタンス生成
Font = font.font_5P()

#flatポジションを表示する。
display.flatPosition()
time.sleep_ms(300)



#=====================================================================================================
#RTCのインスタンスを生成
ds = ds3231.DS3231(i2c1)

"""
#RTCの時間設定
year    = 2023 # Can be yyyy or yy format
month   = 7
mday    = 4
hour    = 15 # 24 hour format only
minute  = 28
second  = 30 # Optional
weekday = 2 # Optional

datetime = (year, month, mday, hour, minute, second, weekday)
ds.datetime(datetime)
print(ds.datetime())
"""

#現在時刻をRTCから読み取って表示
year    = ds.datetime()[0]
month   = ds.datetime()[1]
day     = ds.datetime()[2]
hour    = ds.datetime()[4]
minute  = ds.datetime()[5]
second  = ds.datetime()[6]
print(year, month, day, hour, minute, second)


def sec_display():
    while True:
        second  = ds.datetime()[6]
        image = Font.genTextImage(text = '{:02}'.format(second),font = "number3x5p")
        print('{:02}'.format(second))
        clock_image
        clock_image = display.textOverlay(image, offset = [0,10], text_color = 255, bg_color = 0, transparent = True)

        display.setImage(clock_image)
        time.sleep_ms(10)

#=====================================================================================================

# テキスト表示テスト


# テキストイメージ表示
text_image = Font.genTextImage(text = "3",font = "propotional")
bg_image = display.bg_image_generate(200)
image = display.textOverlay(bg_image, text_image, offset = [0,0],text_color = 50, transparent = True)
display.setImage(image)
time.sleep_ms(1000)

text_image = Font.genTextImage(text = "2",font = "propotional")
bg_image = display.bg_image_generate(200)
image = display.textOverlay(bg_image, text_image, offset = [0,0],text_color = 50, transparent = True)
display.setImage(image)
time.sleep_ms(1000)

text_image = Font.genTextImage(text = "1",font = "propotional")
bg_image = display.bg_image_generate(200)
image = display.textOverlay(bg_image, text_image, offset = [0,0],text_color = 50, transparent = True)
display.setImage(image)
time.sleep_ms(1000)

text_image = Font.genTextImage(text = " ",font = "propotional")
bg_image = display.bg_image_generate(200)
image = display.textOverlay(bg_image, text_image, offset = [0,0],text_color = 50, transparent = True)
display.setImage(image)
time.sleep_ms(1000)

#"""
# テキストイメージスクロール表示 Mouser
#time.sleep_ms(5000)
base_color = 50
text_color = 200

ss = 1
ds = 0

mouser_logo_image = [[ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                     [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                     [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                     [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                     [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                     [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                     [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                     [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                     [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                     [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                     [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                     [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                     [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                     [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                     [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                     [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                     [ss,ds,ds,ds, ds,ds,ds,ds, ds,ds,ds,ds, ds,ds,ds,ss],
                     [ds,ds,ds,ds, ds,ds,ds,ds, ds,ds,ds,ds, ds,ds,ds,ds],
                     [ds,ds,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ds,ds],
                     [ds,ds,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ds,ds],
                     [ds,ds,ss,ss, ss,ss,ss,ds, ds,ds,ds,ds, ds,ds,ds,ds],
                     [ds,ds,ds,ds, ds,ss,ss,ss, ss,ss,ds,ds, ds,ds,ds,ds],
                     [ds,ds,ds,ds, ds,ds,ds,ss, ss,ss,ss,ss, ds,ds,ds,ds],
                     [ds,ds,ds,ds, ds,ds,ds,ds, ds,ds,ss,ss, ss,ss,ds,ds],
                     [ds,ds,ds,ds, ds,ds,ds,ds, ds,ds,ss,ss, ss,ss,ds,ds],
                     [ds,ds,ds,ds, ds,ds,ds,ss, ss,ss,ss,ss, ds,ds,ds,ds],
                     [ds,ds,ds,ds, ds,ss,ss,ss, ss,ss,ds,ds, ds,ds,ds,ds],
                     [ds,ds,ss,ss, ss,ss,ss,ds, ds,ds,ds,ds, ds,ds,ds,ds],
                     [ds,ds,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ds,ds],
                     [ds,ds,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ds,ds],
                     [ds,ds,ds,ds, ds,ds,ds,ds, ds,ds,ds,ds, ds,ds,ds,ds],
                     [ss,ds,ds,ds, ds,ds,ds,ds, ds,ds,ds,ds, ds,ds,ds,ss]]


# for mouser

stop_counter = 16
counter = 0
bg_image = display.bg_image_generate(base_color)
for x in range(len(mouser_logo_image)):
    if counter == stop_counter:
        time.sleep_ms(2000)
    image = display.textOverlay(bg_image, mouser_logo_image, offset = [-x, 0], text_color = text_color, transparent = True)
    display.setImage(image)
    counter += 1

time.sleep_ms(1000)

text_image = Font.genTextImage(text = "        MOUSER MAKE AWARDS 2023    Mechanical Display",font = "propotional")
bg_image = display.bg_image_generate(base_color)
print(text_image)
for x in range(len(text_image)):
    image = display.textOverlay(bg_image, text_image, offset = [-x, 2], text_color = text_color, transparent = True)
#    print("image", x)
    display.setImage(image)
    time.sleep_ms(200)

time.sleep_ms(200)

text_image = Font.genTextImage(text = "        This is The True Color Display!! :-)",font = "propotional")
bg_image = display.bg_image_generate(base_color)
print(text_image)
for x in range(len(text_image)):
    image = display.textOverlay(bg_image, text_image, offset = [-x, 9], text_color = text_color, transparent = True)
#    print("image", x)
    display.setImage(image)
    time.sleep_ms(200)

time.sleep_ms(5000)

# for snacks

text_image = Font.genTextImage(text = "        SNACKS Vol.5 (>_0)    Mechanical Display",font = "propotional")
bg_image = display.bg_image_generate(base_color)
print(text_image)
for x in range(len(text_image)):
    image = display.textOverlay(bg_image, text_image, offset = [-x, 2], text_color = text_color, transparent = True)
#    print("image", x)
    display.setImage(image)
    time.sleep_ms(200)

time.sleep_ms(200)

text_image = Font.genTextImage(text = "        This is The True Color Display!! :-)",font = "propotional")
bg_image = display.bg_image_generate(base_color)
print(text_image)
for x in range(len(text_image)):
    image = display.textOverlay(bg_image, text_image, offset = [-x, 9], text_color = text_color, transparent = True)
#    print("image", x)
    display.setImage(image)
    time.sleep_ms(200)

time.sleep_ms(5000)

# for hackaday

text_image = Font.genTextImage(text = "        Hackaday Prize 2023   Mechanical Display",font = "propotional")
bg_image = display.bg_image_generate(base_color)
print(text_image)
for x in range(len(text_image)):
    image = display.textOverlay(bg_image, text_image, offset = [-x, 2], text_color = text_color, transparent = True)
#    print("image", x)
    display.setImage(image)
    time.sleep_ms(200)

time.sleep_ms(200)

text_image = Font.genTextImage(text = "        This is The True Color Display!! :-)",font = "propotional")
bg_image = display.bg_image_generate(base_color)
print(text_image)
for x in range(len(text_image)):
    image = display.textOverlay(bg_image, text_image, offset = [-x, 9], text_color = text_color, transparent = True)
#    print("image", x)
    display.setImage(image)
    time.sleep_ms(200)


time.sleep_ms(5000)

# sunset & daskey

text_image = Font.genTextImage(text = "        Sunset & Duskey",font = "propotional")
bg_image = display.bg_image_generate(base_color)
print(text_image)
for x in range(len(text_image)):
    image = display.textOverlay(bg_image, text_image, offset = [-x, 9], text_color = text_color, transparent = True)
#    print("image", x)
    display.setImage(image)
    time.sleep_ms(200)

time.sleep_ms(5000)

# sunset & night sky

text_image = Font.genTextImage(text = "        Sunset & Night Sky",font = "propotional")
bg_image = display.bg_image_generate(base_color)
print(text_image)
for x in range(len(text_image)):
    image = display.textOverlay(bg_image, text_image, offset = [-x, 10], text_color = text_color, transparent = True)
#    print("image", x)
    display.setImage(image)
    time.sleep_ms(200)

time.sleep_ms(5000)


# sky blue & forest green

text_image = Font.genTextImage(text = "        Sky Blue & Forest Green",font = "propotional")
bg_image = display.bg_image_generate(base_color)
print(text_image)
for x in range(len(text_image)):
    image = display.textOverlay(bg_image, text_image, offset = [-x, 2], text_color = text_color, transparent = True)
#    print("image", x)
    display.setImage(image)
    time.sleep_ms(200)

time.sleep_ms(5000)

#color flash

for y in range(pixel_layout[1]):
    for x in range(pixel_layout[0]):
        display.setPixel([x, y],base_color)
    time.sleep_ms(100)

time.sleep_ms(5000)

for y in range(pixel_layout[1]):
    for x in range(pixel_layout[0]):
        display.setPixel([x, y],text_color)
    time.sleep_ms(100)



#display.flatPosition()
time.sleep_ms(1000)
#sec_display()

display.release()
