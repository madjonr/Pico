from machine import Pin, PWM, ADC
from machine import I2C
from sh1106 import SH1106_I2C
import time

adc = ADC(Pin(28))
pwm1 = PWM(Pin(5))
pwm2 = PWM(Pin(4))
pwm1.freq(1000)
pwm2.freq(1000)


i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SH1106_I2C(128, 64, i2c)

oled.rotate(True)

while True:
    pwm1.duty_u16(adc.read_u16())
    pwm2.duty_u16(65535-adc.read_u16())
    
    oled.fill(0)
    oled.text("hello teanur", 10, 10)
    oled.text("go play wow", 10, 20)
    oled.text("value {}".format(adc.read_u16()), 10, 40)
    oled.show()
    
    time.sleep(0.1)
