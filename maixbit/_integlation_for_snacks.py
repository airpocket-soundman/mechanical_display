from machine import I2C
import time
import pca9685
import servo
import font
import ds3231
import dot_image
from Maix import GPIO
import lcd
import sensor
import mechanical_display
import random
from math import cos,sin,tan

#=======================================================================================================================


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
        print(counter, "/", loop_num)

# カメラ画像表示
def camera_show(delay = 1, frame = 500):
    counter = 0
    while frame > counter:
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
        print(counter,"/",frame)

#8bit gray scale 表示
def gray_scale_demo():
    color = 255
    for x in range(16):
        for y in range(16):
            display.setPixel([x, y],color)
            color -= 1


def snacks_text(base_color = 50, text_color = 200):
    print("snacks")
    text_image = Font.genTextImage(text = "        2023.7.17  SNACKS Vol.5 (>_0)",font = "propotional")
    bg_image = display.bg_image_generate(base_color)
    for x in range(len(text_image)):
        bg_image = display.bg_image_generate(base_color)
        image = display.textOverlay(bg_image, text_image, offset = [-x, 2], text_color = text_color, transparent = True)
        display.setImage(image)
        time.sleep_ms(50)

    time.sleep_ms(100)

    text_image = Font.genTextImage(text = "        MECHANICAL DISPLAY  8BIT GRAY SCALE VERSION.",font = "propotional")
    bg_image = display.bg_image_generate(base_color)
    for x in range(len(text_image)):
        bg_image = display.bg_image_generate(base_color)
        image = display.textOverlay(bg_image, text_image, offset = [-x, 9], text_color = text_color, transparent = True)
        display.setImage(image)
        time.sleep_ms(50)

    time.sleep_ms(1000)
    gray_scale_demo()


def mario_anime():
    Image = dot_image.dot_image()
    display.minPosition()
    time.sleep_ms(1000)
    image = Image.genImage(image_name = "standing")
    #display.setImage(image)
    time.sleep_ms(3000)

    display.minPosition()


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
            print(row,col)
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
    # Life Gameを実行する
    life_num = 20
    board = initialize_board(20)
    print("Initial state:")
    print_board(board)


    for generation in range(gen):
        board = update_board(board)
        total_life = sum(element for row in board for element in row)
        print(total_life)
        if total_life == 0:
            board = initialize_board(life_num)
        if random.randint(1,100) <= 10:
            board[random.randint(0, 15)][random.randint(0, 15)] = 1
            print("meteo!!")
        print("Generation:",generation,"/",gen)
        print_board(board)
        time.sleep(0.2)

def wave_tan(wave = 162):
    mag = 0
    step = 1
    for t in range(wave):
        for x in range(16):
            for y in range(16):
                display.setPixel(coordinate = [x,y], value = (((t + x) % 16)-8) * int(mag) + 125)
        if mag == 16:
            step = -1
        elif mag ==0:
            step = 1
        mag += step
#=====================================================================================================


while True:

    print("snacks")
    snacks_text(base_color = 50, text_color = 200)
    time.sleep_ms(2000)
    print("camera")
    camera_show(delay = 1, frame = 300)
    print("mario")
    mario_anime()
    time.sleep_ms(5000)
    print("life game")
    run_life_game(gen = 300)
    print("wave_tan")
    wave_tan(wave = 162)
    print("clock")
    clock_display(loop_num = 2000)
    time.sleep_ms(2000)
    fade_pattern = display.gen_fade_pattern(type = "UpLeft to DownRight")
    for i in range(len(fade_pattern)):
        for j in range(len(fade_pattern[i])):
            display.setPixel(coordinate = fade_pattern[i][j], value = gray_scale_level)
        time.sleep_ms(100)
    time.sleep_ms(5000)


#display.maxPosition()
#time.sleep_ms(5000)
#display.flatPosition()
time.sleep_ms(1000)

display.release()
