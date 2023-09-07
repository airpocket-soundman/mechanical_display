from machine import I2C

import time
import pca9685
import servo
import font

from Maix import GPIO
from fpioa_manager import fm, board_info
#import lcd
#import sensor

#I2C　初期化
print("test")
fm.register(34, fm.fpioa.GPIOHS0)
fm.register(35, fm.fpioa.GPIOHS1)
#fm.register(34, fm.fpioa.I2C0_SCLK)
#fm.register(35, fm.fpioa.I2C0_SDA)

p34 = GPIO(GPIO.GPIOHS0, GPIO.PULL_DOWN)
p35 = GPIO(GPIO.GPIOHS1, GPIO.PULL_DOWN)
#p34 = GPIO(34, GPIO.PULL_DOWN)
#p35 = GPIO(35, GPIO.PULL_DOWN)
time.sleep(3)
print("mesure")
p34 = GPIO(GPIO.GPIOHS0, GPIO.PULL_UP)
p35 = GPIO(GPIO.GPIOHS1, GPIO.PULL_UP)
#i2c = I2C(I2C.I2C0, freq=100000, scl=GPIO.GPIOHS0, sda=GPIO.GPIOHS1)
#i2c = I2C(I2C.I2C0, freq=100000, scl=34, sda=35)
#i2c = I2C(I2C.I2C0, freq=100000)
#I2C 接続されているユニットのアドレス確認
#print("finish")
#addr = i2c.scan()
#print( "address is :" + str(addr) )
