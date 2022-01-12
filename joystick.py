from machine import Pin, PWM, ADC
from machine import I2C
from sh1106 import SH1106_I2C
import time

potX = ADC(Pin(26))
potY = ADC(Pin(27))


while True:
    valX = potX.read_u16()
    valY = potY.read_u16()
    print("ValX:{}  ValY:{}".format(valX, valY))
    time.sleep_ms(100)