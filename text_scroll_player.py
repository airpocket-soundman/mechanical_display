import numpy as np
import text2dot
import dot_display_sim

# dotDisplayの階調(bit数で) 8:256階調 0-255
grayBit = 8

# dotDisplayの解像度定義
dotDisplayWidth = 32
dotDisplayHeight = 8

# 仮想ドットディスプレイのインスタンス作成
VDisplay = dot_display_sim.VDisplay(dotDisplayWidth, dotDisplayHeight)
# テキスト＝フォント変換器のインスタンス生成
font = text2dot.dotsFont()

# テキストをDotImageに変換
dotImg = font.setDotImg("0123456789",5)

# dotImageのheightを取得
shape = dotImg.shape[1]
#print("shape=" + str(shape))

# dotImageのheightが仮想ドットディスプレイよりも低かった場合、dotImageの下に空白エリアを追加
if dotImg.shape[1] < dotDisplayHeight:
    newDotImg = np.zeros((dotImg.shape[0],dotDisplayHeight))
    newDotImg[:, :dotImg.shape[1]-dotDisplayHeight] = dotImg
    dotImg = newDotImg

dotImg = dotImg*(2**(grayBit))
print(dotImg)
VDisplay.scrollText(dotImg, 10)
