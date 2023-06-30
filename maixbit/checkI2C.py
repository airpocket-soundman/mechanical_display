from machine import I2C
import time
import pca9685
import servo
import font

from Maix import GPIO
from fpioa_manager import fm, board_info
import lcd
import sensor

#I2C　初期化
i2c = I2C(I2C.I2C0, freq=100000, scl=34, sda=35)

#I2C 接続されているユニットのアドレス確認
addr = i2c.scan()
print( "address is :" + str(addr) )
