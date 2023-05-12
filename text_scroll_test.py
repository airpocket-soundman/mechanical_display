import numpy as np
import text2dot
import dot_display_sim

# dotDisplayの階調(bit数で)
monoBit = 3

# dotDisplayの解像度定義
dotDisplayWidth = 25
dotDisplayHeight = 7

# 仮想ドットディスプレイのインスタンス作成
VDisplay = dot_display_sim.VDisplay(dotDisplayWidth, dotDisplayHeight)
# テキスト＝フォント変換器のインスタンス生成
font = text2dot.dotsFont5p()

dotImg = font.setDotImg("test document")
shape = dotImg.shape[1]
#print("shape=" + str(shape))
if dotImg.shape[1] < dotDisplayHeight:
    newDotImg = np.zeros((dotImg.shape[0],dotDisplayHeight))
    newDotImg[:, :dotImg.shape[1]-dotDisplayHeight] = dotImg
    dotImg = newDotImg

dotImg = dotImg*(2**3)
VDisplay.scrollText(dotImg*(2**(8-monoBit)), 10)