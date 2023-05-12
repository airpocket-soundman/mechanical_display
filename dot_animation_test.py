import numpy as np
import dot_display_sim
import animation_data_4x4

# dotDisplayの階調(bit数で)
monoBit = 3

# dotDisplayの解像度定義
dotDisplayWidth  = 4
dotDisplayHeight = 4

# 仮想ドットディスプレイのインスタンス作成
VDisplay = dot_display_sim.VDisplay(dotDisplayWidth, dotDisplayHeight)

#
animeLib = animation_data_4x4.animationData()

animationData = animeLib.RightLow2LeftUp



VDisplay.playAnimation(animationData*(2**(8-monoBit)), 10)