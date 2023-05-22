from machine import Pin, I2C
import time
import pca9685
import servo
 
i2c = I2C(1, scl=Pin(3), sda=Pin(2))


addr = i2c.scan()
print( "address is :" + str(addr) )
pca = servo.Servos(i2c,address=0x40)

while True:
    pca.position(0, 90)
    time.sleep_ms(1000)
    pca.position(0, 60)
    time.sleep_ms(1000)
    pca.position(0, 120)
    time.sleep_ms(1000)