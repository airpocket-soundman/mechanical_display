from machine import I2C
import time
import pca9685
import servo
 
usCenter=[1500, 1480, 1630, 1620, 1670, 1580, 1500, 1650, 1690, 1470, 1580, 1600, 1510, 1580, 1450, 1550]
usMax   =[1850, 1850, 2000, 1950, 2000, 1950, 1870, 1990, 2010, 1830, 1930, 1920, 1900, 1900, 1900, 1900]
usMin   =[1140, 1120, 1250, 1250, 1320, 1250, 1180, 1330, 1310, 1130, 1270, 1220, 1210, 1250, 1090, 1210]

i2c = I2C(I2C.I2C0, freq=100000, scl=35, sda=34)

addr = i2c.scan()
print( "address is :" + str(addr) )

pca = []
pca.append(servo.Servos(i2c,address=0x40))

for i in range(16):
    pca[0].position(i, us=usCenter[i])
time.sleep_ms(1000)

for i in range(16):
    pca[0].position(i, us=usMax[i])
time.sleep_ms(1000)

for i in range(16):
    pca[0].position(i, us=usMin[i])
time.sleep_ms(1000)

for i in range(16):
    pca[0].position(i, us=usCenter[i])
time.sleep_ms(1000)


for i in range(8,12):
    pca[0].position(i, us=usCenter[i])

for i in range(12,16):
    pca[0].position(i, us=usCenter[i])

time.sleep(1)

for i in range(8,12):
    pca[0].position(i, us=usMin[i])

for i in range(12,16):
    pca[0].position(i, us=usMin[i])

time.sleep(1)

for i in range(8,12):
    pca[0].position(i, us=usMin[i])

for i in range(12,16):
    pca[0].position(i, us=usMin[i])

time.sleep(1)

for i in range(16):
    pca[0].release(i)

"""
while True:
#    servo
    for i in range(16):
        pca[0].position(i, us=usCenter[i])
    time.sleep_ms(1000)

    for i in range(16):
        pca[0].position(i, us=usMax[i])
    time.sleep_ms(1000)

    for i in range(16):
        pca[0].position(i, us=usMin[i])
    time.sleep_ms(1000)

    for i in range(16):
        pca[0].position(i, us=usCenter[i])
    time.sleep_ms(1000)

    for i in range(16):
        pca[0].position(i, us=usMax[i])
        time.sleep_ms(100)

    for i in range(16):
        pca[0].position(i, us=usMin[i])
        time.sleep_ms(100)

    pca[0].position(0, us=usCenter[0])
    pca[0].position(4, us=usCenter[4])
    pca[0].position(8, us=usCenter[8])
    pca[0].position(12, us=usCenter[12])
    time.sleep_ms(200)

    pca[0].position(1, us=usCenter[1])
    pca[0].position(5, us=usCenter[5])
    pca[0].position(9, us=usCenter[9])
    pca[0].position(13, us=usCenter[13])
    time.sleep_ms(200)

    pca[0].position(2, us=usCenter[2])
    pca[0].position(6, us=usCenter[6])
    pca[0].position(10, us=usCenter[10])
    pca[0].position(14, us=usCenter[14])
    time.sleep_ms(200)

    pca[0].position(3, us=usCenter[3])
    pca[0].position(7, us=usCenter[7])
    pca[0].position(11, us=usCenter[11])
    pca[0].position(15, us=usCenter[15])
    time.sleep_ms(200)

    for i in range(4):
        pca[0].position(i,us=usMax[i])
    time.sleep_ms(200)
    for i in range(4):
        pca[0].position(i+4,us=usMin[i+4])
    time.sleep_ms(200)
    for i in range(4):
        pca[0].position(i+8,us=usMax[i+8])
    time.sleep_ms(200)
    for i in range(4):
        pca[0].position(i+12,us=usMin[i+12])
    time.sleep_ms(200)

    for i in range(4):
        pca[0].position(i,us=usMin[i])
    time.sleep_ms(200)
    for i in range(4):
        pca[0].position(i+4,us=usMax[i+4])
    time.sleep_ms(200)
    for i in range(4):
        pca[0].position(i+8,us=usMin[i+8])
    time.sleep_ms(200)
    for i in range(4):
        pca[0].position(i+12,us=usMax[i+12])
    time.sleep_ms(200)
"""
