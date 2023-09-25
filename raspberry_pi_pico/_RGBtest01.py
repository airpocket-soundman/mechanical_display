from machine import Pin, I2C, UART
import time
import pca9685
import servo
import font
import ds3231
import dot_image
import mechanical_display
import random
from math import cos,sin,tan

#=======================================================================================================================

# UART初期化
uart = UART(0, baudrate=115200) 


#displayのUnit配置数定義
unit_layout  = [4, 4]          #[width,height]　現在は[4,4]まで対応。増やす際は、I2Cのaddressリストも修正が必要。
servo_layout = [4, 4]
pixel_layout = [unit_layout[0] * servo_layout[0], unit_layout[1] * servo_layout[1]]
gray_scale_bit_value = 8
gray_scale_level = 2**gray_scale_bit_value

#I2C　初期化
i2c0 = I2C(0, freq = 1000000, scl=Pin(5), sda=Pin(4))
i2c1 = I2C(1, freq = 1000000, scl=Pin(3), sda=Pin(2))

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


#=====================================================================================================
#RTCのインスタンスを生成
ds = ds3231.DS3231(i2c0)

"""
#RTCの時間設定
year    = 2023 # Can be yyyy or yy format
month   = 9
mday    = 9
hour    = 15 # 24 hour format only
minute  = 31
second  = 30 # Optional
weekday = 6 # Optional

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


def clock_display(loop_num = 1000):
    counter = 0
    global finish_auto
    while counter < loop_num:
        if uart.any():
            received_message = uart_read_int()
            display.release()
            finsh_auto = 1
            break
        bg_image = display.bg_image_generate(50)

  #      print(bg_image)
        hour    = ds.datetime()[4]
        minute  = ds.datetime()[5]
        second  = ds.datetime()[6]
        hour_image      = Font.genTextImage(text = '{:02}'.format(hour),font = "number3x5p")
        colon_image     = Font.genTextImage(text = "  ", font = "propotional")
        minute_image    = Font.genTextImage(text = '{:02}'.format(minute),font = "number3x5p")
        sec_image       = Font.genTextImage(text = '{:02}'.format(second),font = "number3x5p")

        clock_image = display.textOverlay(bg_image,    hour_image,   offset = [0,2], text_color = 250, transparent = True)
        clock_image = display.textOverlay(clock_image, colon_image,  offset = [6,2], text_color = 250, transparent = True)
        clock_image = display.textOverlay(clock_image, minute_image, offset = [9,2], text_color = 250, transparent = True)
        clock_image = display.textOverlay(clock_image, sec_image,    offset = [9,9], text_color = 250, transparent = True)

        display.setImage(clock_image)
        #time.sleep_ms(10)
        counter += 1
        print(counter, "/", loop_num)

#=====================================================================================================

def uart_read_img_list():
    print("read_img")    

    while True:
        buffer = []
        if uart.any():
            for i in range(16):
                line_buffer = []
                for j in range(16):
                    received_byte = int.from_bytes(uart.read(1), 'big')
                    line_buffer.append(received_byte)
                buffer.append(line_buffer)
            print("Received data:", buffer)
        else:
            print("break")
            break
            

    
def uart_read_int():
    received_byte = int.from_bytes(uart.read(1), 'big')
    return received_byte
        

def uart_read_str():
    received_message = ""
    while uart.any():
        received_byte = uart.read(1)
        if received_byte:
            received_message += received_byte.decode()  # バイトを文字列に変換し、受信メッセージに追加

        if received_byte == b'\x00':
            return received_message  

#8bit gray scale 表示
def gray_scale_demo():
    color = 255
    for x in range(16):
        for y in range(16):
            display.setPixel([x, y],color)
            color -= 1

def mario_anime():
    Image = dot_image.dot_image()
    display.minPosition()
    time.sleep_ms(1000)

# marioが上から落ちてくる
    image = Image.genImage(image_name = "standing")
    shifted_image = display.shift_image(image,0,15)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "standing")
    shifted_image = display.shift_image(image,0,14)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "standing")
    shifted_image = display.shift_image(image,0,12)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "standing")
    shifted_image = display.shift_image(image,0,9)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "standing")
    shifted_image = display.shift_image(image,0,5)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "standing")
    shifted_image = display.shift_image(image,0,0)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "standing")
    shifted_image = display.shift_image(image,0,2)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "standing")
    shifted_image = display.shift_image(image,0,3)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "standing")
    shifted_image = display.shift_image(image,0,2)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "standing")
    shifted_image = display.shift_image(image,0,0)
    display.setImage(shifted_image)
    time.sleep_ms(1000)


    #marioが右に歩く

    image = Image.genImage(image_name = "run1")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "run2")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "run1")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "run2")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "run1")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "run2")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "run1")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "run2")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "run1")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "run2")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "run1")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "run2")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "run1")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "run2")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "run1")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "run2")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "run1")
    display.setImage(image)
    time.sleep_ms(100)

    #立ち止まる

    image = Image.genImage(image_name = "standing")
    display.setImage(image)
    time.sleep_ms(1000)

    #左に歩く

    image = Image.genImage(image_name = "run1")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "run2")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "run1")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "run2")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "run1")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "run2")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "run1")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "run2")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "run1")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "run2")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "run1")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "run2")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "run1")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "run2")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(100)


    # 走る

    image = Image.genImage(image_name = "run1")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(10)

    image = Image.genImage(image_name = "run2")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(10)


    image = Image.genImage(image_name = "run1")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(10)

    image = Image.genImage(image_name = "run2")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(10)

    image = Image.genImage(image_name = "run1")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(10)

    image = Image.genImage(image_name = "run2")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(10)

    image = Image.genImage(image_name = "run1")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(10)

    image = Image.genImage(image_name = "run2")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(10)

    image = Image.genImage(image_name = "run1")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(10)

    image = Image.genImage(image_name = "run2")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(10)

    image = Image.genImage(image_name = "run1")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(10)

    image = Image.genImage(image_name = "run2")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(10)

    image = Image.genImage(image_name = "run1")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(10)

    image = Image.genImage(image_name = "run2")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(10)

    image = Image.genImage(image_name = "run1")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(10)

    image = Image.genImage(image_name = "run2")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(10)

    image = Image.genImage(image_name = "run1")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(10)

    image = Image.genImage(image_name = "run2")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(10)

    image = Image.genImage(image_name = "run1")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(10)

    image = Image.genImage(image_name = "run2")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(10)

    image = Image.genImage(image_name = "run1")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(10)

    image = Image.genImage(image_name = "run2")
    image.reverse()
    display.setImage(image)
    time.sleep_ms(10)

    #急停止
    image = Image.genImage(image_name = "turn")
    #image.reverse()
    shifted_image = display.shift_image(image,0,0)
    display.setImage(image)
    time.sleep_ms(1000)

    #立つ
    image = Image.genImage(image_name = "standing")
    #image.reverse()
    display.setImage(image)
    time.sleep_ms(3000)

    #死ぬ
    image = Image.genImage(image_name = "dead")
    shifted_image = display.shift_image(image,0,0)
    display.setImage(shifted_image)
    time.sleep_ms(1500)

    image = Image.genImage(image_name = "dead")
    shifted_image = display.shift_image(image,0,4)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "dead")
    shifted_image = display.shift_image(image,0,6)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "dead")
    shifted_image = display.shift_image(image,0,7)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "dead")
    shifted_image = display.shift_image(image,0,6)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "dead")
    shifted_image = display.shift_image(image,0,4)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "dead")
    shifted_image = display.shift_image(image,0,0)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "dead")
    shifted_image = display.shift_image(image,0,-9)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImage(image_name = "dead")
    shifted_image = display.shift_image(image,0,16)
    display.setImage(shifted_image)
    time.sleep_ms(1500)

    fade_pattern = display.gen_fade_pattern(type = "UpLeft to DownRight")

    for i in range(len(fade_pattern)):
        for j in range(len(fade_pattern[i])):
            display.setPixel(coordinate = fade_pattern[i][j], value = gray_scale_level)
        time.sleep_ms(100)
    
    display.release()

def m5stack_anime():
    Image = dot_image.dot_image()
    #displayを最小値に
    display.minPosition()
    time.sleep_ms(1000)

    image = Image.genImageM5(image_name = "s1")
    shifted_image = display.shift_image(image,0,-15)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s1")
    shifted_image = display.shift_image(image,0,-14)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s1")
    shifted_image = display.shift_image(image,0,-13)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s1")
    shifted_image = display.shift_image(image,0,-12)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s1")
    shifted_image = display.shift_image(image,0,-11)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s1")
    shifted_image = display.shift_image(image,0,-10)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s1")
    shifted_image = display.shift_image(image,0,-9)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s1")
    shifted_image = display.shift_image(image,0,-8)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s1")
    shifted_image = display.shift_image(image,0,-7)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s1")
    shifted_image = display.shift_image(image,0,-6)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s1")
    shifted_image = display.shift_image(image,0,-5)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s1")
    shifted_image = display.shift_image(image,0,-4)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s1")
    shifted_image = display.shift_image(image,0,-3)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s1")
    shifted_image = display.shift_image(image,0,-2)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s1")
    shifted_image = display.shift_image(image,0,-1)
    display.setImage(shifted_image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s1")
    display.setImage(image)
    time.sleep_ms(2000)

    image = Image.genImageM5(image_name = "s2")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s3")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s4")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s5")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s6")
    display.setImage(image)
    time.sleep_ms(600)

    image = Image.genImageM5(image_name = "s7")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s8")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s9")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s10")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s11")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s12")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s13")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s14")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s15")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s16")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s17")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s18")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s19")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s20")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s21")
    display.setImage(image)
    time.sleep_ms(100)
    
    image = Image.genImageM5(image_name = "s22")
    display.setImage(image)
    time.sleep_ms(100)

    image = Image.genImageM5(image_name = "s23")
    display.setImage(image)
    time.sleep_ms(100)
    
    image = Image.genImageM5(image_name = "s24")
    display.setImage(image)
    time.sleep_ms(2000)

    image = Image.genImageM5(image_name = "s24")
    shifted_image = display.shift_image(image,1,0)
    display.setImage(shifted_image)
    time.sleep_ms(10)
    
    image = Image.genImageM5(image_name = "s24")
    shifted_image = display.shift_image(image,2,0)
    display.setImage(shifted_image)
    time.sleep_ms(10)

    image = Image.genImageM5(image_name = "s24")
    shifted_image = display.shift_image(image,3,0)
    display.setImage(shifted_image)
    time.sleep_ms(10)
    image = Image.genImageM5(image_name = "s24")
    shifted_image = display.shift_image(image,4,0)
    display.setImage(shifted_image)
    time.sleep_ms(10)
    image = Image.genImageM5(image_name = "s24")
    shifted_image = display.shift_image(image,5,0)
    display.setImage(shifted_image)
    time.sleep_ms(10)
    image = Image.genImageM5(image_name = "s24")
    shifted_image = display.shift_image(image,6,0)
    display.setImage(shifted_image)
    time.sleep_ms(10)
    image = Image.genImageM5(image_name = "s24")
    shifted_image = display.shift_image(image,7,0)
    display.setImage(shifted_image)
    time.sleep_ms(10)
    image = Image.genImageM5(image_name = "s24")
    shifted_image = display.shift_image(image,8,0)
    display.setImage(shifted_image)
    time.sleep_ms(10)
    image = Image.genImageM5(image_name = "s24")
    shifted_image = display.shift_image(image,9,0)
    display.setImage(shifted_image)
    time.sleep_ms(10)
    image = Image.genImageM5(image_name = "s24")
    shifted_image = display.shift_image(image,10,0)
    display.setImage(shifted_image)
    time.sleep_ms(10)
    image = Image.genImageM5(image_name = "s24")
    shifted_image = display.shift_image(image,11,0)
    display.setImage(shifted_image)
    time.sleep_ms(10)
    image = Image.genImageM5(image_name = "s24")
    shifted_image = display.shift_image(image,12,0)
    display.setImage(shifted_image)
    time.sleep_ms(10)
    image = Image.genImageM5(image_name = "s24")
    shifted_image = display.shift_image(image,13,0)
    display.setImage(shifted_image)
    time.sleep_ms(10)
    image = Image.genImageM5(image_name = "s24")
    shifted_image = display.shift_image(image,14,0)
    display.setImage(shifted_image)
    time.sleep_ms(10)
    image = Image.genImageM5(image_name = "s24")
    shifted_image = display.shift_image(image,15,0)
    display.setImage(shifted_image)
    time.sleep_ms(10)
    image = Image.genImageM5(image_name = "s24")
    shifted_image = display.shift_image(image,16,0)
    display.setImage(shifted_image)


    
    base_color = 10
    text_color = 245
    text_image = Font.genTextImage(text = "        M5STACK CREATIVITY CONTEST 2023",font = "propotional")
    bg_image = display.bg_image_generate(base_color)
    for x in range(len(text_image)):
        bg_image = display.bg_image_generate(base_color)
        image = display.textOverlay(bg_image, text_image, offset = [-x, 2], text_color = text_color, transparent = True)
    #    print("image", x)
        display.setImage(image)
        time.sleep_ms(50)
    
    display.release()

def mouser_log():
    # for mouser
    print("mouser")

    color_palette = [10,100,125,150,245]

    mouser_logo_1 =     [[0,4,4,4,4,4,4,4,4,4,4,4,4,4,4,0],
                         [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
                         [4,4,0,0,0,0,0,0,0,0,0,0,0,0,4,4],
                         [4,4,0,0,0,0,0,0,0,0,0,0,0,0,4,4],
                         [4,4,0,0,0,0,0,4,4,4,4,4,4,4,4,4],
                         [4,4,4,4,4,0,0,0,0,0,4,4,4,4,4,4],
                         [4,4,4,4,4,4,4,0,0,0,0,0,4,4,4,4],
                         [4,4,4,4,4,4,4,4,4,4,0,0,0,0,4,4],
                         [4,4,4,4,4,4,4,4,4,4,0,0,0,0,4,4],
                         [4,4,4,4,4,4,4,0,0,0,0,0,4,4,4,4],
                         [4,4,4,4,4,0,0,0,0,0,4,4,4,4,4,4],
                         [4,4,0,0,0,0,0,4,4,4,4,4,4,4,4,4],
                         [4,4,0,0,0,0,0,0,0,0,0,0,0,0,4,4],
                         [4,4,0,0,0,0,0,0,0,0,0,0,0,0,4,4],
                         [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
                         [0,4,4,4,4,4,4,4,4,4,4,4,4,4,4,0]]
    
    mouser_logo_2 =     [[0,1,1,1,1,1,1,1,4,4,4,4,4,4,4,0],
                         [1,1,1,1,1,1,1,1,1,4,4,4,4,4,4,4],
                         [1,1,0,0,0,0,0,0,0,0,0,0,0,0,4,4],
                         [1,1,0,0,0,0,0,0,0,0,0,0,0,0,4,4],
                         [1,1,0,0,0,0,0,1,1,4,4,4,4,4,4,4],
                         [1,1,1,1,1,0,0,0,0,0,4,4,4,4,4,4],
                         [1,1,1,1,1,1,1,0,0,0,0,0,4,4,4,4],
                         [1,1,1,1,1,1,1,1,2,4,0,0,0,0,4,4],
                         [1,1,1,1,1,1,1,2,2,4,0,0,0,0,4,4],
                         [1,1,1,1,1,1,2,0,0,0,0,0,4,4,4,4],
                         [1,1,1,1,2,0,0,0,0,0,4,4,4,4,4,4],
                         [2,2,0,0,0,0,0,2,4,4,4,4,4,4,4,4],
                         [2,2,0,0,0,0,0,0,0,0,0,0,0,0,4,4],
                         [2,2,0,0,0,0,0,0,0,0,0,0,0,0,4,4],
                         [3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4],
                         [0,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0]]
    
    image = mouser_logo_2

    for x in range(16):
        for y in range(16):
            image[x,y] = color_palette[image[x,y]]

    for x in range(33):
        shifted_image = display.shift_image(image,x - 17,0)
        display.setImage(shifted_image)
        if x == 17:
            time.sleep_ms(5000)

    base_color = 10
    text_color = 245
    """
    ss = 0
    ds = 1

    mouser_logo_image = [[ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                        [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                        [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                        [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                        [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                        [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                        [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                        [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                        [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                        [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                        [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                        [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                        [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                        [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                        [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                        [ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss],
                        [ss,ds,ds,ds, ds,ds,ds,ds, ds,ds,ds,ds, ds,ds,ds,ss],
                        [ds,ds,ds,ds, ds,ds,ds,ds, ds,ds,ds,ds, ds,ds,ds,ds],
                        [ds,ds,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ds,ds],
                        [ds,ds,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ds,ds],
                        [ds,ds,ss,ss, ss,ss,ss,ds, ds,ds,ds,ds, ds,ds,ds,ds],
                        [ds,ds,ds,ds, ds,ss,ss,ss, ss,ss,ds,ds, ds,ds,ds,ds],
                        [ds,ds,ds,ds, ds,ds,ds,ss, ss,ss,ss,ss, ds,ds,ds,ds],
                        [ds,ds,ds,ds, ds,ds,ds,ds, ds,ds,ss,ss, ss,ss,ds,ds],
                        [ds,ds,ds,ds, ds,ds,ds,ds, ds,ds,ss,ss, ss,ss,ds,ds],
                        [ds,ds,ds,ds, ds,ds,ds,ss, ss,ss,ss,ss, ds,ds,ds,ds],
                        [ds,ds,ds,ds, ds,ss,ss,ss, ss,ss,ds,ds, ds,ds,ds,ds],
                        [ds,ds,ss,ss, ss,ss,ss,ds, ds,ds,ds,ds, ds,ds,ds,ds],
                        [ds,ds,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ds,ds],
                        [ds,ds,ss,ss, ss,ss,ss,ss, ss,ss,ss,ss, ss,ss,ds,ds],
                        [ds,ds,ds,ds, ds,ds,ds,ds, ds,ds,ds,ds, ds,ds,ds,ds],
                        [ss,ds,ds,ds, ds,ds,ds,ds, ds,ds,ds,ds, ds,ds,ds,ss]]

    stop_counter = 17
    counter = 0
    bg_image = display.bg_image_generate(base_color)
    for x in range(len(mouser_logo_image)+1):
        if counter == stop_counter:
            time.sleep_ms(5000)
        bg_image = display.bg_image_generate(base_color)
        image = display.textOverlay(bg_image, mouser_logo_image, offset = [-x, 0], text_color = text_color, transparent = True)
        display.setImage(image)
        counter += 1

    time.sleep_ms(1000)
    """

    text_image = Font.genTextImage(text = "        MOUSER MAKE AWARDS 2023",font = "propotional")
    bg_image = display.bg_image_generate(base_color)
    print(text_image)
    for x in range(len(text_image)):
        bg_image = display.bg_image_generate(base_color)
        image = display.textOverlay(bg_image, text_image, offset = [-x, 2], text_color = text_color, transparent = True)
    #    print("image", x)
        display.setImage(image)
        time.sleep_ms(100)

    time.sleep_ms(200)
    display.release()


# life game関係
def initialize_board(ini = "glider"):
    # 初期状態の盤面を生成する
    board = [[0] * 16 for _ in range(16)]
    print(ini)
    # 盤面の一部を初期配置として設定する

    if ini == "glider":
        board[5][6] = 1
        board[6][7] = 1
        board[7][5] = 1
        board[7][6] = 1
        board[7][7] = 1

    else:
        positions = []
        for i in range(ini):
            positions.append(random.randint(0,255))
        for pos in positions:
            row = pos // 16
            col = pos % 16
            #print(row,col)
            board[row][col] = 1

    return board

def print_board(board):
    # 盤面を表示する
    bg_image = display.bg_image_generate(255)
    image = display.textOverlay(bg_image, board, offset = [0, 0], text_color = 0, transparent = True)
    display.setImage(image)

def count_neighbors(board, row, col):
    # 指定されたセルの周囲の生存セルの数を数える
    count = 0
    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
            if (i, j) != (row, col):
                # 周期境界条件を適用する
                neighbor_row = (i + 16) % 16
                neighbor_col = (j + 16) % 16
                count += board[neighbor_row][neighbor_col]
    return count

def update_board(board):
    # 盤面を更新する
    new_board = [[0] * 16 for _ in range(16)]

    for i in range(16):
        for j in range(16):
            count = count_neighbors(board, i, j)
            if board[i][j] == 1 and (count == 2 or count == 3):
                new_board[i][j] = 1
            elif board[i][j] == 0 and count == 3:
                new_board[i][j] = 1

    return new_board

def run_life_game(gen = 500):
    global finish_auto
    # Life Gameを実行する
    life_num = 20
    board = initialize_board(20)
    print("Initial state:")
    print_board(board)


    for generation in range(gen):
        if uart.any():
            received_message = uart_read_int()
            display.release()
            finish_auto = 1
            break
        
        board = update_board(board)
        total_life = sum(element for row in board for element in row)
        #print(total_life)
        if total_life == 0:
            board = initialize_board(life_num)
        if random.randint(1,100) <= 10:
            board[random.randint(0, 15)][random.randint(0, 15)] = 1
            print("meteo!!")
        print("Generation:",generation,"/",gen)
        print_board(board)
        time.sleep_ms(150)

def wave_tan(wave = 162):
    global finish_auto
    mag = 0
    step = 1
    for t in range(wave):
        if uart.any():
            received_message = uart_read_int()
            display.release()
            finish_auto = 1
            break
        for x in range(16):
            for y in range(16):
                display.setPixel(coordinate = [x,y], value = (((t + x) % 16)-8) * int(mag) + 125)
        if mag == 16:
            step = -1
        elif mag == 2:
            step = 1
        mag += step
    display.release()
#=====================================================================================================


def uart_read_img_list2():
    countx = 0
    county = 0
    count = 0
    image  = []
    imagey = []
    while True:
        if uart.any():
            count += 1
            received_byte = int.from_bytes(uart.read(1), 'big')
            #imagey.append(received_byte)
            imagey.insert(0,received_byte)
            county += 1
            if county > 15:
                image.append(imagey)
                imagey = []
                county = 0
                countx += 1
            
            if count == 256:
                print("return")
                return image

                

def camera(frame = 300):
    global finish_auto
    for i in range(frame):
#    while True:
        if uart.any():
            received_message = uart_read_int()
            print("mes=",received_message)
            if received_message == 1:
                while uart.any():
                     image = uart_read_img_list2()
                     print("image = ",image)
                     display.setImage(image)
            else:
                print("else")
                finish_auto = 1
                break

finish_auto = 0
def auto():
    global finish_auto
    while True:
        mouser_log()
        if finish_auto == 1:
            finish_auto = 0
            display.flatPosition()
            break
        m5stack_anime()
        if finish_auto == 1:
            finish_auto = 0
            display.flatPosition()
            break
        mario_anime()
        if finish_auto == 1:
            finish_auto = 0
            display.flatPosition()
            break
        clock_display(loop_num = 1500)
        if finish_auto == 1:
            finish_auto = 0
            display.flatPosition()
            break
        run_life_game(gen = 100)
        if finish_auto == 1:
            finish_auto = 0
            display.flatPosition()
            break
        wave_tan(wave = 300)
        if finish_auto == 1:
            finish_auto = 0
            display.flatPosition()
            break
        camera()
        if finish_auto == 1:
            finish_auto = 0
            display.flatPosition()
            break

def color_test():
    """
    red1    =   0
    yellow =  40
    green    = 100
    cian    = 125
    blue   = 150
    magenda  = 215
    red2    = 255

    RGB_list = [red2, magenda, blue, cian, green, yellow, red1]

    for i in range(1): #パターンの繰り返し回数
        for color in RGB_list:
            for y in range(4):
                for x in range(8):
                    display.setPixel(coordinate = [x, y], value = color)
            time.sleep_ms(500)
    """
    print("roop")
    for i in range(1024): #16の倍数をセット、16一回につき1ウェーブ
        color_list = []
        for j in range(16):
            k = i - j*4
            if k < 0:
                k = 0
            color_list.append((k%128)*2)
        
        color_num = 0
        print(color_list)
        for y in range(4):
            for x in range(4):
                
                display.setPixel(coordinate = [x,     y], value = color_list[color_num])
                display.setPixel(coordinate = [x + 4, y], value = color_list[color_num])
                color_num += 1
        print(color_list)
        time.sleep_ms(10)
    
    print("finish roop")
    for i in range(64): #16枚のパネルがすべてcolor=15に貼りつくまでの処理
        for j in range(16):
            color_list[j] += 2
            if color_list[j] > 254:
                color_list[j] = 254
        print(color_list)
        color_num = 0
        for y in range(4):
            for x in range(4):
                
                display.setPixel(coordinate = [x,     y], value = color_list[color_num])
                display.setPixel(coordinate = [x + 4, y], value = color_list[color_num])
                color_num +=1
        time.sleep_ms(10)

while True:
    
    if uart.any():
        received_message = uart_read_int()
        print(received_message)
        if received_message == 0:
            display.flatPosition()
            time.sleep_ms(100)
            display.release()
        if received_message == 1:
            print("camera")
            camera()
        if received_message == 2:
            print("clock")
            clock_display(loop_num = 1000)
        if received_message == 3:
            run_life_game(gen = 100)
        if received_message == 4:
            m5stack_anime()
        if received_message == 5:
            mario_anime()
        if received_message == 6:
            mouser_log()
        if received_message == 7:
            wave_tan(wave = 1000)
        if received_message == 8:
            finish_auto = 0
            auto()
        if received_message == 9:
            time.sleep_ms(5000)
            display.maxPosition()
            time.sleep_ms(100)
            display.release()
        if received_message == 10:
            display.minPosition()
            time.sleep_ms(100)
            display.release()
        if received_message == 11:
            color_test()
#display.maxPosition()
#time.sleep_ms(5000)
#display.flatPosition()
time.sleep_ms(1000)

display.release()
