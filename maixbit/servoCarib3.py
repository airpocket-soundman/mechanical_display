from machine import I2C
import time
import pca9685
import servo

UnitLayout = [2,2]          #ユニットの配置数を指定　[width,height] 当面は[2,2]以下のみ対応

UnitID = [[64, 65, 66, 67],
          [68, 79, 70, 71],
          [72, 73, 74, 75],
          [76, 77, 78, 79]]

"""
UnitID = [[0x40, 0x41, 0x42, 0x43],
          [0x44, 0x45, 0x46, 0x47],
          [0x48, 0x49, 0x4a, 0x4b],
          [0x4c, 0x4d, 0x4e, 0x4f]]
"""

usCenter=[[1500, 1480, 1630, 1620, 1670, 1580, 1500, 1650, 1690, 1470, 1580, 1600, 1510, 1580, 1450, 1550],
          [1500, 1560, 1470, 1450, 1590, 1450, 1510, 1420, 1570, 1480, 1540, 1620, 1520, 1530, 1560, 1500],
          [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500],
          [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]]
usMax   =[[1850, 1850, 2000, 1950, 2000, 1950, 1870, 1990, 2010, 1830, 1930, 1920, 1900, 1900, 1900, 1900],
          [1850, 1870, 1820, 1800, 1950, 1800, 1870, 1810, 1920, 1860, 1900, 1940, 1820, 1880, 1900, 1870],
          [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500],
          [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]]
usMin   =[[1140, 1120, 1250, 1250, 1320, 1250, 1180, 1330, 1310, 1130, 1270, 1220, 1210, 1250, 1090, 1210],
          [1160, 1200, 1110, 1090, 1230, 1100, 1170, 1090, 1200, 1150, 1200, 1300, 1150, 1210, 1250, 1180],
          [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500],
          [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]]

i2c = I2C(I2C.I2C0, freq=100000, scl=34, sda=35)

addr = i2c.scan()
print( "address is :" + str(addr) )

pca = []

for i in range(UnitLayout[1]):
    list=[]
    for j in range(UnitLayout[0]):
        list.append(servo.Servos(i2c, address = UnitID[i][j]))
    pca.append(list)
    print(UnitID[i][j])


for i in range(UnitLayout[1]):
    for j in range(UnitLayout[0]):
        for k in range(16):
            pca[i][j].position(j, us=usCenter[i][j])
            pca[i][j].release
time.sleep_ms(1000)

for i in range(UnitLayout[1]):
    for j in range(UnitLayout[0]):
        for k in range(16):
            pca[i][j].position(j, us=usMax[i][j])
            pca[i][j].release
time.sleep_ms(1000)

for i in range(UnitLayout[1]):
    for j in range(UnitLayout[0]):
        for k in range(16):
            pca[i][j].position(j, us=usMin[i][j])
            pca[i][j].release
time.sleep_ms(1000)


for i in range(UnitLayout[1]):
    for j in range(UnitLayout[0]):
        for k in range(16):
            pca[i][j].position(j, us=usCenter[i][j])
            pca[i][j].release
time.sleep_ms(1000)

