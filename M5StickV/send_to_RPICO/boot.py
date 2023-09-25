import lcd
import sensor
from Maix import I2S, GPIO
from fpioa_manager import fm
from board import board_info
import time
from machine import I2C, UART


# UART設定
fm.register(35, fm.fpioa.UART2_TX, force=True)
fm.register(34, fm.fpioa.UART2_RX, force=True)
uart = UART(UART.UART2, 115200,8,0,0, timeout=1000, read_buf_len= 4096)


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

pixel_layout=[16,16]

#ABボタンの定義
fm.register(board_info.BUTTON_A, fm.fpioa.GPIO1)
but_a=GPIO(GPIO.GPIO1, GPIO.IN, GPIO.PULL_UP)

fm.register(board_info.BUTTON_B, fm.fpioa.GPIO2)
but_b = GPIO(GPIO.GPIO2, GPIO.IN, GPIO.PULL_UP)

but_a_pressed = 0
but_b_pressed = 0

#MENU画面設定
menu = 0
menu_list = [" 0. FLAT", " 1. CAMERA", " 2. CLOCK", " 3. LIFE GAME", " 4. M5STACK", " 5. MARIO", " 6. MOUSER", " 7. WAVE", " 8. AUTO", " 9. MAX","10. MIN","11. COLOR PANEL"," 0. FLAT"," 1. CAMERA", " 2. CLOCK", " 3. LIFE GAME"]

# データ開始の識別用パケット
start_packet = b'START'

# データ開始パケットを送信
#uart.write(start_packet)
#uart.write(b'\x00')
uart.write(bytes([0]))

def CAMERA():
    global but_a_pressed
    global camera_image
    lcd.direction(lcd.YX_LRDU)
    print("camera1")
    #time.sleep_ms(1000)
    while True:
        camera_image = sensor.snapshot()         # Take a picture and return the image.
        camera_image = camera_image.copy((20,0,140,120))
        lcd.display(camera_image)
        camera_image = camera_image.resize(pixel_layout[0], pixel_layout[1])
        uart.write(bytes([2]))
        image_list = []
        for x in range(pixel_layout[0]):
            listy = []
            for y in range(pixel_layout[1]):
                p = 255-camera_image.get_pixel(x,y)
                listy.append(p)
                uart.write(bytes([p]))
            image_list.append(listy)

        print("sended")
        print(image_list)
        if but_a.value() == 0 and but_a_pressed == 0:
            #print("A_push")
            but_a_pressed=1
            lcd.direction(lcd.YX_RLDU)
            display_menu()
            del camera_image
            break
        if but_a.value() == 1 and but_a_pressed == 1:
            #print("A_release")
            but_a_pressed=0
        time.sleep_ms(200)

        #break

def enter():
    global but_a_pressed
    print("start ",menu)
    while True:
        if but_a.value() == 0 and but_a_pressed == 0:
            #print("A_push-")
            but_a_pressed=1
            display_menu()
            break
        if but_a.value() == 1 and but_a_pressed == 1:
            #print("A_release-")

            but_a_pressed=0


def display_menu():
    global menu,menu_list
    lcd.clear((0,0,0))
    lcd.draw_string(20,20, "=== MENU (0 to 11)===", lcd.GREEN, lcd.BLACK)
    lcd.draw_string(20,40, ">", lcd.WHITE, lcd.BLACK)
    lcd.draw_string(30,40, menu_list[menu], lcd.BLACK, lcd.WHITE)
    lcd.draw_string(30,60, menu_list[menu+1], lcd.WHITE, lcd.BLACK)
    lcd.draw_string(30,80, menu_list[menu+2], lcd.WHITE, lcd.BLACK)
    lcd.draw_string(30,100, "....", lcd.WHITE, lcd.BLACK)

display_menu()

while True:
    if but_b.value() == 0 and but_b_pressed == 0:
        #print("B_push")
        menu += 1
        if menu > 11:
            menu = 0
        print("change to ",menu)
        display_menu()
        but_b_pressed=1

    if but_b.value() == 1 and but_b_pressed == 1:
        #print("B_release")
        but_b_pressed=0

    if but_a.value() == 0 and but_a_pressed == 0:
        #print("A_push")
        time.sleep_ms(200)
        but_a_pressed=1

        lcd.draw_string(30,40, menu_list[menu], lcd.BLACK, lcd.RED)
        uart.write(bytes([menu]))

        if menu == 1:
            CAMERA()

        else:
            enter()

    if but_a.value() == 1 and but_a_pressed == 1:
        #print("A_release")
        print("finish ", menu)
        time.sleep_ms(1000)
        uart.write(bytes([0]))
        but_a_pressed=0
