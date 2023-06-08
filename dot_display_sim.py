import numpy as np
import cv2

class VDisplay():
    def __init__(self, displayWidth, displayHeight,fps=10):

        self.displayWidth  = displayWidth
        self.displayHeight = displayHeight
        self.delay_ms = int(1/fps*1000)

# 仮想ディスプレイ上のドットのサイズとギャップの定義
        self.dotSize = 30
        self.dotGap = 5

# 仮想ディスプレイの描画サイズ定義
        self.VImgWidth = (self.dotSize * displayWidth) + (self.dotGap * (displayWidth + 1))
        self.VImgHeight = (self.dotSize * displayHeight) + (self.dotGap * (displayHeight + 1)) 

# 仮想ディスプレイ用img生成
        self.img = np.full((self.VImgHeight, self.VImgWidth), 128, dtype=np.uint8)

# 仮想ディスプレイのdotピクセル座標リスト定義
        self.pixelCoordinate = np.zeros((displayWidth, displayHeight, 2), dtype=int)

        for i in range(displayWidth):
            for j in range(displayHeight):
                self.pixelCoordinate[i,j] = (int(self.dotGap * (i + 1) + (self.dotSize * i)), int(self.dotGap * (j + 1) + (self.dotSize * j)))

# 仮想ディスプレイにdotImgを表示するメソッド
    def setVDisplay(self, dotImg):
        #print(dotImg)
        for i in range(self.displayWidth):
            for j in range(self.displayHeight):
                self.x = self.pixelCoordinate[i,j,0]
                self.y = self.pixelCoordinate[i,j,1]
                self.color = int(dotImg[i,j])
                cv2.rectangle(self.img, (self.x, self.y), (self.x + self.dotSize, self.y + self.dotSize), self.color, thickness = -1)
        cv2.imshow("img",self.img)
        key = cv2.waitKey(self.delay_ms)

    def setPixel(self, coordinate, color):
        self.x = self.pixelCoordinate[coordinate[0],coordinate[1],0]
        self.y = self.pixelCoordinate[coordinate[0],coordinate[1],1]
        cv2.rectangle(self.img, (self.x, self.y), (self.x + self.dotSize, self.y + self.dotSize), color, thickness = -1)
        cv2.imshow("img", self.img)
        key = cv2.waitKey(self.delay_ms)

    # テキストのdotImageを受け取り、スクロールアニメーションに変換して仮想ディスプレイに表示するメソッド
    def scrollText(self, fullImg, fps=10):

        # FPS設定
        self.delay_ms = int(1/fps*1000)
        # スクロール前後の空白データ設定
        self.scrollFade = np.zeros((self.displayWidth - 1, fullImg.shape[1]), dtype=int)
        # テキストのdotImgの前後に空白データを追加
        self.scrollImg = np.concatenate([self.scrollFade,fullImg,self.scrollFade], axis = 0)
        #print("scrollImg=")
        #print(self.scrollImg)

        # スクロールアニメーションのトータルフレーム数を計算
        self.totalFrames = fullImg.shape[0] + self.displayWidth
    
        # dotImageを左から右へスライドしつつ一画面分のデータをsetDisplayに送る
        for i in range(self.totalFrames - 1):
            self.dotImg = np.delete(self.scrollImg, np.s_[:i], axis = 0)
            self.dotImg = np.delete(self.dotImg, np.s_[self.displayWidth:], axis = 0)
            self.setVDisplay(self.dotImg)

        cv2.destroyAllWindows()

    def playAnimation(self, animationData, fps=10):

        # FPS設定
        self.delay_ms = int(1/fps*1000)

        self.totalFrames = animationData.shape[0]
        for i in range(self.totalFrames):
            self.setVDisplay(animationData[i])