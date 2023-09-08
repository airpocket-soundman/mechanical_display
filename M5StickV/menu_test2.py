import lcd
import sensor
from Maix import I2S, GPIO
from fpioa_manager import fm
from board import board_info
import time
from machine import I2C
import pca9685
import servo
import font
import ds3231
import dot_image
import mechanical_display
import random
from math import cos,sin,tan

lcd.init()

#カメラ設定
sensor.reset()                      # Reset and initialize the sensor. It will
                                    # run automatically, call sensor.run(0) to stop
sensor.set_pixformat(sensor.GRAYSCALE) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)   # Set frame size to QVGA (320x240) QQVGA (160x120)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
sensor.set_contrast(+2)             # Contrast +2 to -2
sensor.set_auto_gain(0,10)           # enable,gain_db enable=1:auto,0:off
sensor.set_hmirror(1)                 # 1:enable 0:disable
#sensor.set_brightness(-2)           # Brightness +2 to -2
sensor.set_saturation(-2)           # Saturation +2 to -2
#sensor.set_vflip(1)                 # 1:enable 0:disable


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
display.magnification = 32
display.distance = 1

#5Pフォントのインスタンス生成
Font = font.font_5P()

#flatポジションを表示する。
display.flatPosition()
time.sleep_ms(300)

#ABボタンの定義
fm.register(board_info.BUTTON_A, fm.fpioa.GPIO1)
but_a=GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP)

fm.register(board_info.BUTTON_B, fm.fpioa.GPIO2)
but_b = GPIO(GPIO.GPIO2, GPIO.IN, GPIO.PULL_UP)

but_a_pressed = 0
but_b_pressed = 0

#MENU画面設定
menu = 0
menu_list = ["1. CAMERA", "2. CLOCK", "3. LIFE GAME", "4. M5STACK", "5. MARIO", "6. MOUSER", "7. WAVE", "8. AUTO", "1. CAMERA", "2. CLOCK", "3. LIFE GAME"]

def CAMERA():
    global but_a_pressed
    lcd.direction(lcd.YX_LRDU)
    print("camera")

    while True:
        camera_image = sensor.snapshot()         # Take a picture and return the image.
        camera_image = camera_image.copy((20,0,140,120))
        lcd.display(camera_image)
        camera_image = camera_image.resize(pixel_layout[0], pixel_layout[1])
        for x in range(pixel_layout[0]):
            for y in range(pixel_layout[1]):
                p = 255-camera_image.get_pixel(x,y)
                display.setPixel([x,y],p)
                #print(p)


        if but_a.value() == 0 and but_a_pressed == 0:
            print("A_push")
            but_a_pressed=1
            lcd.direction(lcd.YX_RLDU)
            display_menu()
            break
        if but_a.value() == 1 and but_a_pressed == 1:
            print("A_release")
            but_a_pressed=0

"""
def camera_show(delay = 1, frame = 500):
    counter = 0
    while frame > counter:
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
        print(counter,"/",frame)
"""

def CLOCK():
    global but_a_pressed
    print("clock")

    while True:
        bg_image = display.bg_image_generate(50)

#      print(bg_image)
        hour    = ds.datetime()[4]
        minute  = ds.datetime()[5]
        second  = ds.datetime()[6]
        hour_image      = Font.genTextImage(text = '{:02}'.format(hour)　　,font = "number3x5p")
        colon_image     = Font.genTextImage(text = "  "                 　,font = "propotional")
        minute_image    = Font.genTextImage(text = '{:02}'.format(minute),font = "number3x5p")
        sec_image       = Font.genTextImage(text = '{:02}'.format(second),font = "number3x5p")

        clock_image = display.textOverlay(bg_image,    hour_image,   offset = [0,2], text_color = 200, transparent = True)
        clock_image = display.textOverlay(clock_image, colon_image,  offset = [6,2], text_color = 200, transparent = True)
        clock_image = display.textOverlay(clock_image, minute_image, offset = [9,2], text_color = 200, transparent = True)
        clock_image = display.textOverlay(clock_image, sec_image,    offset = [9,9], text_color = 200, transparent = True)

        display.setImage(clock_image)


        if but_a.value() == 0 and but_a_pressed == 0:
            print("A_push")
            but_a_pressed=1
            display_menu()
            break
        if but_a.value() == 1 and but_a_pressed == 1:
            print("A_release")
            but_a_pressed=0


