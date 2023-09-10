from machine import Pin, I2C, UART
import time
import mechanical_display

i2c0 = I2C(0, freq = 100000, scl=Pin(5), sda=Pin(4))
i2c1 = I2C(1, freq = 100000, scl=Pin(3), sda=Pin(2))

addr0 = i2c0.scan()
addr1 = i2c1.scan()

print("addr0:", addr0)
print("addr1:", addr1)