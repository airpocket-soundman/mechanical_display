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

#UnitのIDのリスト定義
        self.UnitIDList = []
        n = 0
        for i in range(self.UnitLayout[0]):
            list=[]
            for j in range(self.UnitLayout[1]):
                list.append(n)
                n += 1
            self.UnitIDList.append(list)
        print("UnitIDList:",self.UnitIDList)

#Unit内のPixel位置とサーボIDの対応を定義
        self.UnitPixelIDList = [[ 0,  1,  2,  3],
                                [ 4,  5,  6,  7],
                                [ 8,  9, 10, 11],
                                [12, 13, 14, 15]]

#UnitIDListとUnitPixelIDListから、displayのPixelとUnitID,各ユニットのPixelIDを対応させるPixelIDListを生成する
        self.PixelIDList = []

        for i in range(self.UnitLayout[1]):
            for k in range(4):
                list = []
                for j in  range(self.UnitLayout[0]):
                    UnitID = self.UnitIDList[i][j]
                    for l in range(4):
                        list.append([UnitID,self.UnitPixelIDList[k][l]])

                self.PixelIDList.append(list)

        #生成されたPixelIDListを確認
        print("PixelIDList:")
        for i in range(len(self.PixelIDList)):
            print(self.PixelIDList[i])

# サーボのキャリブレーションデータ 4*4ユニット対応版
        self.usCenter= [[1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500],
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

                        [1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500],
                        [1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500],
                        [1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500],
                        [1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500,  1500, 1500, 1500, 1500]]


        self.usMax   = [[1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900],
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

                        [1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900],
                        [1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900],
                        [1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900],
                        [1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900,  1900, 1900, 1900, 1900]]


        self.usMin   = [[1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100],
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

                        [1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100],
                        [1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100],
                        [1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100],
                        [1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100,  1100, 1100, 1100, 1100]]

# 3bitグレースケール用のポジションリストを生成する
        print("3bit GrayScale List generating ")
        self.us3bitGrayScalePositionList  = []
        for i in range(4):
            listUnit = []
            for j in range(8):
                listServo = []
                for k in range(8):
                    listServo.appnend(int(self.usMin[j][k] + (((self.usCenter[j][k] - self.usMin[j][k]) / 7) * i * 2)))   
                listUnit.append(listServo)
            self.us3bitGrayScalePositionList.append(listUnit)

        for i in range(4, 4):
            listUnit = []
            for j in range(8):
                listServo = []
                for k in range(8):
                    listServo.appnend(int(self.usCenter[j][k] + (((self.usMax[j][k] - self.usCenter[j][k]) / 7) * i * 2)))   
                listUnit.append(listServo)
            self.us3bitGrayScalePositionList.append(listUnit)
        print("3bit GrayScale List generate complete.")
        print("unit 0, scale 0")
        for i in range(8):
            print(self.us3bitGrayScalePositionList[0][0])
        print("unit 0, scale 1")
        for i in range(8):
            print(self.us3bitGrayScalePositionList[1][0])    


        print(i,j)

#サーボドライバ初期化
        self.pca = []
        for i in range(self.UnitLayout[1]):
            for j in range(self.UnitLayout[0]):
                self.pca.append(servo.Servos(self.i2c, address = self.UnitAddressList[i][j]))
                print(self.UnitIDList[i][j])

# imageを表示するメソッド
    def setImage(self, img):
        
        #imgのサイズとdisplayのサイズがマッチするか確認
        if (len(img[0]) != (self.UnitLayout[0] * 4)):
            print("image width unmatched")
            return
        elif (len(img[1]) != (self.UnitLayout[1] * 4)):
            print("image height unmatched")
            return
        
        #差分を確認
        #変化のあったピクセルだけを動かす
        #リリースする
        
        #とりあえず3bitGrayでもらって表示するだけ
        for i in range(self.UnitLayout[1]*4):
            for j in range(Layout[0]*4):
                self.pca[self.PixelIDList[i][j][0]].position(self.PixelIDList[i][j][1], us=self.us3bitGrayScalePositionList[img[i][j]][self.PixelIDList[i][j][0]][self.PixelIDList[i][j][1]])
                time.sleep_ms(50)
                self.pca[self.PixelIDList[i][j][0]].release(self.PixelIDList[i][j][1])
        print("set image")

# 指定ピクセルを表示するメソッド
    #Valueは3bitGrayに限る
    def setPixel(self, value, coordinate):
        x = coordinate[0]
        y = coordinate[1]
        set.pca[[self.PixelIDList[x][y][0]].position(self.PixelIDList[x][y][1], us=self.us3bitGrayScalePositionList[value][x][y])]

