from machine import Pin, I2C, UART
import time


# UART初期化
uart = UART(0, baudrate=115200) # UARTポート0を使用し、ボーレート9600に設定

# データを受信するためのバッファ

# データ開始の識別用パケット
start_packet = b'START'

# データ開始パケットを待つ
while True:
    buffer = []
    if uart.any():
        if uart.read(len(start_packet)) == start_packet:
            print("len",len(start_packet))
            

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
                print(i)
        # 受信したデータを表示
            print("Received data:", buffer)
#            print(buffer[2])
    

# 必要ならば、通信を終了する
uart.deinit()





