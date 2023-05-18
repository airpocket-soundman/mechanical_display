import numpy as np
import dot_display_sim
import animation_data_4x4
import animation_data_8x8
from dot_image_editor import invert,vflip,hflip,rotate90,rotate180,rotate270

# dotDisplayの解像度定義
dotDisplayWidth  = 8
dotDisplayHeight = 8

# 仮想ドットディスプレイのインスタンス作成
VDisplay = dot_display_sim.VDisplay(dotDisplayWidth, dotDisplayHeight)

# アニメーションライブラリ読み込み
animeLib = animation_data_8x8.animationData()

# アニメーションデータを結合して編集
animationData = np.concatenate([animeLib.RightUp2LeftLow,
                                animeLib.RightLow2LeftUp,
                                animeLib.LeftLow2RightUp,
                                animeLib.LeftUp2RightLow],
                                axis=0)

# アニメーションデータの白黒反転
animationData = invert(animationData)
#animationData = vflip(animationData)
animationData = rotate270(animationData)

# アニメーションデータを仮想ドットディスプレイに表示
VDisplay.playAnimation(animationData, 10)  #(アニメーションデータ(256階調))