from fpioa_manager import fm
from machine import UART
fm.register(35, fm.fpioa.UART2_TX, force=True)
fm.register(34, fm.fpioa.UART2_RX, force=True)

uart = UART(UART.UART2, 115200,8,0,0, timeout=1000, read_buf_len= 4096)

list2 = [[0,1,2,3],[2,3,4,5],[1,2,3,4]]
list2 = [[1,1,1,1],[2,2,2,2],[3,3,3,3]]

x = len(list2)
y = len(list2[0])
print("x",x)
print("y",y)

for i in range(10):

    # データ開始の識別用パケット
    start_packet = b'START'

    # データ開始パケットを送信
    uart.write(start_packet)

    # リストの要素数を送信
    uart.write(bytes([x]))
    uart.write(bytes([y]))

    # データを送信
    for i in range(x):
        for j in range(y):
            uart.write(bytes([list2[i][j]]))
