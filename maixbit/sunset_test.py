from math import cos,sin,acos,degrees,radians,pi
import math

Longitude = 134.057985               # 経度（東経を入力）
Latitude = 34.724401                 # 緯度（北緯を入力）
days = 0
daycount = [31,28,31,30,31,30,31,31,30,31,30,31]
month  = 7
day = 11
for i in range(month - 1):
    days += daycount[i]
days += day - 1
print(month,"月",day,"日")
print("days:",days)


def dCalc(n):
    w = (n + 0.5) * 2 * pi / 365
    d = + 0.33281 - 22.984 * cos(w) - 0.34990 * cos(2 * w) - 0.13980 * cos(3 * w) + 3.7872 * sin(w) + 0.03250 * sin(2 * w) + 0.07187 * sin(3 * w)
    return radians(d)


def eCalc(n):
    w = (n + 0.5) * 2 * pi / 365
    e = + 0.0072 * cos(w) - 0.0528 * cos(2 * w) - 0.0012 * cos(3 * w) - 0.1229 * sin(w) - 0.1565 * sin(2 * w) - 0.0041 * sin(3 * w)
    return e

def SunRiseTime(x, y, n):    # 日の出時刻を求める関数
    y = radians(y)    # 緯度をラジアンに変換
    d = dCalc(n)           # 太陽赤緯を求める
    e = eCalc(n)           # 均時差を求める
    # 太陽の時角幅を求める（視半径、大気差などを補正 (-0.899度)　）
    t = degrees(acos( (sin(radians(-0.899)) - sin(d) * sin(y)) / (cos(d) * cos(y)) ) )
    return ( -t + 180.0 - x + 135.0) / 15.0 - e  #日の出時刻を返す

def SunSetTime(x, y, n):     # 日の入り時刻を求める関数
    y = radians(y)      # 緯度をラジアンに変換
    d = dCalc(n)             # 太陽赤緯を求める
    e = eCalc(n)             # 均時差を求める
    # 太陽の時角幅を求める（視半径、大気差などを補正 (-0.899度)　）
    t = degrees(acos( (sin(radians(-0.899)) - sin(d) * sin(y)) / (cos(d) * cos(y)) ) );
    return ( t + 180.0 - x + 135.0) / 15.0 - e   #日の入り時刻を返す

sunrize_time = SunRiseTime(Longitude, Latitude, days)
sunset_time  = SunSetTime(Longitude, Latitude, days)
hourR = int(sunrize_time)
minR  = int((sunrize_time - hourR)*60)
secR  = int((((sunrize_time - hourR)*60) - minR) * 60)
hourS = int(sunset_time)
minS  = int((sunset_time - hourS)*60)
secS  = int((((sunset_time - hourS)*60) - minS) * 60)

print("sun rise",hourR,":",minR,":",secR)
print("sun set ",hourS,":",minS,":",secS)
