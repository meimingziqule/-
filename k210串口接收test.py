from fpioa_manager import fm
from machine import UART
import time
from board import board_info


fm.register(18, fm.fpioa.UART1_TX, force=True)
fm.register(19, fm.fpioa.UART1_RX, force=True)

uart = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=4096)

frame_head = '#'
frame_tail = ';'
task_flag = ''

while True:
    data = uart.read()
    if data:
       data_decoded = data.decode('utf-8')
       if data_decoded[0] == frame_head and data_decoded[2] == frame_tail:
            task_flag = data_decoded[1]
            print(task_flag)