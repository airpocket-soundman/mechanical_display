import numpy as np
import dot_display_sim
import animation_data_4x4
import animation_data_8x8

# dotDisplayの解像度定義
dotDisplayWidth  = 8
dotDisplayHeight = 8

# 仮想ドットディスプレイのインスタンス作成
VDisplay = dot_display_sim.VDisplay(dotDisplayWidth, dotDisplayHeight)

#
animeLib = animation_data_8x8.animationData()

animationData = np.concatenate([animeLib.RightUp2LeftLow,
                                animeLib.RightLow2LeftUp,
                                animeLib.LeftLow2RightUp,
                                animeLib.LeftUp2RightLow],
                                axis=0)

VDisplay.playAnimation(animationData, 10)  #(アニメーションデータ(256階調))