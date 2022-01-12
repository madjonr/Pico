from machine import Pin
import utime

pins = [Pin(2, Pin.OUT), Pin(3, Pin.OUT), Pin(4, Pin.OUT), Pin(5, Pin.OUT)]

full_step_sequence = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]


while True:
    for step in full_step_sequence:
        for i in range(len(pins)):
            pins[i].value(step[i])
            utime.sleep_ms(1)
    #utime.sleep(0.1)