def LIFE_GAME():
    global but_a_pressed
    print("life game")
    while True:
        if but_a.value() == 0 and but_a_pressed == 0:
            print("A_push")
            but_a_pressed=1
            display_menu()
            break
        if but_a.value() == 1 and but_a_pressed == 1:
            print("A_release")
            but_a_pressed=0


def M5STACK():
    global but_a_pressed
    print("m5stack")
    while True:
        if but_a.value() == 0 and but_a_pressed == 0:
            print("A_push")
            but_a_pressed=1
            display_menu()
            break
        if but_a.value() == 1 and but_a_pressed == 1:
            print("A_release")
            but_a_pressed=0

def MARIO():
    global but_a_pressed
    print("mario")
    while True:
        if but_a.value() == 0 and but_a_pressed == 0:
            print("A_push")
            but_a_pressed=1
            display_menu()
            break
        if but_a.value() == 1 and but_a_pressed == 1:
            print("A_release")
            but_a_pressed=0

def MOUSER():
    global but_a_pressed
    print("mouser")
    while True:
        if but_a.value() == 0 and but_a_pressed == 0:
            print("A_push")
            but_a_pressed=1
            display_menu()
            break
        if but_a.value() == 1 and but_a_pressed == 1:
            print("A_release")
            but_a_pressed=0

def WAVE():
    global but_a_pressed
    print("wave")
    while True:
        if but_a.value() == 0 and but_a_pressed == 0:
            print("A_push")
            but_a_pressed=1
            display_menu()
            break
        if but_a.value() == 1 and but_a_pressed == 1:
            print("A_release")
            but_a_pressed=0

def AUTO():
    global but_a_pressed
    print("auto")
    while True:
        if but_a.value() == 0 and but_a_pressed == 0:
            print("A_push")
            but_a_pressed=1
            display_menu()
            break
        if but_a.value() == 1 and but_a_pressed == 1:
            print("A_release")
            but_a_pressed=0


def display_menu():
    global menu,menu_list
    lcd.clear((0,0,0))
    lcd.draw_string(20,20, "=== MENU (1 to 8)===", lcd.GREEN, lcd.BLACK)
    lcd.draw_string(20,40, ">", lcd.WHITE, lcd.BLACK)
    lcd.draw_string(30,40, menu_list[menu], lcd.BLACK, lcd.WHITE)
    lcd.draw_string(30,60, menu_list[menu+1], lcd.WHITE, lcd.BLACK)
    lcd.draw_string(30,80, menu_list[menu+2], lcd.WHITE, lcd.BLACK)
    lcd.draw_string(30,100, "....", lcd.WHITE, lcd.BLACK)

display_menu()


while True:


    if but_b.value() == 0 and but_b_pressed == 0:
        print("B_push")
        menu += 1
        if menu > 7:
            menu = 0
        print(menu)
        display_menu()
        but_b_pressed=1

    if but_b.value() == 1 and but_b_pressed == 1:
        print("B_release")
        but_b_pressed=0

    if but_a.value() == 0 and but_a_pressed == 0:
        print("A_push")
        but_a_pressed=1

        lcd.draw_string(30,40, menu_list[menu], lcd.BLACK, lcd.RED)

        if menu == 0:
            CAMERA()
        elif menu == 1:
            CLOCK()
        elif menu == 2:
            LIFE_GAME()
        elif menu == 3:
            M5STACK()
        elif menu == 4:
            MARIO()
        elif menu == 5:
            MOUSER()
        elif menu == 6:
            WAVE()
        elif menu == 7:
            AUTO()
        time.sleep_ms(200)

    if but_a.value() == 1 and but_a_pressed == 1:
        print("A_release")
        but_a_pressed=0

