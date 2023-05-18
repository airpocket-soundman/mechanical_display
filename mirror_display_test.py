import cv2
import numpy as np
import time

print(cv2.__version__)

# dotDisplayの解像度定義
displayWidth = 24
displayHeight = 6

# dotDisplay用のイメージデータアレイ定義 
dotImg = np.zeros((displayWidth, displayHeight), dtype=int)

# シミュレーション用の仮想ディスプレイクラス
class VDisplay():
    def __init__(self, displayWidth, displayHeight):

# 仮想ディスプレイ上のドットのサイズとギャップの定義
        self.dotSize = 20
        self.dotGap = 4

# 仮想ディスプレイの描画サイズ定義
        self.imgWidth = (self.dotSize * displayWidth) + (self.dotGap * (displayWidth + 1))
        self.imgHeight = (self.dotSize * displayHeight) + (self.dotGap * (displayHeight + 1)) 

# 仮想ディスプレイ用img生成
        self.img = np.full((self.imgHeight, self.imgWidth), 128, dtype=np.uint8)

# 仮想ディスプレイのdotピクセル座標リスト定義
        self.pixelCoordinate = np.zeros((displayWidth, displayHeight, 2), dtype=int)

        for i in range(displayWidth):
            for j in range(displayHeight):
                self.pixelCoordinate[i,j] = (int(self.dotGap * (i + 1) + (self.dotSize * i)), int(self.dotGap * (j + 1) + (self.dotSize * j)))

    def setDisplay(self, dotImg):
        print(dotImg)
        for i in range(displayWidth):
            for j in range(displayHeight):
                self.x = self.pixelCoordinate[i,j,0]
                self.y = self.pixelCoordinate[i,j,1]
                self.color = int(dotImg[i,j])
                cv2.rectangle(self.img, (self.x, self.y), (self.x + self.dotSize, self.y + self.dotSize), self.color, thickness = -1)
        cv2.imshow("img",self.img)
        key = cv2.waitKey(self.delay_ms)

    def scrollDisplay(self, fullImg, fps):

        self.delay_ms = int(1/fps*1000)
        self.scrollFade = np.zeros((displayWidth - 1, fullImg.shape[1]), dtype=int)
        self.scrollImg = np.concatenate([self.scrollFade,fullImg,self.scrollFade], axis = 0)
        print(self.scrollImg)
        self.totalFrames = fullImg.shape[0] + displayWidth
    
        for i in range(self.totalFrames - 1):
            self.dotImg = np.delete(self.scrollImg, np.s_[:i], axis = 0)
            self.dotImg = np.delete(self.dotImg, np.s_[displayWidth:], axis = 0)
            self.setDisplay(self.dotImg)

        cv2.destroyAllWindows()



char1 = np.array([[255,255,0,0],[0,255,255,0],[0,0,255,255],[0,0,0,255]])
char2 = np.array([[0,0,255,255],[0,255,255,0],[255,255,0,0],[255,0,0,0]])
charh = np.array([[255,255,255,255],[0,255,0,0],[0,0,255,255]])
chare = np.array([[0,255,255,0],[255,0,255,255],[0,255,0,255]])
charl = np.array([[255,0,0,0],[255,255,255,255]])
charo = np.array([[0,255,255,255],[0,255,0,255],[0,255,255,255]])
charw = np.array([[0,255,255,0],[0,0,0,255],[0,0,255,0],[0,0,0,255],[0,255,255,0]])
charr = np.array([[0,255,255,255],[0,0,255,0],[0,255,0,0]])
chard = np.array([[0,255,255,255],[0,255,0,255],[255,255,255,255]])
sp1 = np.array([[0,0,0,0]])
sp2 = np.array([[0,0,0,0],[0,0,0,0]])

HH = np.array([[0,255,255,255,255,255],[0,0,0,255,0,0],[0,0,0,255,0,0],[0,255,255,255,255,255],[0,0,0,0,0,0]])
EE = np.array([[0,255,255,255,255,255],[0,255,0,255,0,255],[0,255,0,255,0,255],[0,0,0,0,0,0]])
LL = np.array([[0,255,255,255,255,255],[0,0,0,0,0,255],[0,0,0,0,0,255],[0,0,0,0,0,0]])
OO = np.array([[0,0,255,255,255,0],[0,255,0,0,0,255],[0,255,0,0,0,255],[0,0,255,255,255,0],[0,0,0,0,0,0]])
WW = np.array([[0,255,255,255,255,0],[0,0,0,0,0,255],[0,0,255,255,255,0],[0,0,0,0,0,255],[0,255,255,255,255,0],[0,0,0,0,0,0]])
RR = np.array([[0,255,255,255,255,255],[0,255,0,255,0,0],[0,255,0,255,0,0],[0,0,255,0,255,255],[0,0,0,0,0,0]])
DD = np.array([[0,255,255,255,255,255],[0,255,0,0,0,255],[0,255,0,0,0,255],[0,0,255,255,255,0],[0,0,0,0,0,0]])
SP_= np.array([[0,0,0,0,0,0],[0,0,0,0,0,0]])

ha = np.array([[0,0,0,0,0,255],[0,255,255,255,255,0],[0,0,0,0,0,0],[0,255,255,255,255,0],[0,0,0,0,0,255],[0,0,0,0,0,0]])
ro = np.array([[0,255,255,255,255,255],[0,255,0,0,0,255],[0,255,0,0,0,255],[0,255,255,255,255,255],[0,0,0,0,0,0]])
wa = np.array([[0,255,255,0,0,0],[0,255,0,0,0,255],[0,255,0,0,0,255],[0,255,0,0,0,255],[0,255,255,255,255,0],[0,0,0,0,0,0]])
ru = np.array([[0,0,0,0,0,255],[0,255,255,255,255,0],[0,0,0,0,0,0],[0,255,255,255,255,255],[0,0,0,0,0,255],[0,0,0,0,0,0]])
do = np.array([[0,255,255,255,255,255],[0,0,0,255,0,0],[0,255,0,255,0,0],[0,255,0,0,0,0],[0,0,0,0,0,0]])
bar = np.array([[0,0,0,255,0,0],[0,0,0,255,0,0],[0,0,0,255,0,0],[0,0,0,255,0,0],[0,0,0,0,0,0]])


#fullDotImg= np.concatenate([char1,char2,char1], axis = 0)


#fullDotImg= np.concatenate([char1,char2,char1], axis = 0)
#fullDotImg = np.concatenate([charh,sp1,chare,sp1,charl,sp1,charl,sp1,charo,sp2,charw,sp1,charo,sp1,charr,sp1,charl,sp1,chard])
fullDotImg = np.concatenate([HH,EE,LL,LL,OO,SP_,WW,OO,RR,LL,DD,SP_,SP_,SP_,SP_,SP_,ha,ro,bar,SP_,wa,bar,ru,do])
display = VDisplay(displayWidth, displayHeight)

display.scrollDisplay(fullDotImg, 10)


