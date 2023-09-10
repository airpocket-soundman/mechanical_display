from machine import Pin, I2C, UART
import time


# UART初期化
uart = UART(0, baudrate=115200) 

def uart_read_img_list():
    # リストの要素数を受信
    x = int.from_bytes(uart.read(1), 'big')
    y = int.from_bytes(uart.read(1), 'big')
            
    print("x",x)
    print("y",y)

    # データを受信
    for i in range(x):
         line_buffer = []
         for j in range(y):
             received_byte = int.from_bytes(uart.read(1), 'big')
             line_buffer.append(received_byte)
         buffer.append(line_buffer)
    # 受信したデータを表示
    print("Received data:", buffer)

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

while True:
    if uart.any():
        received_message = uart_read_int()
        print(received_message)
 

# 必要ならば、通信を終了する
uart.deinit()





