import numpy as np
import dot_display_sim
from dot_image_editor import invert,vflip,hflip,rotate90,rotate180,rotate270
import time
import math

# dotDisplayの解像度定義
dotDisplayWidth  = 8
dotDisplayHeight = 8

# 仮想ドットディスプレイのインスタンス作成
VDisplay = dot_display_sim.VDisplay(dotDisplayWidth, dotDisplayHeight,fps = 50)

flat = np.full((8,8),127)
max_amplitude = 127
power = 1
decay_rate = 0.90
VDisplay.setVDisplay(flat)
time_count = 0
time_resolution = 30

for i in range(1,time_resolution + 1,1):
    displacement = math.sin(i/time_resolution * math.pi * 2) * max_amplitude * power + 127
    print(i/time_resolution, displacement )
    VDisplay.setPixel([0,0],displacement)
    max_amplitude *= decay_rate
    print(max_amplitude)
#    time.sleep(1)

time.sleep(2)