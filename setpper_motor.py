from machine import Pin
import utime

pins = [Pin(18, Pin.OUT), Pin(19, Pin.OUT), Pin(20, Pin.OUT), Pin(21, Pin.OUT)]

# full_step_sequence = [[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0],[0,0,1,0],[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0],[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,0]]
# full_step_sequence = [[1,0,0,1],[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,1,1],[0,0,0,1]]
# full_step_sequence = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
full_step_sequence = [[-1,0,1,0],[0,1,0,-1],[1,0,-1,0],[0,-1,0,1]]    # 42步进电机单拍
# full_step_sequence = [[-1,-1,1,1],[-1,1,1,-1],[1,1,-1,-1],[1,-1,-1,1]]    # 42步进电机双拍
# full_step_sequence = [[-1,-1,1,1],[0,-1,0,1],[1,-1,-1,1],[1,0,-1,0],[1,1,-1,-1],[0,1,0,-1],[-1,1,1,-1],[-1,0,1,0]]    # 42步进电机半拍


while True:
    for step in full_step_sequence:
        for i in range(len(pins)):
            pins[i].value(step[i])
            utime.sleep_ms(1)
    # utime.sleep(3)