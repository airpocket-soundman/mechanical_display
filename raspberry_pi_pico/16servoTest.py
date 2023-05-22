from machine import Pin, I2C
import time
import pca9685
import servo
 
i2c = I2C(1, scl=Pin(3), sda=Pin(2))

addr = i2c.scan()
print( "address is :" + str(addr) )
pca = servo.Servos(i2c,address=0x40)

positionCenter = [ 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90]
positionMax    = [ 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]
positionMin    = [-30,-30,-30,-30,-30,-30,-30,-30,-30,-30,-30,-30,-30,-30,-30,-30]



fps = 10
delay_ms = 1000/fps




for i in range(16):
    pca.position(i, positionCenter[i])


movie=[]
movie.append(positionMin)

for j in range(10):
    position = []
    print("movie[j]=" + str(movie[j]))
    for i in range(len(positionMax)):
        position.append(movie[j][i] + positionMax[i]/10)
        print("movie[j][i]=" + str(movie[j][i]))
        print(position)
    movie.append(position)
for j in range(10):
    position = []
    print("movie[j]=" + str(movie[j]))
    for i in range(len(positionMax)):
        position.append(movie[j+10][i] - positionMax[i]/10)
        print("movie[j][i]=" + str(movie[j][i]))
        print(position)
    movie.append(position)
for j in range(10):
    position = []
    print("movie[j]=" + str(movie[j]))
    for i in range(len(positionMax)):
        position.append(movie[j+20][i] + positionMin[i]/10)
        print("movie[j][i]=" + str(movie[j][i]))
        print(position)
    movie.append(position)
for j in range(10):
    position = []
    print("movie[j]=" + str(movie[j]))
    for i in range(len(positionMax)):
        position.append(movie[j+30][i] - positionMin[i]/10)
        print("movie[j][i]=" + str(movie[j][i]))
        print(position)
    movie.append(position)

del movie[0]
print(movie)
print(len(movie))
counter = 0
while True:
#    servo
    pca.position(0, 90)
    time.sleep_ms(1000)
    pca.position(0, 60)
    time.sleep_ms(1000)
    pca.position(0, 120)
    time.sleep_ms(1000)