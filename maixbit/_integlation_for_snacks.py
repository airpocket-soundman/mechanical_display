from machine import I2C
import time
import pca9685
import servo
import font
import ds3231

from Maix import GPIO
#from fpioa_manager import fm, board_info
import lcd
import sensor
import mechanical_display

#=======================================================================================================================
#ボタン設定
#fm.register(board_info.BUTTON_A, fm.fpioa.GPIO1)
#button_a = GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP)
#fm.register(board_info.BUTTON_B, fm.fpioa.GPIO2)
#button_b = GPIO(GPIO.GPIO2, GPIO.IN, GPIO.PULL_UP)



#LCD設定
#lcd.init(freq=15000000)
lcd.init()
lcd.direction(lcd.YX_LRDU)

#カメラ設定
sensor.reset()                      # Reset and initialize the sensor. It will
                                    # run automatically, call sensor.run(0) to stop
sensor.set_pixformat(sensor.GRAYSCALE) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)   # Set frame size to QVGA (320x240) QQVGA (160x120)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
sensor.set_contrast(+2)             # Contrast +2 to -2
#sensor.set_brightness(-2)           # Brightness +2 to -2
#sensor.set_saturation(-2)           # Saturation +2 to -2
sensor.set_auto_gain(0,20)           # enable,gain_db enable=1:auto,0:off
#sensor.set_vflip(1)                 # 1:enable 0:disable
sensor.set_hmirror(1)                 # 1:enable 0:disable



#displayのUnit配置数定義
unit_layout  = [4, 4]          #[width,height]　現在は[4,4]まで対応。増やす際は、I2Cのaddressリストも修正が必要。
servo_layout = [4, 4]
pixel_layout = [unit_layout[0] * servo_layout[0], unit_layout[1] * servo_layout[1]]
gray_scale_bit_value = 8
gray_scale_level = 2**gray_scale_bit_value



#I2C　初期化
i2c0 = I2C(I2C.I2C0, freq=100000, scl=34, sda=35)
i2c1 = I2C(I2C.I2C1, freq=100000, scl=32, sda=33)

#I2C 接続されているユニットのアドレス確認
addr0 = i2c0.scan()
addr1 = i2c1.scan()
print("address is :" + str(addr0))
print("address is :" + str(addr1))
#displayのインスタンス生成
display = mechanical_display.mechanical_display(i2c0, i2c1, unit_layout, servo_layout, gray_scale_bit_value)

#5Pフォントのインスタンス生成
Font = font.font_5P()

#flatポジションを表示する。
display.flatPosition()
time.sleep_ms(300)



#=====================================================================================================
#RTCのインスタンスを生成
ds = ds3231.DS3231(i2c1)

"""
#RTCの時間設定
year    = 2023 # Can be yyyy or yy format
month   = 7
mday    = 4
hour    = 15 # 24 hour format only
minute  = 28
second  = 30 # Optional
weekday = 2 # Optional

datetime = (year, month, mday, hour, minute, second, weekday)
ds.datetime(datetime)
print(ds.datetime())
"""

#現在時刻をRTCから読み取って表示
year    = ds.datetime()[0]
month   = ds.datetime()[1]
day     = ds.datetime()[2]
hour    = ds.datetime()[4]
minute  = ds.datetime()[5]
second  = ds.datetime()[6]
print(year, month, day, hour, minute, second)


def clock_display(loop_num = 300):
    counter = 0
    while counter < loop_num:
        bg_image = display.bg_image_generate(50)

  #      print(bg_image)
        hour    = ds.datetime()[4]
        minute  = ds.datetime()[5]
        second  = ds.datetime()[6]
        hour_image      = Font.genTextImage(text = '{:02}'.format(hour),font = "number3x5p")
        colon_image     = Font.genTextImage(text = "  ", font = "propotional")
        minute_image    = Font.genTextImage(text = '{:02}'.format(minute),font = "number3x5p")
        sec_image       = Font.genTextImage(text = '{:02}'.format(second),font = "number3x5p")

        clock_image = display.textOverlay(bg_image,    hour_image,   offset = [0,2], text_color = 200, transparent = True)
        clock_image = display.textOverlay(clock_image, colon_image,  offset = [6,2], text_color = 200, transparent = True)
        clock_image = display.textOverlay(clock_image, minute_image, offset = [9,2], text_color = 200, transparent = True)
        clock_image = display.textOverlay(clock_image, sec_image,    offset = [9,9], text_color = 200, transparent = True)

        display.setImage(clock_image)
        #time.sleep_ms(10)
        counter += 1

# カメラ画像表示
def camera_show(delay = 1, flame = 500):
    counter = 0
    while flame < counter:
#    if button_a.value() == 0:
#        break

        camera_image = sensor.snapshot()         # Take a picture and return the image.
        camera_image = camera_image.copy((20,0,140,120))
        lcd.display(camera_image)
        camera_image = camera_image.resize(pixel_layout[0], pixel_layout[1])
        for x in range(pixel_layout[0]):
            for y in range(pixel_layout[1]):
                p = 255-camera_image.get_pixel(x,y)
                display.setPixel([x,y],p)
                #print(p)
        counter += 1
        time.sleep_ms(delay)

#8bit gray scale 表示
def gray_scale_demo():
    color = 255
    for x in range(16):
        for y in range(16):
            display.setPixel([x, y],color)
            color -= 1


def snacks_text():
    print("snacks")
    text_image = Font.genTextImage(text = "        2023.7.17  SNACKS Vol.5 (>_0)",font = "propotional")
    bg_image = display.bg_image_generate(base_color)
    for x in range(len(text_image)):
        bg_image = display.bg_image_generate(base_color)
        image = display.textOverlay(bg_image, text_image, offset = [-x, 2], text_color = text_color, transparent = True)
        display.setImage(image)
        time.sleep_ms(100)

    time.sleep_ms(200)

    text_image = Font.genTextImage(text = "        MECHANICAL DISPLAY  8BIT GRAY SCALE VERSION.",font = "propotional")
    bg_image = display.bg_image_generate(base_color)
    for x in range(len(text_image)):
        bg_image = display.bg_image_generate(base_color)
        image = display.textOverlay(bg_image, text_image, offset = [-x, 9], text_color = text_color, transparent = True)
        display.setImage(image)
        time.sleep_ms(100)

    time.sleep_ms(1000)
    gray_scale_demo()
#=====================================================================================================


while True:

    # snacks demo text表示

    snacks_text()
    # カメラ画像を表示
    camera_show(delay = 1, flame = 500)
    # mario 表示

    # life game 表示

    # wave cos 表示

    # wave sin 表示

    # clock 表示
    clock_display(loop_num = 300)


display.maxPosition()
time.sleep_ms(1000)
#display.flatPosition()
#time.sleep_ms(100)
#"""



display.flatPosition()
time.sleep_ms(1000)
clock_display()

display.release()
