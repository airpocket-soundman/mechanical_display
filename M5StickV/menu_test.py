import lcd
import sensor
from Maix import I2S, GPIO
from fpioa_manager import fm
from board import board_info
import time



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


fm.register(board_info.BUTTON_A, fm.fpioa.GPIO1)
but_a=GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP)

fm.register(board_info.BUTTON_B, fm.fpioa.GPIO2)
but_b = GPIO(GPIO.GPIO2, GPIO.IN, GPIO.PULL_UP)

but_a_pressed = 0
but_b_pressed = 0

menu = 0
menu_list = ["1. CAMERA", "2. CLOCK", "3. LIFE GAME", "4. M5STACK", "5. MARIO", "6. MOUSER", "7. WAVE", "8. AUTO", "1. CAMERA", "2. CLOCK", "3. LIFE GAME"]

def CAMERA():
    global but_a_pressed

    lcd.direction(lcd.YX_LRDU)
    print("camera")
    camera_image = sensor.snapshot()         # Take a picture and return the image.
    camera_image = camera_image.copy((20,0,140,120))
    lcd.display(camera_image)
    while True:
        camera_image = sensor.snapshot()         # Take a picture and return the image.
        camera_image = camera_image.copy((20,0,140,120))
        lcd.display(camera_image)
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

