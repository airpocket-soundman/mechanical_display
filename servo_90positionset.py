from machine import I2C
import time
import pca9685
import servo


usCenter=[[1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500],
          [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500],
          [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500],
          [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]]

#usCenter=[[1500, 1480, 1630, 1620, 1670, 1580, 1500, 1650, 1690, 1470, 1580, 1600, 1510, 1580, 1450, 1550],
#          [1500, 1560, 1470, 1450, 1590, 1450, 1510, 1420, 1570, 1480, 1540, 1620, 1520, 1530, 1560, 1500],
#          [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500],
#          [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]]
usMax   =[[1850, 1850, 2000, 1950, 2000, 1950, 1870, 1990, 2010, 1830, 1930, 1920, 1900, 1900, 1900, 1900],
          [1850, 1870, 1820, 1800, 1950, 1800, 1870, 1810, 1920, 1860, 1900, 1940, 1820, 1880, 1900, 1870],
          [1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900],
          [1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900]]
usMin   =[[1140, 1120, 1250, 1250, 1320, 1250, 1180, 1330, 1310, 1130, 1270, 1220, 1210, 1250, 1090, 1210],
          [1160, 1200, 1110, 1090, 1230, 1100, 1170, 1090, 1200, 1150, 1200, 1300, 1150, 1210, 1250, 1180],
          [1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100],
          [1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100]]

i2c = I2C(I2C.I2C0, freq=100000, scl=34, sda=35)

addr = i2c.scan()
print( "address is :" + str(addr) )
pcaNum =  1

pca = []

pca.append(servo.Servos(i2c,address = 64))
#pca.append(servo.Servos(i2c,address = 65))
#pca.append(servo.Servos(i2c,address = 68))
#pca.append(servo.Servos(i2c,address = 69))

for i in range(16):
    pca[0].position(i,us = 1000)
time.sleep_ms(1000)

for i in range(16):
    pca[0].position(i,us = 1900)
time.sleep_ms(1000)



for i in range(16):
    pca[0].position(i,us = 1400)
time.sleep_ms(1000)

"""
for i in range(pcaNum):
    pca.append(servo.Servos(i2c,address = addr[i]))
    print(addr[i])

print(pca)

for i in range(pcaNum):
    for j in range(16):
        pca[i].position(j, us=usCenter[i][j])
        #pca[i].release(j)
time.sleep_ms(200)

#time.sleep_ms(1000)


for i in range(pcaNum):
    for j in range(16):
        pca[i].position(j, us=usMax[i][j])
        #pca[i].release(j)
time.sleep_ms(200)
#time.sleep_ms(100)

for i in range(pcaNum):
    for j in range(16):
        pca[i].position(j, us=usMin[i][j])
        #pca[i].release(j)
time.sleep_ms(200)
#time.sleep_ms(100)

for i in range(pcaNum):
    for j in range(16):
        pca[i].position(j, us=usMax[i][j])
        #pca[i].release(j)
time.sleep_ms(200)
#time.sleep_ms(100)

for i in range(pcaNum):
    for j in range(16):
        pca[i].position(j, us=usCenter[i][j])
        #pca[i].release(j)
time.sleep_ms(200)
#time.sleep_ms(100)



for i in range(pcaNum):
    for j in range(16):
        #pca[i].position(j, us=usCenter[i][j])
        pca[i].release(j)


"""
