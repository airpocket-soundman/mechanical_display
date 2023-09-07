from machine import I2C
import time
import pca9685
import servo
import font
import dot_image
import mechanical_display
import random
from math import cos,sin,tan

#=======================================================================================================================



#displayのUnit配置数定義
unit_layout  = [4, 4]          #[width,height]　現在は[4,4]まで対応。増やす際は、I2Cのaddressリストも修正が必要。
servo_layout = [4, 4]
pixel_layout = [unit_layout[0] * servo_layout[0], unit_layout[1] * servo_layout[1]]
gray_scale_bit_value = 8
gray_scale_level = 2**gray_scale_bit_value

#I2C　初期化
i2c0 = I2C(0, freq = 400000, scl=Pin(5), sda=Pin(4))
i2c1 = I2C(1, freq = 400000, scl=Pin(3), sda=Pin(2))

# I2C 接続されているユニットのアドレス確認
addr0 = i2c0.scan()
addr1 = i2c1.scan()
print("address is :" + str(addr0))
print("address is :" + str(addr1))
#displayのインスタンス生成
display = mechanical_display.mechanical_display(i2c0, i2c1, unit_layout, servo_layout, gray_scale_bit_value)
display.magnification = 32
display.distance = 1

#flatポジションを表示する。
display.flatPosition()
time.sleep_ms(300)



#=====================================================================================================

#while True:



display.maxPosition()
time.sleep_ms(2000)
display.minPosition()
time.sleep_ms(2000)

display.flatPosition()
time.sleep_ms(1000)

display.release()