# 全てのパネルをセンター位置に移動する
    def flatPosition(self):
        print("flat position")

        for i in range(self.UnitLayout[1]*4):
            for j in range(Layout[0]*4):
                self.pca[self.PixelIDList[i][j][0]].position(self.PixelIDList[i][j][1], us=self.usCenter[self.PixelIDList[i][j][0]][self.PixelIDList[i][j][1]])
                time.sleep_ms(50)
                self.pca[self.PixelIDList[i][j][0]].release(self.PixelIDList[i][j][1])

# 全てのパネルを最小位置に移動する
    def maxPosition(self):
        print("max position")
        for i in range(self.UnitLayout[1]*4):
            for j in range(Layout[0]*4):
                self.pca[self.PixelIDList[i][j][0]].position(self.PixelIDList[i][j][1], us=self.usMax[self.PixelIDList[i][j][0]][self.PixelIDList[i][j][1]])
                time.sleep_ms(50)
                self.pca[self.PixelIDList[i][j][0]].release(self.PixelIDList[i][j][1])

# 全てのパネルを最小位置に移動する
    def minPosition(self):
        print("min position")
        for i in range(self.UnitLayout[1]*4):
            for j in range(Layout[0]*4):
                self.pca[self.PixelIDList[i][j][0]].position(self.PixelIDList[i][j][1], us=self.usMin[self.PixelIDList[i][j][0]][self.PixelIDList[i][j][1]])
                time.sleep_ms(50)
                self.pca[self.PixelIDList[i][j][0]].release(self.PixelIDList[i][j][1])

# 全てのサーボをリリースするメソッド
    def Release(self, coordinate = 0):
        #全てのサーボをリリース
        if coordinate == 0:
            print("all servo release")
            for i in range(self.UnitLayout[1]*4):
                for j in range(Layout[0]*4):
                    self.pca[self.PixelIDList[i][j][0]].release(self.PixelIDList[i][j][1])
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

#フラット位置に移動
"""
for i in range(Layout[1]*4):
    for j in range(Layout[0]*4):
#        print("UnitNo:",i)
#        print("ServoNo:",PixelIDList[i][j][1])
        display.pca[display.PixelIDList[i][j][0]].position(display.PixelIDList[i][j][1], us=display.usMax[display.PixelIDList[i][j][0]][display.PixelIDList[i][j][1]])
        time.sleep_ms(50)
#        pca[PixelIDList[i][j][0]].release(PixelIDList[i][j][1])
#        time.sleep_ms(50)
        display.pca[display.PixelIDList[i][j][0]].position(display.PixelIDList[i][j][1], us=display.usCenter[display.PixelIDList[i][j][0]][display.PixelIDList[i][j][1]])
        time.sleep_ms(50)
        display.pca[display.PixelIDList[i][j][0]].release(display.PixelIDList[i][j][1])

for j in range(display.UnitLayout[1]*4):
    for i in range(display.UnitLayout[0]*4):
#        print("UnitNo:",i)
#        print("ServoNo:",PixelIDList[i][j][1])
        display.pca[display.PixelIDList[i][j][0]].position(display.PixelIDList[i][j][1], us=display.usMin[display.PixelIDList[i][j][0]][display.PixelIDList[i][j][1]])
        time.sleep_ms(100)
#        pca[PixelIDList[i][j][0]].release(PixelIDList[i][j][1])
#        time.sleep_ms(50)
        display.pca[display.PixelIDList[i][j][0]].position(display.PixelIDList[i][j][1], us=display.usCenter[display.PixelIDList[i][j][0]][display.PixelIDList[i][j][1]])
        time.sleep_ms(50)
        display.pca[display.PixelIDList[i][j][0]].release(display.PixelIDList[i][j][1])
"""
print("use method")

#display.flatPosition()
display.maxPosition()
display.minPosition()
display.flatPosition()
display.flatPosition()
display.allRelease()


"""
for i in range(UnitLayout[1]*4):
    for j in range(UnitLayout[0]*4):
        pca[PixelIDList[i][j][0]].position(PixelIDList[i][j][1], us=usMax[i][j])
        pca[PixelIDList[i][j][0]].release(PixelIDList[i][j][1])
time.sleep_ms(1000)

for i in range(UnitLayout[1]*4):
    for j in range(UnitLayout[0]*4):
        pca[PixelIDList[i][j][0]].position(PixelIDList[i][j][1], us=usMin[i][j])
        pca[PixelIDList[i][j][0]].release(PixelIDList[i][j][1])
time.sleep_ms(1000)

for i in range(UnitLayout[1]*4):
    for j in range(UnitLayout[0]*4):
        pca[PixelIDList[i][j][0]].position(PixelIDList[i][j][1], us=usCenter[i][j])
        pca[PixelIDList[i][j][0]].release(PixelIDList[i][j][1])
time.sleep_ms(1000)
"""
